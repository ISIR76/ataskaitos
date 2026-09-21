# Ataskaitos

Mokslinių dokumentų vertinimo platforma. Ji priima įkeltą dokumentą (DOCX, PDF,
MD, TXT), konvertuoja jį į Markdown ir įvertina dideliais kalbos modeliais pagal
paskelbtą standartą.

## Ką vertina

| Dokumento tipas | Standartas | Balų vertintojai | Agentai |
|---|---|---|---|
| **Ataskaita** (`report`) — MTEP veiklos ataskaitos | Frascati vadovas (OECD) | 8 | 4 |
| **Straipsnis** (`article`) — mokslinės publikacijos | SMSM reglamentas | 45 | 3 |

## Du vertinimo režimai

**Balų režimas** (`evaluation_type=scoring`) paleidžia LLM teisėjų rinkinį.
Kiekvienas teisėjas turi savo aprašą (rubriką) ir grąžina `0,0–1,0` balą su
pagrindimu. Vienas teisėjas — vienas LLM iškvietimas su visu dokumentu, o visi
pasirinkti teisėjai vykdomi vienu metu. Šį režimą sąsaja naudoja pagal
nutylėjimą.

**Agentų režimas** (`evaluation_type=agent`) paleidžia vieną ar kelis PydanticAI
agentus, kurie grąžina struktūrizuotą Pydantic objektą, o ne pavienį balą.
Agentai vykdomi nuosekliai ir vienam dokumentui kainuoja gerokai mažiau, nes
dokumentas siunčiamas vieną kartą, o ne po vieną kiekvienam kriterijui.

Žr. [Balų vertintojai](evaluators.md) ir [Agentai](agents.md).

## Trumpai

- **Modelis gamyboje:** `openai:gpt-4o` visiems teisėjams ir agentams,
  `temperature=0`.
- **Kaina vienam vertinimui:** ~0,31 USD ataskaitai, ~1,71 USD straipsniui su
  45 kriterijais (40 000 simbolių dokumentas). Žr.
  [Modeliai ir tokenų kaštai](models-and-tokens.md).
- **Serverio dalis:** FastAPI + PydanticAI + pydantic-evals, paleista su Uvicorn.
- **Naudotojo sąsaja:** React + TypeScript + TanStack Router, sukompiliuojama ir
  patiekiama iš to paties konteinerio.
- **Autentikacija:** JWT per `fastapi-users`.
- **Paketų tvarkyklė:** `uv`.

## Kur toliau

| Jei norite… | Skaitykite |
|---|---|
| paleisti lokaliai | [Pirmi žingsniai](getting-started.md) |
| suprasti, kaip eina užklausa | [Architektūra](architecture.md) |
| pridėti ar pataisyti vertinimo kriterijų | [Balų vertintojai](evaluators.md) |
| kviesti API | [HTTP API](api.md) |
| žinoti, ką daro nustatymas | [Konfigūracija](configuration.md) |
| įvertinti kaštus ar tokenų sąnaudas | [Modeliai ir tokenų kaštai](models-and-tokens.md) |
| planuoti vienalaikius naudotojus | [Našumas ir mastelis](scaling.md) |
| diegti | [Diegimas](deployment.md) |

!!! note "Šie puslapiai pakeičia `API.md`"
    Repozitorijoje dar yra senesnis `API.md` ir `## API Usage` skyrius
    `README.md` faile. Abu aprašo ankstesnę revizuiją — `X-API-Key`
    autentikaciją ir `/evaluate/agent` tipo maršrutus — kurios esamas kodas
    nebeaptarnauja. [HTTP API](api.md) sudarytas iš veikiančios programos
    maršrutų lentelės ir yra tikslus žinynas.
