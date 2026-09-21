# Kūrimas

## Repozitorijos sandara

```
ataskaitos/              # Pagrindinis paketas
├── api/                 # FastAPI programa, maršrutai, priklausomybės
│   └── routes/          # evaluate, projects, evaluators, auth, health
├── agents/              # Agentų fabrikas, registras, atsakymų schemos
├── evaluators/          # Registras, įkėlėjas ir JSON aprašai
│   ├── articles/        # smsm_judges.json    (45)
│   └── reports/         # frascati_judges.json (8)
├── models/              # SQLAlchemy ir srities modeliai
├── repositories/        # Duomenų prieiga pagal agregatą
├── services/            # DocumentService, EvaluationService, saugykla
├── prompts/             # Agentų instrukcijų tekstai
├── analysis/            # Rezultatų analizės pagalbinės funkcijos
├── cli.py               # Click CLI
├── database.py          # Variklis, sesija, init_db
├── settings.py          # pydantic-settings Settings
├── evals.py             # Neinteraktyvūs ataskaitų vertintojai (fiksuoja gemini-2.5-pro)
└── agent_from_human.py  # MTEP agentas ir jo 76 laukų schema

straipsniai/             # Neinteraktyvūs straipsnių vertinimo eksperimentai
frontend/                # React + TypeScript + TanStack Router
scripts/
├── analysis/            # ML ir statistinė analizė
├── evaluation/          # Kelių modelių lyginimo paleidėjas
└── utils/               # Konvertavimo ir atvaizdavimo įrankiai
tests/
docs/                    # Ši dokumentacija (mkdocs šaltinis)
```

`ataskaitos/evals.py` ir `straipsniai/evals.py` yra kūrimo įrankiai, ne
aptarnaujamos programos dalis. `ataskaitos/api.py` yra pakeistas
`ataskaitos/api/` paketo ir nebenaudojamas.

## Testai

```bash
uv run pytest
uv run pytest tests/test_services/test_evaluation_service.py   # vienas failas
uv run pytest -k evaluation                                     # pagal pavadinimą
```

## Kodo tikrinimas

```bash
make lint       # ruff check
make lint-fix   # ruff check --fix
```

`line-length = 120`, sukonfigūruota `pyproject.toml`. Tipų tikrintuvo nėra.

## Make komandos

| Komanda | Paskirtis |
|---|---|
| `make dev` | Paleisti API su perkrovimu prie 8000 |
| `make lint`, `make lint-fix` | Ruff |
| `make eval-agent` | Kelių modelių agentų lyginimas |
| `make eval-reports`, `make eval-articles` | Neinteraktyvūs vertintojų paleidimai |
| `make convert-latest` | Naujausi rezultatai → CSV požymių lentelė |
| `make analyze-latest` | sklearn analizė iš to CSV |
| `make show-latest` | Atspausdinti prognozes |
| `make pdf-latest` | Naujausių rezultatų PDF ataskaita |
| `make pipeline` | `eval-agent` → `convert-latest` → `analyze-latest` |
| `make combine-results` | Sulieti rezultatų failus |
| `make clean` | Ištrinti sugeneruotus išvestinius failus |
| `make deploy` | Diegti į Cloud Run |
| `make docs-serve` | Patiekti šią dokumentaciją su gyvu perkrovimu |
| `make docs-build` | Sukompiliuoti dokumentaciją į `site/` |
| `make docs-pdf` | Suformuoti dokumentaciją į vieną PDF |

## Dokumentacija

Dokumentacija yra [MkDocs](https://www.mkdocs.org/) svetainė su Material tema.
Šaltiniai — Markdown failai kataloge `docs/`, o navigacija aprašyta
`mkdocs.yml`.

```bash
uv sync --group docs     # įdiegti dokumentacijos įrankius
make docs-serve          # http://localhost:8001 su gyvu perkrovimu
make docs-build          # statinė svetainė į site/
```

`site/` yra generuojamas ir neversijuojamas.

Katalogai `docs/out/` ir `docs/reference_documents/` bei du vidiniai darbiniai
failai (`evaluator-service-plan.md`, `frascati_evaluation_str.md`) į svetainę
neįtraukiami — jie išvardyti `exclude_docs` sąraše `mkdocs.yml`.

### PDF

`print-site` papildinys suformuoja visus puslapius į vieną spausdinamą
dokumentą adresu `/print_page/`. PDF pasidaryti:

```bash
make docs-pdf            # sukuria ataskaitos-docs.pdf
```

Ši komanda sukompiliuoja svetainę ir atspausdina sujungtą puslapį per fone
veikiantį Chrome. Arba, kol veikia `make docs-serve`, atsidarykite
<http://localhost:8001/print_page/> ir pasinaudokite naršyklės „Spausdinti į
PDF“.

Šriftai į PDF įterpiami kaip duomenų URI: fone veikiantis Chrome nepatikimai
suspėja atsisiųsti tinklinius šriftus per savo laiko limitą, o be įterpimo PDF
tyliai nusirenka į sistemos šriftus. Tuo užsiima
`scripts/report/build_pdf.py`, kuris po suformavimo dar ir patikrina, ar
tikrieji šriftai tikrai pateko į PDF.

### Susitarimai

- Rašykite, ką kodas daro, o ne ką turėtų daryti. Kur elgesys netikėtas,
  pasakykite tai atskirame įspėjime, o ne tyliai dokumentuokite ketinimą.
- Nepatikrintus skaičius pažymėkite kaip įverčius. Puslapyje
  [Modeliai ir tokenų kaštai](models-and-tokens.md) dalis skaičių yra išmatuoti,
  dalis ne; tas skirtumas nurodytas aiškiai ir toks turėtų likti.
- Dėkite nuorodas tarp puslapių, o ne kartokite turinį, kad skaičius gyventų
  vienoje vietoje.

## Dokumentų konvertavimas rankomis

DOCX į Markdown:

```bash
uv run python -m markitdown failas.docx > isvestis.md
uv run python -m markitdown --keep-data-uris failas.docx > su-vaizdais.md
```

Pagal nutylėjimą `markitdown` nukerpa base64 vaizdus; `--keep-data-uris` juos
išsaugo failo dydžio kaina.

Įterptus vaizdus išskirti:

```bash
uv run python ataskaitos/extract_images.py su-vaizdais.md images/
```

EMF failai išvestyje yra Windows vektorinė grafika, dažna Office dokumentuose —
paprastai schemos ir diagramos, kurias, jei reikia, galima konvertuoti į PNG.
