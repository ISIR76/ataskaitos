# HTTP API

Bazinis adresas kuriant lokaliai: <http://localhost:8000>. Interaktyvi
dokumentacija patiekiama adresu `/api/docs` (Swagger UI) ir `/api/redoc`, o
schema — `/api/openapi.json`.

Žemiau esanti maršrutų lentelė paimta iš veikiančios programos.

## Autentikacija

`fastapi-users` su JWT bearer strategija. Esamas kodas **nepalaiko**
`X-API-Key`, nepaisant to, ką rašo senesnis `API.md` repozitorijoje.

```bash
# 1. Registracija
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"jus@example.com","password":"pasirinkite-slaptazodi"}'

# 2. Prisijungimas — forma, o ne JSON, ir laukas vadinasi `username`
curl -X POST http://localhost:8000/auth/jwt/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=jus@example.com&password=pasirinkite-slaptazodi'
# → {"access_token":"eyJ...","token_type":"bearer"}

# 3. Naudojimas
curl http://localhost:8000/users/me -H "Authorization: Bearer $TOKEN"
```

Raktai nustoja galioti po `jwt_lifetime_seconds` (pagal nutylėjimą 3600).
Gamyboje būtina nustatyti `JWT_SECRET`.

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/auth/register` | POST | Sukurti naudotoją |
| `/auth/jwt/login` | POST | Iškeisti prisijungimo duomenis į bearer raktą |
| `/auth/jwt/logout` | POST | Anuliuoti esamą raktą |
| `/users/me` | GET, PATCH | Perskaityti ar atnaujinti esamą naudotoją |
| `/users/{id}` | GET, PATCH, DELETE | Valdyti naudotoją (supernaudotojas) |

## Gyvumas ir metaduomenys

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/api/` | GET | Šakninis gyvumo tikrinimas |
| `/api/health` | GET | Gyvumo tikrinimas su prieinamais metodais |
| `/api/cors-test` | GET | CORS konfigūracijos patikra |

!!! warning "`/health` nėra gyvumo maršrutas"
    Gyvumas yra **`/api/health`**. Nesutaptus adresus perima visa apimantis
    maršrutas, patiekiantis naudotojo sąsają, tad užklausa į `/health` grąžina
    sąsajos HTML su būsena 200. Todėl į `/health` nukreipti konteinerio
    tikrinimai rodo, kad viskas gerai, nepriklausomai nuo programos būsenos —
    žr. [Diegimas](deployment.md#gyvumo-tikrinimai).

## Vienkartinis vertinimas

Įkelti ir įvertinti viena užklausa, dokumento neišsaugant. Visi trys maršrutai
priima `multipart/form-data`, ne JSON.

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/api/v1/evaluate` | POST | Įvertinti įkeltą dokumentą |
| `/api/v1/reports/evaluate` | POST | Tas pat su fiksuotu `document_type=report` |
| `/api/v1/articles/evaluate` | POST | Tas pat su fiksuotu `document_type=article` |

**Formos laukai**

| Laukas | Būtinas | Reikšmės | Pastabos |
|---|---|---|---|
| `file` | taip | `.docx`, `.pdf`, `.doc`, `.txt`, `.md` | Bet kas kita — klaida 400 |
| `document_type` | taip (`/evaluate` maršrute) | `report`, `article` | |
| `evaluation_type` | ne | `scoring` (numatyta), `agent` | |
| `evaluators` | ne | kableliais atskirti pavadinimai | Balų režimas. Nenurodžius — **visi** |
| `agents` | ne | kableliais atskirti pavadinimai | Agentų režimas. Nenurodžius — **visi** |

```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file=@ataskaita.docx' \
  -F 'document_type=report' \
  -F 'evaluation_type=scoring' \
  -F 'evaluators=novelty_score,systematic_score'
```

**Atsakymas**

```json
{
  "evaluation_id": "…",
  "document_type": "report",
  "evaluation_type": "scoring",
  "status": "success",
  "markdown_content": "# Tyrimo ataskaita…",
  "results": {
    "total_cases": 1,
    "total_failures": 0,
    "averages": { "scores": { "novelty_score": 0.6 } },
    "cases": [
      {
        "scores": {
          "novelty_score": { "value": 0.6, "reason": "Įrodymai iš dokumento…" }
        }
      }
    ]
  },
  "metadata": { "filename": "ataskaita.docx", "character_count": 41233 }
}
```

!!! important "`status: success` nereiškia, kad suveikė visi kriterijai"
    Nepavykęs teisėjas užregistruojamas kaip nesėkmė, o užklausa vis tiek
    pavyksta. **Visada tikrinkite `results.total_failures`.** Ne nulinė reikšmė
    reiškia, kad balai daliniai — dažniausia priežastis yra teikėjo greičio
    limitai, o automatinio pakartojimo nėra. Žr.
    [Našumas ir mastelis](scaling.md#nera-pakartojimo-prie-greicio-limitu).

## Projektai ir dokumentų versijos

Ilgalaikis darbo būdas: projektas turi dokumento versijas, o vertinimai
kabinami prie versijos, kad redakcijas būtų galima lyginti.

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/api/v1/projects` | GET, POST | Sąrašas (filtruotas kvietėjui) arba sukūrimas |
| `/api/v1/projects/scores-grid` | GET | Balų matrica per kvietėjo projektus |
| `/api/v1/projects/{project_id}` | GET, DELETE | Perskaityti ar ištrinti projektą |
| `/api/v1/projects/{project_id}/marked-good` | PATCH | Pažymėti projektą kaip gerą pavyzdį |
| `/api/v1/projects/{project_id}/versions` | GET, POST | Versijų sąrašas arba naujos įkėlimas |
| `/api/v1/projects/{project_id}/versions/{version_id}` | GET, DELETE | Perskaityti ar ištrinti versiją |
| `/api/v1/projects/{project_id}/versions/{version_id}/markdown` | GET | Konvertuotas Markdown |
| `/api/v1/projects/{project_id}/versions/{version_id}/set-active` | POST | Padaryti šią versiją aktyvia |
| `/api/v1/projects/{project_id}/versions/{version_id}/evaluate` | POST | Įvertinti šią versiją |
| `/api/v1/projects/{project_id}/versions/{version_id}/llm-detect` | POST | Paleisti LLM atpažinimo agentą |
| `/api/v1/projects/{project_id}/versions/{version_id}/evaluations` | GET | Versijos vertinimų istorija |
| `/api/v1/projects/{project_id}/evaluations/{evaluation_id}` | GET | Vienas įrašytas vertinimas |

`POST .../evaluate` priima tuos pačius `evaluation_type`, `evaluators` ir
`agents` formos laukus kaip vienkartinis maršrutas, bet be `file` — dokumentas
imamas iš saugyklos. Dokumento tipą nustato projekto `project_type`:
`straipsnis` atitinka `article`, visa kita — `report`.

!!! warning "Ne visi šie maršrutai tikrina savininką"
    Autentikuoto kvietėjo reikalauja tik `list_projects`, `create_project`,
    `get_scores_grid`, `set_project_marked_good` ir `run_llm_detection`, o
    `project.user_id` su juo lygina tik pastarieji du. Likę šios lentelės
    maršrutai, tarp jų `evaluate_version` ir `upload_version`, priima
    neautentikuotas užklausas ir savininko netikrina.

## Vertintojų katalogas

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/api/v1/evaluators` | GET | Prieinamų vertintojų sąrašas su rubrikomis |
| `/api/v1/agents` | GET | Prieinamų agentų sąrašas su metaduomenimis |
| `/api/v1/evaluators-admin` | GET, POST | Įrašytų vertintojų aprašų sąrašas ar sukūrimas |
| `/api/v1/evaluators-admin/{id}` | PATCH, DELETE | Atnaujinti ar ištrinti aprašą |
| `/api/v1/evaluators-admin/{id}/active` | PATCH | Įjungti ar išjungti |

`evaluators-admin` maršrutams reikia autentikacijos. Pakeitimai įsigalioja jau
sekančiame vertinime be perkrovimo — žr.
[Balų vertintojai](evaluators.md#kur-gyvena-aprasai).

## Naudotojo sąsaja

| Maršrutas | Metodas | Paskirtis |
|---|---|---|
| `/{full_path:path}` | GET | Patiekia sukompiliuotą React sąsają |

Šis visa apimantis maršrutas registruojamas paskutinis, tad gauna tik tuos
adresus, kurių nepaėmė nė vienas API maršrutas.
