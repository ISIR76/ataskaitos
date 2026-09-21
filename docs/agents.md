# Agentai

Agentas — tai PydanticAI `Agent` su instrukcijų tekstu ir Pydantic atsakymo
schema. Jis perskaito dokumentą vieną kartą ir grąžina struktūrizuotą objektą,
tad agentų režimas kainuoja gerokai mažiau nei balų režimas — maždaug 6 kartus
mažiau ataskaitai ir 35 kartus mažiau straipsniui, nei leidžiant visus teisėjus.

Agentus kuria `AgentFactory` (`ataskaitos/agents/factory.py`), o registruoja
`AgentRegistry` (`ataskaitos/agents/registry.py`), kuris sukuriamas vieną kartą
ir laikomas modulio lygio globalioje kintamajame.

## Registruoti agentai

### Straipsniams

| Pavadinimas | Atsakymo schema | Paskirtis |
|---|---|---|
| `simple_article_agent` | `SimpleArticleEvaluation` | Greitas įvertinimas, bendra apžvalga |
| `detailed_article_agent` | `DetailedArticleEvaluation` | Išsami analizė su detalia išklotine |
| `llm_detector_agent` | `LLMDetectionResult` | Įvertina, ar straipsnis sugeneruotas LLM |

### Ataskaitoms

| Pavadinimas | Atsakymo schema | Paskirtis |
|---|---|---|
| `simple_report_agent` | `SimpleReportEvaluation` | Bazinis Frascati MTEP vertinimas |
| `frascati_classifier_agent` | `FrascatiClassifierEvaluation` | MTEP ar ne MTEP — žinių kūrimas prieš jų taikymą |
| `detailed_report_agent` | `DetailedReportEvaluation` | Pilna 5 kriterijų Frascati išklotinė su įrodymais |
| `mtep_agent` | `MTEPVertinimas` | Lietuvos MTEP standartas, griežti kriterijai |

Sąrašą su metaduomenimis galima gauti veikiant programai:

```bash
curl http://localhost:8000/api/v1/agents
```

## Instrukcijų tekstai

Instrukcijos yra paprasti tekstiniai failai kataloge `ataskaitos/prompts/`,
įkeliami agento kūrimo metu. Tai, kad jie nėra Python kode, reiškia, jog
instrukcijos pakeitimas yra teksto redagavimas ir perkrovimas, o ne kodo
pakeitimas.

| Failas | Dydis (simb.) |
|---|---|
| `articles/simple_article_agent.txt` | 518 |
| `articles/detailed_article_agent.txt` | 1 051 |
| `articles/llm_detector_agent.txt` | 2 581 |
| `reports/simple_report_agent.txt` | 775 |
| `reports/detailed_report_agent.txt` | 4 959 |
| `reports/frascati_classifier_agent.txt` | 9 514 |

Išimtis — `mtep_agent`: jį kuria `ataskaitos/agent_from_human.py`, kuriame
instrukcijos surašytos tiesiai Python kode kartu su 76 laukų atsakymo schema,
perimta iš žmogaus recenzento rubrikos.

## Vykdymas

`EvaluationService._evaluate_with_agent()` suformuoja vieną užklausą su
dokumentu ir trumpu, nuo dokumento tipo priklausančiu instrukcijų bloku, tada
paleidžia kiekvieną pasirinktą agentą **nuosekliai**:

```python
for agent_name, agent in agents.items():
    evaluation_result = await agent.run(prompt)
```

Todėl pasirinkus tris straipsnių agentus, užtruks maždaug tris kartus ilgiau nei
pasirinkus vieną. Tai priešingybė balų režimui, kur visi teisėjai išsiunčiami
vienu metu.

Rezultatai grąžinami sugrupuoti pagal agento pavadinimą:

```json
{
  "agent_evaluations": {
    "simple_article_agent": { "score": 0.72, "summary": "..." },
    "llm_detector_agent":   { "likelihood": 0.1, "reason": "..." }
  },
  "agent_count": 2
}
```

## Agento pridėjimas

Kitaip nei vertintojams, agentams reikia kodo pakeitimo ir diegimo.

1. **Aprašykite atsakymo schemą** kataloge `ataskaitos/agents/schemas/`:

    ```python
    class CustomEvaluation(BaseModel):
        score: float = Field(ge=0.0, le=1.0, description="Bendra kokybė")
        summary: str = Field(description="Dviejų sakinių pagrindimas")
    ```

    Laukų aprašai (`description`) yra dalis to, ką modelis mato užklausoje —
    rašykite juos kaip instrukcijas, ne kaip vidinius komentarus.

2. **Parašykite instrukcijų tekstą** faile
   `ataskaitos/prompts/articles/custom_agent.txt`.

3. **Pridėkite kūrimo metodą** faile `ataskaitos/agents/factory.py`:

    ```python
    @classmethod
    def create_custom_agent(cls, model: Optional[Model] = None) -> Agent[None, CustomEvaluation]:
        instructions = cls._load_prompt("articles/custom_agent.txt")
        if model is None:
            model_name = cls._get_model_name(settings.default_article_model)
            model = OpenAIResponsesModel(model_name, settings=cls._settings)
        return Agent(model=model, output_type=CustomEvaluation, instructions=instructions)
    ```

    Tai, kad `model` parametras yra neobligatorinis, ir leidžia neinteraktyviems
    modelių lyginimo skriptams paleisti tą patį agentą per kitus teikėjus.

4. **Užregistruokite** funkcijoje `get_agent_registry()`:

    ```python
    registry.register(
        "article",
        "custom_agent",
        factory.create_custom_agent(),
        metadata={
            "description": "Ką šis agentas vertina",
            "output_type": "CustomEvaluation",
        },
    )
    ```

Registras atmeta bet kokį `document_type`, kuris nėra `article` arba `report`.

## Modelių lyginimas { #modeliu-lyginimas }

`scripts/evaluation/run_agent.py` paleidžia vieną agentą per kelis teikėjus su
dokumentų rinkiniu ir įrašo rezultatus į
`docs/out/reports/agent_evaluations/`. Jis įmanomas būtent dėl aukščiau minėto
įterpiamo `model` parametro. Naudokite jį modelio keitimui pagrįsti matavimais,
o ne spėjimu — žr.
[Modeliai ir tokenų kaštai](models-and-tokens.md#modeliu-lyginimas-neinteraktyviai).

```bash
make eval-agent        # paleisti lyginimą
make convert-latest    # rezultatai → CSV požymių lentelė
make analyze-latest    # sklearn analizė
```
