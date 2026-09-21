# Pirmi žingsniai

## Ko reikia

- Python 3.13 ar naujesnis
- [uv](https://docs.astral.sh/uv/) Python priklausomybėms
- Node.js 20 ar naujesnis (tik naudotojo sąsajai kompiliuoti ar kurti)
- OpenAI API raktas

## Įdiegimas

```bash
uv sync
```

## Konfigūravimas

Nusikopijuokite pavyzdinį aplinkos failą ir įrašykite raktą:

```bash
cp .env.example .env
```

Minimaliai reikia:

```bash
OPENAI_API_KEY=sk-...
```

Visi teisėjai ir agentai pagal nutylėjimą veikia per OpenAI, tad be šio rakto
vertinimas nepavyks. `GOOGLE_API_KEY` ir `ANTHROPIC_API_KEY` reikalingi tik
neinteraktyviems modelių lyginimo skriptams. Visus nustatymus žr.
[Konfigūracija](configuration.md).

## Serverio paleidimas

```bash
make dev
```

Paleidžia Uvicorn su automatiniu perkrovimu adresu <http://localhost:8000>.
Atitinka:

```bash
uv run uvicorn ataskaitos.api:app --host=localhost --port=8000 --reload
```

Startuodama programa:

1. Sukuria SQLite duomenų bazę ir lenteles (pagal nutylėjimą
   `data/database/ataskaitos.db`).
2. Įkelia vertintojų aprašus iš pridėtų JSON failų.
3. Įrašo tuos aprašus į `evaluators` lentelę, jei jų ten dar nėra. Įrašymas yra
   idempotentinis, tad per administravimo API atlikti pakeitimai išlieka po
   perkrovimo.

Interaktyvi API dokumentacija — <http://localhost:8000/api/docs>.

!!! warning "Gyvumo maršrutas yra `/api/health`, ne `/health`"
    Nesutaptus maršrutus perima visa apimantis maršrutas, patiekiantis naudotojo
    sąsają, tad `/health` grąžina sąsajos HTML su būsena 200, o ne gyvumo
    atsakymą. Tai svarbu konteinerio tikrinimams — žr.
    [Diegimas](deployment.md).

## Naudotojo sąsajos paleidimas

```bash
cd frontend
npm install
npm run dev
```

Kūrimo serveris veikia adresu <http://localhost:5173>, kuris jau yra
numatytajame CORS sąraše.

## Pirmas vertinimas

Užregistruokite naudotoją ir prisijunkite, nes vertinimo maršrutams reikia JWT:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"jus@example.com","password":"pasirinkite-slaptazodi"}'

TOKEN=$(curl -s -X POST http://localhost:8000/auth/jwt/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=jus@example.com&password=pasirinkite-slaptazodi' | python3 -c 'import json,sys;print(json.load(sys.stdin)["access_token"])')
```

Tada įvertinkite dokumentą. Atkreipkite dėmesį: tai `multipart/form-data`
įkėlimas, ne JSON:

```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file=@ataskaita.docx' \
  -F 'document_type=report' \
  -F 'evaluation_type=scoring' \
  -F 'evaluators=novelty_score,systematic_score'
```

Nenurodžius `evaluators`, paleidžiami **visi** to tipo vertintojai — 8
ataskaitai ir 45 straipsniui. Prieš tai darant su dideliu dokumentu,
perskaitykite [Modeliai ir tokenų kaštai](models-and-tokens.md).

## Komandinė eilutė

CLI leidžia vertinti pavienius failus ir paketus neeinant per API:

```bash
# Viena ataskaita, agentų režimas
uv run python -m ataskaitos.cli ataskaitos agent ataskaita.docx

# Viena ataskaita, konkretūs teisėjai
uv run python -m ataskaitos.cli ataskaitos evals ataskaita.docx -e novelty_score -e systematic_score

# Paketas, 5 vienalaikiai vertinimai
uv run python -m ataskaitos.cli ataskaitos agent --batch "docs/**/*.docx" -c 5
```

Likusius įrankius žr. [Kūrimas](development.md).
