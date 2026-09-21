# Balų vertintojai

Balų vertintojas (toliau „teisėjas“) — tai rubrika ir pavadinimas. Vertinimo
metu kiekvienas jų tampa `pydantic_evals.evaluators.LLMJudge` objektu, kuris
gauna visą dokumentą ir savo rubriką, o grąžina `0,0–1,0` balą su pagrindimu.

**Vienas teisėjas — vienas LLM iškvietimas.** Pasirinkus 45 kriterijus,
dokumentas išsiunčiamas 45 kartus. Žr.
[Modeliai ir tokenų kaštai](models-and-tokens.md).

## Kaip sukuriamas teisėjas

`ataskaitos/evaluators/loader.py` visus teisėjus kuria vienodai:

```python
judge_params = {
    "rubric": rubric,
    "include_input": False,
    "score": {"evaluation_name": name, "include_reason": True},
}
if has_assertion:
    judge_params["assertion"] = {
        "evaluation_name": f"{name.replace('_score', '')}_qualified",
        "include_reason": True,
    }
LLMJudge(**judge_params)
```

Apie laukus:

- `include_input=False` neįtraukia duomenų aibės *įvesties* į užklausą. Tai
  **neišima dokumento** — dokumentas atkeliauja kaip vertinamas *rezultatas*,
  nes aibės užduoties funkcija yra tapatumo funkcija.
- `score` grąžina skaitinį rezultatą vertintojo pavadinimu.
- `has_assertion` prideda antrą, loginį rezultatą `<bazė>_qualified` prie balo.
  Papildomo LLM iškvietimo tai **nekainuoja**: vienas iškvietimas grąžina
  `reason`, `pass` ir `score` kartu.
- `model` neperduodamas, tad teisėjai naudoja tą modelį, kurį pydantic-evals
  turi numatytąjį. Žr.
  [Modeliai ir tokenų kaštai](models-and-tokens.md#teiseju-modelis-nera-uzfiksuotas).

## Kur gyvena aprašai { #kur-gyvena-aprasai }

Aprašai turi dvi vietas, ir svarbu, kuri veikia:

| Šaltinis | Kada naudojamas | Paskirtis |
|---|---|---|
| `ataskaitos/evaluators/{articles,reports}/*.json` | CLI ir neinteraktyvūs skriptai; startuojant įrašoma į DB | Versijuojami numatytieji |
| `evaluators` lentelė duomenų bazėje | Bet kuri API užklausa su sesija | Gyvi, naudotojo redaguojami aprašai |

Startuojant `seed_default_evaluators()` įterpia kiekvieną JSON apraše
nurodytą vertintoją, kurio lentelėje dar nėra, sutapatinant pagal
`(name, document_type)`. Esamos eilutės neliečiamos, tad **per administravimo
API atlikti pakeitimai išlieka po perkrovimų** ir nėra užrašomi JSON failais.

Užklausos metu `build_judges_from_db()` nuskaito lentelę ir grąžina aktyvių
eilučių teisėjus, tad rubrikos pakeitimas įsigalioja jau sekančiame vertinime
be perkrovimo.

## Ataskaitų vertintojai (Frascati)

8 vertintojai iš `ataskaitos/evaluators/reports/frascati_judges.json`.

| Pavadinimas | Prideda tvirtinimą | Rubrikos dydis (simb.) |
|---|---|---|
| `short_evaluator` | ne | 453 |
| `combined_score` | ne | 811 |
| `novelty_score` | ne | 644 |
| `creativity_score` | ne | 696 |
| `uncertainty_score` | ne | 875 |
| `systematic_score` | ne | 716 |
| `transferable_score` | ne | 754 |
| `comprehensive_rd_score` | **taip** | 8188 |

## Straipsnių vertintojai (SMSM) { #straipsniu-vertintojai-smsm }

45 vertintojai iš `ataskaitos/evaluators/articles/smsm_judges.json`. Jie
skirstosi į keturias grupes, kurios sąmoningai persidengia — kelios vertina tą
patį dalyką skirtingu detalumu, ir tai verta žinoti prieš pasirenkant visus.

**Pirminiai balai (7)** — pagrindiniai kriterijai su ilgiausiomis rubrikomis.

`scientific_apparatus_score`, `structure_organization_score`,
`novelty_contribution_score`, `publication_type_score`,
`publisher_quality_inference_score`, `academic_rigor_score`,
`comprehensive_text_based_score` (prideda tvirtinimą; 5400 simbolių rubrika).

**Antriniai balai (10)** — siauresni, su trumpesnėmis rubrikomis.

`reproducibility_score`, `citation_quality_score`,
`limitations_discussion_score`, `research_significance_score`,
`reporting_completeness_score`, `language_quality_score`,
`data_transparency_score`, `results_interpretation_score`,
`scope_appropriateness_score`, `theoretical_grounding_score`.

**Gradientiniai variantai (10)** — `*_fluid` pavadinimai, skirti tolygesniam
balų skirstiniui nei jų `*_score` atitikmenys.

`apparatus_fluid`, `structure_fluid`, `contribution_fluid`,
`venue_quality_fluid`, `rigor_fluid`, `reproducibility_fluid`,
`references_fluid`, `critical_awareness_fluid`, `importance_fluid`,
`overall_quality_fluid`.

**Iš recenzento perimti kriterijai (18)** — `giedre_*` pavadinimai, koduojantys
konkretaus recenzento kontrolinį sąrašą. Kiekvienas turi detalią (`*_detalus`)
ir kompaktišką formą.

`giedre_temos_formulavimas`, `giedre_temos_aktualumas_naujumas`,
`giedre_tikslas_uždaviniai_svoris`, `giedre_teorine_analize`,
`giedre_metodologija`, `giedre_rezultatai`,
`giedre_isvados_kokybe_gradientas`, `giedre_privaloma_struktura`,
`giedre_kalbos_stilius_binarinis`, `giedre_citavimas_baudos` ir pirmųjų
aštuonių `_detalus` variantai.

!!! tip "Rinkitės poaibį"
    Kadangi grupės persidengia, visus 45 leisti retai kada būtina. Perduokite
    `evaluators=` su kableliais atskirtu sąrašu, arba išjunkite eilutes per
    `PATCH /api/v1/evaluators-admin/{id}/active`. Kaštai auga tiesiškai su
    pasirinktų kriterijų skaičiumi.

## Vertintojo pridėjimas

**Per API** (įsimena iš karto, be perkrovimo ir be diegimo):

```bash
curl -X POST http://localhost:8000/api/v1/evaluators-admin \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "clarity_score",
    "document_type": "article",
    "rubric": "Vertinkite teksto aiškumą. 1,0 skirkite, kai...",
    "has_assertion": false
  }'
```

**Per JSON failus** (versijuojama; tampa numatytuoju naujose aplinkose):

```json title="ataskaitos/evaluators/articles/smsm_judges.json"
[
  {
    "name": "clarity_score",
    "rubric": "Vertinkite teksto aiškumą. 1,0 skirkite, kai...",
    "has_assertion": false
  }
]
```

Perkraukite, kad būtų įrašyta. Kadangi įrašymas niekada neperrašo esamos
eilutės, rubrikos redagavimas JSON faile **neturi jokio poveikio** toje
aplinkoje, kur vertintojas jau buvo įrašytas — tenai keiskite per API arba
pirma ištrinkite eilutę.

## Rubrikos rašymas

Teisėjas mato tik dokumentą ir rubriką. Praktinės pasekmės:

- Aiškiai nurodykite skalę. Aprašykite, kas nusipelno `1,0`, kas `0,0` ir bent
  vieną vidurio tašką, kitaip balai susispiečia.
- Reikalaukite įrodymų. Pagrindimo laukas yra tai, kas leidžia balą peržiūrėti.
- Vienam vertintojui — vienas dalykas. Sujungus kelis, gaunamas vidurkis, kurio
  skaitytojas nebeišskaido.
- Rubrikos ilgis yra realus kaštas, bet mažas prieš dokumentą: visos 8
  ataskaitos rubrikos sudaro apie 3 200 tokenų, visos 45 straipsnio — 10 300,
  o 40 000 simbolių dokumentas yra ~13 800 tokenų **kiekviename iškvietime**.
