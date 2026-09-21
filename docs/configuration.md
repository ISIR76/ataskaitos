# Konfigūracija

Nustatymai aprašyti faile `ataskaitos/settings.py` naudojant
`pydantic-settings`. Jie nuskaitomi iš aplinkos kintamųjų ir iš `.env` failo
darbiniame kataloge; aplinkos kintamieji turi viršenybę. Nežinomi `.env` įrašai
ignoruojami.

Priešdėlis nenaudojamas, tad **aplinkos kintamojo pavadinimas — tai lauko
pavadinimas didžiosiomis**: `default_article_model` nustatomas per
`DEFAULT_ARTICLE_MODEL`.

## API raktai

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `OPENAI_API_KEY` | nėra | **Būtinas.** Visi teisėjai ir agentai naudoja OpenAI |
| `GOOGLE_API_KEY` | nėra | Tik neinteraktyviems modelių lyginimo skriptams |
| `ANTHROPIC_API_KEY` | nėra | Tik neinteraktyviems modelių lyginimo skriptams |

## Modeliai

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `DEFAULT_ARTICLE_MODEL` | `openai:gpt-4o` | Straipsnių agentai |
| `DEFAULT_REPORT_MODEL` | `openai:gpt-4o` | Ataskaitų agentai |
| `DEFAULT_MTEP_MODEL` | `openai:gpt-4o` | Aprašytas, bet MTEP agento nenaudojamas — jis fiksuoja `gpt-4o` kode |
| `DEFAULT_TEMPERATURE` | `0.0` | Taikoma agentams |

Formatas yra `teikėjas:modelis`, tačiau naudojama tik dalis po dvitaškio, o
teikėjas visada instancijuojamas kaip `OpenAIResponsesModel`. Todėl nustatymas
`DEFAULT_ARTICLE_MODEL=google:gemini-2.5-pro` išsiųstų `gemini-2.5-pro` į
OpenAI ir nepavyktų.

**Šie nustatymai neturi jokio poveikio balų režimui.** Teisėjai jokio modelio
argumento negauna — žr.
[Modeliai ir tokenų kaštai](models-and-tokens.md#teiseju-modelis-nera-uzfiksuotas).

## Saugykla

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `DATA_DIRECTORY` | `data` | |
| `UPLOADS_DIRECTORY` | `data/uploads` | Kur rašo `LocalStorageService` |
| `USE_GCS` | `false` | `true` perjungia į Google Cloud Storage |
| `GCS_BUCKET_NAME` | nėra | Būtinas, kai `USE_GCS=true` |
| `GCS_PROJECT_ID` | nėra | |
| `GCS_CREDENTIALS_PATH` | nėra | Kelias iki paslaugos paskyros JSON failo |
| `GCS_BASE_PATH` | `ataskaitos` | Priešdėlis kibiro viduje |

Pagrindas pasirenkamas vieną kartą importo metu, tad `USE_GCS` pakeitimui
reikia perkrovimo.

## Duomenų bazė

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `DATABASE_URL` | `sqlite:///data/database/ataskaitos.db` | Automatiškai perrašomas į asinchroninę tvarkyklę |

`sqlite://` tampa `sqlite+aiosqlite://`, o `postgresql://` tampa
`postgresql+asyncpg://`; bet kokia kita schema perduodama nepakitusi. Įdiegti
tiek `aiosqlite`, tiek `asyncpg`.

Migracijų įrankio nėra. `init_db()` paleidžia `create_all()`, o tada fiksuotą
papildomų `ALTER TABLE` sakinių sąrašą faile `ataskaitos/database.py`, kiekvieną
atskiroje tranzakcijoje, kad pasikartojančio stulpelio klaida viena
nepanaikintų kitų. Naują stulpelį reikia įrašyti į tą sąrašą.

## Serveris

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `SERVER_HOST` | `0.0.0.0` | Naudoja `serve` CLI komanda |
| `SERVER_PORT` | `8000` | Konteineris vietoje to naudoja `PORT` |
| `ALLOWED_ORIGINS` | `localhost:5173`, `localhost:3000` ir jų `127.0.0.1` formos | CORS leidžiamų sąrašas |
| `CORS_MAX_AGE_SECONDS` | `3600` | |

`ALLOWED_ORIGINS` yra sąrašas. **Įdiegtą naudotojo sąsają bet kuriame kitame
adrese reikia čia įrašyti**, kitaip naršyklės užklausos neišlaikys CORS.

## Autentikacija

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `JWT_SECRET` | nėra | **Gamyboje būtina nustatyti** |
| `JWT_LIFETIME_SECONDS` | `3600` | Rakto galiojimo laikas |

## Programos metaduomenys

| Kintamasis | Numatyta | Pastabos |
|---|---|---|
| `API_VERSION` | `0.2.0` | Grąžina API |
| `SERVICE_NAME` | `ataskaitos-api` | |
| `ENVIRONMENT` | `development` | Nuskaitoma į `settings.environment` |
| `BATCH_EVALUATION_CONCURRENCY` | `5` | Tik numatytoji `-c` reikšmė paketinėms CLI komandoms |

!!! note "`BATCH_EVALUATION_CONCURRENCY` neriboja API"
    Tai tik CLI `--concurrency` parametro numatytoji reikšmė. API vertinimai
    išsiunčia visus pasirinktus teisėjus vienu metu be jokio ribojimo. Žr.
    [Našumas ir mastelis](scaling.md#neribotas-teiseju-vienalaikiskumas).

## Du kintamieji, kurie nėra nustatymai { #ne-nustatymai }

Du naudojami aplinkos kintamieji nėra `Settings` dalis:

- **`ENV`** nuskaitomas tiesiogiai su `os.getenv("ENV", "development")` faile
  `ataskaitos/api/dependencies.py` ir būtent jį nustato `deploy.sh`. Jis yra
  atskiras nuo `ENVIRONMENT`, kuris patenka į `settings.environment`. Nustačius
  vieną, antrasis nenustatomas.
- **`API_KEY`** kaip paslaptį įterpia `deploy.sh`, bet programa jo nebenaudoja.
  Jis priklausė ankstesnei `X-API-Key` schemai, kurią pakeitė JWT
  autentikacija.

## Stebėjimas

| Kintamasis | Paskirtis |
|---|---|
| `LOGFIRE_TOKEN` | Įjungia telemetrijos eksportą. Logfire sukonfigūruotas su `send_to_logfire="if-token-present"`, tad be šio rakto instrumentacija neveikia |
