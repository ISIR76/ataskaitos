# Diegimas

Programa diegiama į Google Cloud Run kaip vienas konteineris, aptarnaujantis ir
API, ir sukompiliuotą naudotojo sąsają.

## Konteineris

`Dockerfile` statomas ant `python:3.13-slim` ir atlieka abi statymo dalis:

1. Įdiegia Node.js 20 ir `uv`.
2. `uv sync --frozen` Python priklausomybėms.
3. `npm ci` ir `npm run build` naudotojo sąsajai.
4. Paleidžia `uvicorn ataskaitos.api:app` prie `${PORT:-8080}`.

Atkreipkite dėmesį į modulio kelią `ataskaitos.api`. Egzistuoja ir
`ataskaitos/api.py`, ir `ataskaitos/api/` paketas; Python pasirenka paketą, tad
aptarnaujama esama programa, o senasis `api.py` — kuriame dar yra buvusi
`X-API-Key` schema — yra nebenaudojamas kodas.

## Diegimo komanda

```bash
make deploy     # paleidžia ./deploy.sh
```

`deploy.sh` statosi iš šaltinio ir diegia:

| Nustatymas | Reikšmė |
|---|---|
| Projektas | `delves-sandbox` |
| Regionas | `europe-west1` |
| Paslauga | `ataskaitos` |
| Atmintis | `1Gi` |
| Procesoriai | `2` |
| **Maks. egzempliorių** | **`1`** |
| Prievadas | `8080` |
| Prieiga | `--allow-unauthenticated` |
| Aplinka | `ENV=production` |
| Paslaptys | `OPENAI_API_KEY`, `API_KEY`, `DATABASE_URL`, `JWT_SECRET` |

Paslaptys imamos iš Secret Manager. `API_KEY` vis dar įterpiamas, bet programa
jo nebenaudoja — žr.
[Konfigūracija](configuration.md#ne-nustatymai).

!!! warning "`deploy.sh` ir `service.yaml` nesutaria"
    Repozitorijoje taip pat yra `service.yaml` — Knative manifestas, nurodantis
    `maxScale: 10`, `2Gi` atminties, `timeoutSeconds: 300`,
    `cloud-run-service-account` tapatybę bei `GOOGLE_API_KEY` ir
    `ANTHROPIC_API_KEY` paslaptis. `make deploy` jo nenaudoja — nugali
    `deploy.sh` su vienu egzemplioriumi ir 1Gi. Vieną iš šių dviejų laikykite
    autoritetiniu, o kitą ištrinkite arba suderinkite; šiandien lengva
    perskaityti ne tą ir patikėti, kad paslauga masinasi automatiškai.

## Nustatymai, svarbūs gamyboje

| Kintamasis | Kodėl |
|---|---|
| `JWT_SECRET` | Be jo autentikacija nesaugi |
| `DATABASE_URL` | Numatytoji SQLite gyvena laikinajame konteinerio diske |
| `USE_GCS` | Palikus `false`, įkelti failai prarandami po perkrovimo |
| `ALLOWED_ORIGINS` | Įdiegtos sąsajos adresas turi būti sąraše, kitaip naršyklės užklausos neišlaikys CORS |
| `OPENAI_API_KEY` | Būtinas bet kokiam vertinimui |

`USE_GCS` nėra nustatomas `deploy.sh`, tad **failų saugykla šiuo metu yra paties
konteinerio diskas**. Įkelti dokumentai ir jų konvertuotas Markdown
neišgyvena perkrovimo ir nėra bendrinami tarp egzempliorių. Pakėlus
`--max-instances` ir nenustačius `USE_GCS=true`, kiekvienas egzempliorius
turėtų savo, kitiems nematomą, failų kopiją.

`DATABASE_URL` pateikiamas iš Secret Manager. `asyncpg` yra įdiegtas, o kodas
perrašo `postgresql://` į `postgresql+asyncpg://`, tad numatytas tikslas yra
PostgreSQL; patikrinkite paslapties reikšmę, o ne darykite prielaidą.

## Gyvumo tikrinimai { #gyvumo-tikrinimai }

`Dockerfile` `HEALTHCHECK` ir `service.yaml` startavimo bei gyvumo tikrinimai
visi kviečia **`/health`**.

!!! danger "Tikrinimai netikrina programos būklės"
    Programa gyvumą aptarnauja adresu `/api/health`. `/health` vietoje to
    sutampa su visa apimančiu sąsajos maršrutu ir grąžina naudotojo sąsajos
    HTML su būsena 200. Todėl kiekvienas tikrinimas pavyksta tol, kol procesas
    klauso prievado ir egzistuoja sukompiliuota sąsaja — įskaitant atvejus, kai
    įvykių ciklas užblokuotas arba vertinimas visiškai neveikia.

    Nukreipkite tikrinimus į `/api/health`.

Tai nemaloniai susijungia su blokuojančiu dokumento konvertavimu, aprašytu
puslapyje
[Našumas ir mastelis](scaling.md#blokuojantis-konvertavimas): tikrinimas į
tikrąjį maršrutą pasibaigtų laiko limitu ir sukeltų perkrovimą, o būtent tokio
signalo ir norima. Tikrinimas, pataikantis į sąsajos maršrutą, visą laiką
rodo, kad viskas gerai.

## Duomenų bazės schemos pakeitimai

Migracijų įrankio nėra. Startuojant `init_db()` kviečia `create_all()`, kuris
sukuria neegzistuojančias lenteles, bet niekada nekeičia esamų, o tada pritaiko
fiksuotą papildomų `ALTER TABLE` sakinių sąrašą iš `_ADDITIVE_COLUMNS` faile
`ataskaitos/database.py`:

```python
_ADDITIVE_COLUMNS: list[tuple[str, str, str]] = [
    ("projects", "is_marked_good", "BOOLEAN NOT NULL DEFAULT FALSE"),
]
```

Kiekvienas vykdomas atskiroje tranzakcijoje, o pasikartojančio stulpelio
klaidos nuslopinamos, tad veiksmas yra idempotentinis. **Stulpelio pridėjimo
modelyje neužtenka** — jį reikia pridėti ir čia, kitaip esami diegimai jo
negaus. Viskam, kas daugiau nei stulpelio pridėjimas (pervadinimai, tipų
keitimai, duomenų užpildymas), mechanizmo nėra visiškai ir reikia rankinio
plano.

## Prieš atveriant paslaugą didesniam naudotojų ratui

`deploy.sh` perduoda `--allow-unauthenticated`, o keli projektų API maršrutai
netikrina nei autentikacijos, nei savininko. Prieš plečiant prieigą,
perskaitykite
[Našumas ir mastelis](scaling.md#pasirengimas-keliems-naudotojams).
