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

## Gamybos projektas

Nuo 2026-09-21 gamyba gyvena atskirame Google Cloud projekte
`innate-client-508813-e6` („Ataskaitos-prod“). Ankstesnė aplinka buvo bendrame
`delves-sandbox` projekte kartu su nesusijusiomis paslaugomis; naujasis
projektas priklauso **kitai organizacijai** ir turi **atskirą atsiskaitymo
paskyrą**, tad ištekliai buvo ne perkelti, o sukurti iš naujo ir duomenys
nukopijuoti.

| Išteklius | Reikšmė |
|---|---|
| Projektas | `innate-client-508813-e6` (numeris `687594214295`) |
| Regionas | `europe-west1` |
| Cloud Run paslauga | `ataskaitos` |
| Paslaugos paskyra | `ataskaitos-run@innate-client-508813-e6.iam.gserviceaccount.com` |
| Cloud SQL | `ataskaitos-prod` (PostgreSQL 17, `europe-west1`, `db-g1-small`) |
| Duomenų bazė / naudotojas | `ataskaitos` / `ataskaitos` |
| Failų saugykla | `gs://ataskaitos-prod-687594214295` |
| Atvaizdų saugykla | `europe-west1-docker.pkg.dev/innate-client-508813-e6/cloud-run-source-deploy` |

Cloud SQL egzempliorius turi viešą IP, bet **nė vieno leidžiamo tinklo**
(`authorized networks`). Prisijungiama tik per Cloud Run Cloud SQL jungtį
(unix socket `/cloudsql/...`) arba per `cloud-sql-proxy` su IAM teisėmis, tad
iš interneto tiesiogiai prisijungti neįmanoma.

Skirtingai nuo ankstesnės aplinkos, paslauga sukasi su **tam skirta paslaugos
paskyra**, o ne su numatytąja `compute` paskyra. Jos teisės: `cloudsql.client`,
`logging.logWriter`, `secretmanager.secretAccessor` kiekvienai paslapčiai ir
`storage.objectAdmin` failų saugyklos kibirui.

## Diegimo komanda

```bash
make deploy     # paleidžia ./deploy.sh
```

`deploy.sh` statosi iš šaltinio ir diegia:

| Nustatymas | Reikšmė |
|---|---|
| Projektas | `innate-client-508813-e6` |
| Regionas | `europe-west1` |
| Paslauga | `ataskaitos` |
| Atmintis | `1Gi` |
| Procesoriai | `2` |
| **Maks. egzempliorių** | **`1`** |
| Prievadas | `8080` |
| Prieiga | `--allow-unauthenticated` |
| Aplinka | `ENV=production`, `USE_GCS=true`, `GCS_BUCKET_NAME`, `GCS_PROJECT_ID` |
| Paslaptys | `OPENAI_API_KEY`, `API_KEY`, `DATABASE_URL`, `JWT_SECRET` |

Paslaptys imamos iš Secret Manager. `API_KEY` vis dar įterpiamas, bet programa
jo nebenaudoja — žr.
[Konfigūracija](configuration.md#ne-nustatymai).

!!! note "`service.yaml` yra veidrodis, ne šaltinis"
    Repozitorijoje esantis `service.yaml` (Knative manifestas) buvo suderintas
    su `deploy.sh`: tas pats projektas, paslaugos paskyra, Cloud SQL jungtis,
    aplinkos kintamieji ir `maxScale: 1`. Autoritetingas išlieka `deploy.sh` —
    būtent jį paleidžia `make deploy`. Keisdami vieną, atnaujinkite ir kitą.

## Nustatymai, svarbūs gamyboje

| Kintamasis | Kodėl |
|---|---|
| `JWT_SECRET` | Be jo autentikacija nesaugi |
| `DATABASE_URL` | Numatytoji SQLite gyvena laikinajame konteinerio diske |
| `USE_GCS` | Palikus `false`, įkelti failai prarandami po perkrovimo |
| `ALLOWED_ORIGINS` | Įdiegtos sąsajos adresas turi būti sąraše, kitaip naršyklės užklausos neišlaikys CORS |
| `OPENAI_API_KEY` | Būtinas bet kokiam vertinimui |

`USE_GCS=true` dabar **yra** nustatytas `deploy.sh`, tad įkelti dokumentai ir jų
konvertuotas Markdown rašomi į `gs://ataskaitos-prod-687594214295` ir išgyvena
perkrovimą. Anksčiau šis kintamasis nebuvo nustatytas ir failai gyveno paties
konteinerio diske.

Abi saugyklos realizacijos (`LocalStorageService` ir `GCSStorageService`)
kelią skaičiuoja iš `(project_id, version_number)`, o ne iš duomenų bazėje
įrašyto kelio, tad `USE_GCS` perjungimas nesugadina esamų įrašų.

`ALLOWED_ORIGINS` nenustatytas ir gamyboje: sąsaja aptarnaujama iš to paties
konteinerio (to paties kilmės adreso), tad CORS jai nereikalingas.

## Gyvumo tikrinimai { #gyvumo-tikrinimai }

Programa gyvumą aptarnauja adresu **`/api/health`**. `service.yaml` startavimo
ir gyvumo tikrinimai nukreipti būtent ten.

!!! warning "`Dockerfile` HEALTHCHECK vis dar rodo į `/health`"
    `Dockerfile` eilutėje 54 esantis `HEALTHCHECK` kviečia `/health`, kuris
    sutampa su visa apimančiu sąsajos maršrutu ir grąžina naudotojo sąsajos
    HTML su būsena 200 — tad pavyksta net tada, kai programa neveikia. Cloud Run
    šio `HEALTHCHECK` nepaiso (naudoja savo zondus), tad gamyboje žalos nėra,
    bet vietiniam Docker paleidimui tikrinimas yra beprasmis.

Cloud Run šiuo metu naudoja numatytąjį TCP startavimo zondą (prievadas 8080), o
ne `service.yaml` aprašytus HTTP zondus, nes paslauga diegiama `gcloud run
deploy` komanda, o ne manifestu.

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

Startuojant taip pat įsėjami numatytieji vertintojai („Seeded 53 default
evaluator definitions“). Veiksmas idempotentinis: perkeltoje duomenų bazėje
eilučių skaičius po paleidimo nepakito.

## Duomenų perkėlimas tarp projektų

Perkeliant duomenų bazę tarp projektų (pvz., kaip 2026-09-21 iš
`delves-sandbox`), paprasčiausias būdas yra serverinis Cloud SQL eksportas į
GCS ir importas į naują egzempliorių — nereikia nei atidaryti ugniasienės, nei
turėti duomenų bazės slaptažodžio vietoje:

```bash
gcloud sql export sql SENAS_EGZ gs://kibiras/dump.sql --database=ataskaitos
gcloud sql import sql NAUJAS_EGZ gs://kibiras/dump.sql --database=ataskaitos
```

Eksportuojančio egzemplioriaus paslaugos paskyrai reikia `storage.objectAdmin`,
importuojančiojo — `storage.objectViewer` atitinkamam kibirui; abi teises po
darbo verta atšaukti. Naudotojo vaidmuo (`ataskaitos`) naujame egzemplioriuje
turi būti sukurtas **prieš** importą. Po perkėlimo ištrinkite dump failus — juose
yra naudotojų duomenys.

## Prieš atveriant paslaugą didesniam naudotojų ratui

`deploy.sh` perduoda `--allow-unauthenticated`, o keli projektų API maršrutai
netikrina nei autentikacijos, nei savininko. Prieš plečiant prieigą,
perskaitykite
[Našumas ir mastelis](scaling.md#pasirengimas-keliems-naudotojams).
