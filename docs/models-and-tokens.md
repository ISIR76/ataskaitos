# Modeliai ir tokenų kaštai

Šis puslapis atsako į tris klausimus: kokie modeliai veikia gamyboje, kiek
tokenų sunaudoja vienas vertinimas ir kiek tai kainuoja.

Tokenų skaičiai čia **išmatuoti** — tikri dokumentai, tikros rubrikos ir tas
pats serializavimas, kurį atlieka kodas, suskaičiuota `o200k_base` koduote,
kurią naudoja `gpt-4o`. Išvesties tokenai ir trukmė yra **įvertinti**, ir tai
pažymėta.

## Modeliai gamyboje

Visi teisėjai ir visi agentai veikia su `gpt-4o` ir `temperature=0`.

| Komponentas | Modelis | Kur nustatyta |
|---|---|---|
| Balų teisėjai | `openai:gpt-4o` | Kode nenustatyta — pydantic-evals numatytoji reikšmė |
| Straipsnių agentai | `openai:gpt-4o` | `settings.default_article_model` |
| Ataskaitų agentai | `openai:gpt-4o` | `settings.default_report_model` |
| MTEP agentas | `openai:gpt-4o` | Fiksuota kode, `ataskaitos/agent_from_human.py` |

`GOOGLE_API_KEY` ir `ANTHROPIC_API_KEY` yra prijungti prie nustatymų ir prie
diegimo, bet nė vienas gamybinis kelias jų nenaudoja.

### Teisėjų modelis nėra užfiksuotas { #teiseju-modelis-nera-uzfiksuotas }

`ataskaitos/evaluators/loader.py` kiekvieną `LLMJudge` kuria be `model`
argumento, tad teisėjai naudoja tą, kurį pydantic-evals turi kaip
`_default_model`. Šiuo metu tai `openai:gpt-4o`.

!!! warning "Bibliotekos atnaujinimas gali pakeisti teisėjų modelį"
    Kadangi modelis perimamas, o ne nurodomas, `pydantic-evals` versijos
    pakėlimas gali nepastebimai pakeisti, kuris modelis vertina visus
    dokumentus — balai pasikeis be jokio pakeitimo šioje repozitorijoje.
    Užfiksuokite jį aiškiai, perduodami `model=` kuriant teisėją arba
    startuojant iškviesdami `set_default_judge_model()`.

Neinteraktyvus skriptas `ataskaitos/evals.py` modelį **užfiksuoja** —
importo metu kviečia `set_default_judge_model("gemini-2.5-pro")`. Tas modulis
nėra importuojamas API, tad aptarnaujamų užklausų jis nepaveikia.

### Modelio konteksto ribos

| Riba | `gpt-4o` | Praktinė pasekmė |
|---|---|---|
| Konteksto langas | 128 000 tokenų | Maksimalus dokumentas ≈ **370 000 simbolių**, apie 150 A4 lapų. Didesnis grąžins klaidą |
| Maksimalus atsakymas | 16 384 tokenai | Pakanka visoms esamoms atsakymų schemoms |

## Kodėl tokenų sąnaudos didelės

Balų režime duomenų aibės užduoties funkcija yra tapatumo funkcija, tad
kiekvieno teisėjo užklausoje kaip vertinamas rezultatas atsiduria **visas
dokumentas**, o po jo — to teisėjo rubrika. Todėl *N* kriterijų reiškia *N* LLM
iškvietimų, kiekviename po pilną dokumento kopiją.

```
dokumentas (13 800 tokenų)  ──┬──▶ teisėjas 1  (dokumentas + rubrika 1)
                              ├──▶ teisėjas 2  (dokumentas + rubrika 2)
                              │        ⋮
                              └──▶ teisėjas 45 (dokumentas + rubrika 45)
```

| Dokumento tipas | Kriterijai | LLM iškvietimų vienam vertinimui |
|---|---|---|
| Straipsnis | 45 | 45, visi išsiunčiami vienu metu |
| Ataskaita | 8 | 8, visi išsiunčiami vienu metu |

Agentų režimas dokumentą siunčia po vieną kartą kiekvienam agentui.

## Lietuviškas tekstas kainuoja daugiau vienam simboliui

Išmatuota `gpt-4o` koduote:

| Dokumentas | Simbolių | Tokenų | Simbolių tokenui |
|---|---|---|---|
| MTEP ataskaita (`energus-ataskaita.md`) | 111 834 | 37 736 | **2,96** |
| SMSM reglamentas | 47 832 | 17 386 | **2,75** |

Angliškas tekstas vidutiniškai turi apie 4 simbolius tokenui, tad
**lietuviškas tekstas tam pačiam ilgiui sunaudoja maždaug 1,4 karto daugiau
tokenų**. Žemiau esantys įverčiai naudoja 2,9.

## Tokenai vienam vertinimui

| Dokumento dydis | Režimas | Įvesties tokenų | Išvesties tokenų (įvert.) |
|---|---|---|---|
| Mažas — 4 000 simb. | Ataskaita, 8 kriterijai | 15 600 | ~2 000 |
| | Straipsnis, 45 kriterijai | 79 800 | ~11 300 |
| | Vienas agentas | 5 500 | ~2 500 |
| Vidutinis — 40 000 simb. | Ataskaita, 8 kriterijai | 114 900 | ~2 000 |
| | **Straipsnis, 45 kriterijai** | **638 500** | ~11 300 |
| | Vienas agentas | 17 900 | ~2 500 |
| Didelis — 112 000 simb. | Ataskaita, 8 kriterijai | 313 500 | ~2 000 |
| | **Straipsnis, 45 kriterijai** | **1 755 700** | ~11 300 |
| | Vienas agentas | 42 700 | ~2 500 |

Išvestis įvertinta po ~250 tokenų kriterijui — balas ir jo pagrindimas. Tikri
skaičiai yra Logfire, kai nustatytas `LOGFIRE_TOKEN`.

## Kaštai

Skaičiuota pagal `gpt-4o` viešą kainą: **2,50 USD** už milijoną įvesties
tokenų, **10,00 USD** už milijoną išvesties, **1,25 USD** už milijoną
podėliuotos įvesties. Prieš remiantis šiais skaičiais, kainas verta
pertikrinti.

| Dokumento dydis | Režimas | Kaina dabar | Su podėliavimu |
|---|---|---|---|
| Mažas | Ataskaita, 8 | 0,06 USD | 0,05 USD |
| | Straipsnis, 45 | 0,31 USD | 0,24 USD |
| | Vienas agentas | 0,04 USD | — |
| Vidutinis | Ataskaita, 8 | 0,31 USD | 0,19 USD |
| | **Straipsnis, 45** | **1,71 USD** | 0,95 USD |
| | Vienas agentas | 0,07 USD | — |
| Didelis | Ataskaita, 8 | 0,80 USD | 0,47 USD |
| | **Straipsnis, 45** | **4,50 USD** | 2,38 USD |
| | Vienas agentas | 0,13 USD | — |

### Mėnesinis planavimas

| Apimtis | Kaina dabar | Su podėliavimu |
|---|---|---|
| 100 ataskaitų (vidutinių) | ~31 USD | ~19 USD |
| 100 straipsnių (vidutinių, visi 45) | ~171 USD | ~95 USD |
| 1 000 straipsnių | ~1 710 USD | ~950 USD |

## Kaštų mažinimas

### 1. Įjungti užklausų podėliavimą — apie 45 % pigiau

Kiekvieno teisėjo užklausa prasideda **identiška** pradžia: teisėjo sistemos
instrukcija, po jos visas dokumentas. Skiriasi tik pabaigoje esanti rubrika.
Tai yra ideali forma automatiniam užklausų podėliavimui.

Šiandien tai neveikia, nes visi 45 iškvietimai išsiunčiami tą pačią
milisekundę ir nė vienas nemato podėlio, kurio kitas dar neįrašė. Pakanka pirmą
iškvietimą atlikti atskirai, o likusius 44 išleisti po jo — tada jie pataiko į
šiltą podėlį.

Tai vertingiausias prieinamas pakeitimas: nereikia nei keisti modelio, nei
kriterijų.

### 2. Pigesnis teisėjų modelis — iki maždaug 90 % pigiau

Teisėjai atlieka struktūrizuotą vertinimą pagal aiškią rubriką, o su tuo
mažesni modeliai neretai gerai susidoroja. Tam reikia patikrinimo, o ne
prielaidos, ir stendas tam jau egzistuoja.

### 3. Peržiūrėti kriterijų rinkinį

45 straipsnio kriterijai persidengia sąmoningai — pirminiai balai, `*_fluid`
gradientiniai variantai ir `giedre_*` recenzento kriterijai detalia bei
kompaktiška forma neretai vertina tą patį dalyką. Kaštai auga tiesiškai su
pasirinktų kriterijų skaičiumi, tad rinkinio sutvarkymas sutaupo proporcingai.
Žr. [Balų vertintojai](evaluators.md#straipsniu-vertintojai-smsm).

## Modelių lyginimas neinteraktyviai { #modeliu-lyginimas-neinteraktyviai }

`scripts/evaluation/run_agent.py` paleidžia agentą per kelis teikėjus su
dokumentų rinkiniu. Jis jau buvo naudotas su `gpt-4o`, `gpt-5.1`,
`claude-sonnet-4-5`, `claude-opus-4-5`, `gemini-3-pro-preview`,
`gemini-2.5-flash` ir `gemini-2.5-flash-lite`.

```bash
make eval-agent        # paleisti per sukonfigūruotus modelius
make convert-latest    # rezultatai → CSV požymių lentelė
make analyze-latest    # sklearn analizė
make show-latest       # atspausdinti prognozes
```

Rezultatai atsiranda kataloge `docs/out/reports/agent_evaluations/`. Naudokite
tai prieš keisdami bet kurį gamybinį modelį.

## Kas neišmatuota { #kas-neismatuota }

| Rodiklis | Statusas | Kaip uždaryti |
|---|---|---|
| Įvesties tokenai | Išmatuota | — |
| Išvesties tokenai | Įvertinta po ~250 kriterijui | Įrašyti `result.usage()` prie kiekvieno vertinimo |
| **Vertinimo trukmė** | **Neišmatuota** | Gamybinių matavimų nėra; `evaluations` lentelė šio teksto rašymo metu buvo tuščia. Logfire jau tai atseka |
| Teikėjo greičio limitai | Priklauso nuo paskyros | Pasitikrinti OpenAI valdymo skydelyje |

Vienas teisėjo iškvietimas su vidutiniu dokumentu tikėtinai užima 5–15
sekundžių, tad pilnas vertinimas — kažkur tarp 20 ir 60 sekundžių, kai niekas
neriboja. Traktuokite tai kaip eilės tvarką, ne kaip skaičių.
