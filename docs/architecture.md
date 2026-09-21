# Architektūra

## Komponentai

```
Naršyklė (React SPA)
   │  multipart įkėlimas + JWT
   ▼
FastAPI programa  (ataskaitos/api/app.py)
   ├── autentikacijos maršrutai   fastapi-users, JWT
   ├── /api/v1/evaluate           vienkartinis: įkelti, įvertinti, grąžinti
   ├── /api/v1/projects/...       ilgalaikiai projektai ir dokumentų versijos
   ├── /api/v1/evaluators-admin   vertintojų aprašų CRUD
   └── visa apimantis maršrutas   patiekia sukompiliuotą sąsają
   │
   ├── DocumentService     markitdown: DOCX/PDF/TXT/MD → Markdown
   ├── EvaluationService   valdo balų ir agentų režimus
   │      ├── balai  → pydantic-evals Dataset + LLMJudge (1 iškvietimas teisėjui)
   │      └── agentai → PydanticAI Agent (1 iškvietimas agentui)
   ├── StorageService      vietinis diskas arba Google Cloud Storage
   └── SQLAlchemy (async)  SQLite lokaliai, PostgreSQL gamyboje
```

## Vertinimo užklausos kelias

Abu vertinimo įėjimai atlieka tą patį darbą; skiriasi tik tuo, ar dokumentas
prieš tai išsaugomas.

1. **Įkėlimas.** `POST /api/v1/evaluate` priima failą tiesiogiai.
   `POST /api/v1/projects/{id}/versions/{id}/evaluate` vietoje to nuskaito
   anksčiau įkeltą versiją iš saugyklos.
2. **Konvertavimas.** `DocumentService.convert_to_markdown()` įrašo failą į
   laikinąjį failą ir paleidžia `markitdown`. Priimami plėtiniai: `.docx`,
   `.pdf`, `.doc`, `.txt`, `.md`; bet kas kita — klaida 400.
3. **Kriterijų atranka.** Balų režime su duomenų bazės sesija teisėjai
   sukuriami iš `evaluators` lentelės **kiekvienos užklausos metu**, tad
   rubrikų pakeitimai įsigalioja jau sekančiame vertinime be perkrovimo. Be
   sesijos (CLI naudojimas) naudojamas atmintyje esantis registras iš JSON.
4. **Vertinimas.** Žr. abu režimus žemiau.
5. **Grąžinimas ir įrašymas.** Projekto maršrutas įrašo rezultatą ir jo trukmę į
   `evaluations` lentelę. Vienkartinis maršrutas grąžina neįrašęs.

Visas vertinimas vyksta **HTTP užklausos viduje**. Nėra nei darbų eilės, nei
būsenos maršruto apklausai — tai pagrindinis vienalaikiškumo apribojimas, žr.
[Našumas ir mastelis](scaling.md).

## Balų režimas

`EvaluationService._evaluate_with_scoring()` suvynioja dokumentą į vieno atvejo
`pydantic_evals.Dataset`, kurio užduoties funkcija yra tapatumo funkcija, ir
prijungia po vieną `LLMJudge` kiekvienam pasirinktam kriterijui.

Kadangi užduotis yra tapatumo funkcija, kiekvieno teisėjo užklausoje kaip
vertinamas „rezultatas“ atsiduria **visas dokumentas**, o po jo — to teisėjo
rubrika. Tad *N* kriterijų reiškia *N* LLM iškvietimų, kiekviename po pilną
dokumento kopiją.

`Dataset.evaluate()` kviečiamas be `max_concurrency`, o pydantic-evals surenka
atvejo vertintojus be jokio ribojimo, tad **visi pasirinkti teisėjai
išsiunčiami vienu metu**. Pasirinkus visus 45 straipsnio kriterijus, išeina 45
vienalaikiai LLM iškvietimai.

Nepavykęs teisėjas — pavyzdžiui, dėl greičio limito klaidos — užklausos
nesugriauna. pydantic-evals užregistruoja tai kaip nesėkmę, o atsakymas vis tiek
grąžina `status: "success"`, o skaičius atsiduria
`results.total_failures` lauke. Tikrinkite šį lauką, kad žinotumėte, ar
rezultatas pilnas.

## Agentų režimas

`EvaluationService._evaluate_with_agent()` suformuoja užklausą su dokumentu ir
trumpu instrukcijų bloku, tada eina ciklu per pasirinktus agentus:

```python
for agent_name, agent in agents.items():
    evaluation_result = await agent.run(prompt)
```

Ciklas `await`inamas paeiliui, tad agentai vykdomi **vienas po kito**, ne
paraleliai. Kiekvienas grąžina Pydantic modelį, kuris `model_dump()` metodu
serializuojamas į atsakymą.

## Duomenų saugojimas

- **Duomenų bazė.** Asinchroninis SQLAlchemy. Lentelės: `users`, `projects`,
  `document_versions`, `evaluations`, `evaluators`. `init_db()` kviečia
  `create_all()`, o tada pritaiko fiksuotą papildomų `ALTER TABLE` sąrašą, nes
  `create_all()` niekada nekeičia jau esančios lentelės. Migracijų įrankio nėra,
  tad naują stulpelį reikia įrašyti į tą sąrašą faile `ataskaitos/database.py`.
- **Failai.** `StorageService` importo metu pasirenka pagrindą pagal `use_gcs`
  nustatymą: `LocalStorageService`, rašantis į `uploads_directory`, arba
  `GCSStorageService`. Saugomi ir įkelti originalai, ir jų konvertuotas
  Markdown.
- **Projektai ir versijos.** Projektas turi tvarkingą dokumento versijų aibę,
  iš kurių viena yra aktyvi. Vertinimai prikabinami prie versijos, tad
  rezultatus galima lyginti tarp to paties dokumento redakcijų.

## Autentikacija

`fastapi-users` su JWT strategija. `POST /auth/register` sukuria naudotoją,
`POST /auth/jwt/login` grąžina bearer raktą, o raktai galioja
`jwt_lifetime_seconds` (pagal nutylėjimą 3600). Apsaugoti maršrutai priklauso
nuo `current_active_user`.

!!! warning "Apsauga netolygi"
    Keli projektų maršrutai — įskaitant `evaluate_version`, `upload_version`,
    `get_project` ir `delete_project` — nepriklauso nuo `current_active_user` ir
    nelygina `project.user_id` su kvietėju. `Project` turi `user_id` lauką, o
    `list_projects` pagal jį filtruoja, tad duomenų modelis atskyrimą tarp
    naudotojų palaiko; tuose maršrutuose paprasčiausiai nėra patikrinimų. Tai
    būtina uždaryti prieš atveriant platformą keliems naudotojams. Žr.
    [Našumas ir mastelis](scaling.md#pasirengimas-keliems-naudotojams).

## Stebėjimas

Logfire sukonfigūruojamas importo metu su
`send_to_logfire="if-token-present"` ir instrumentuoja FastAPI, Pydantic bei
PydanticAI. Nustačius `LOGFIRE_TOKEN`, kiekvienas LLM iškvietimas atsekamas su
tikrosiomis tokenų sąnaudomis — tai greičiausias būdas pakeisti įverčius
puslapyje [Modeliai ir tokenų kaštai](models-and-tokens.md) tikrais matavimais.
