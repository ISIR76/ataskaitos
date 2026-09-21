# Našumas ir mastelis

Platforma gerai veikia po vieną naudotoją vienu metu — būtent tam ji šiuo metu
ir sukonfigūruota. Šis puslapis aprašo, kas nutinka esant vienalaikei apkrovai,
kodėl ir ką reikia pakeisti.

## Santrauka

**Dabartinės konfigūracijos maždaug 50 vienalaikių naudotojų sėkmingai
neaptarnautų.** Pirmosios užklausos pasibaigtų sėkmingai, dalis grąžintų
klaidas, o dalis būtų nutrauktos nepalikus jokio įrašo. Priežastys konkrečios ir
pataisomos, ir nė viena nereikalauja architektūros perprojektavimo.

## Kaip atrodo vienalaikiškumas

Vienoje užklausoje sugyvena du skirtingi vienalaikiškumo elgesio būdai:

| Režimas | Elgesys |
|---|---|
| Balų | Kiekvienas pasirinktas teisėjas išsiunčiamas **vienu metu**, be jokio ribojimo |
| Agentų | Pasirinkti agentai vykdomi **nuosekliai**, vienas `await` po kito |

Tad viena balų užklausa straipsniui su visais kriterijais sukuria 45
vienalaikius išeinančius LLM iškvietimus. Penkiasdešimt tokių užklausų — 2 250.

### 50 naudotojų pliūpsnis

Penkiasdešimt naudotojų, kiekvienas tą pačią sekundę paleidžiantis straipsnio
vertinimą (45 kriterijai, 40 000 simbolių dokumentas):

| Rodiklis | Reikšmė |
|---|---|
| Vienalaikių LLM iškvietimų | **2 250** |
| Įvesties tokenų per ~1 minutę | **~32 mln.** |
| Vienkartinė šio pliūpsnio kaina | **~85 USD** |

Tas pats pliūpsnis su ataskaitomis (8 kriterijai): 400 iškvietimų, ~5,7 mln.
tokenų, ~15 USD.

## Kliūtys

### Vienas egzempliorius, vienas įvykių ciklas { #vienas-egzempliorius }

`deploy.sh` diegia su `--max-instances 1`, `--cpu 2` ir `--memory 1Gi`, o
konteineryje veikia vienas Uvicorn procesas be `--workers`. Visas srautas
patenka į vieną įvykių ciklą, o horizontalus mastelio didinimas praktiškai
išjungtas, nors platforma jį palaiko. Atkreipkite dėmesį: repozitorijoje esantis
`service.yaml` nurodo `maxScale: 10` ir `2Gi` — abu failai nesutaria, o
`make deploy` paleidžia būtent `deploy.sh`. Žr. [Diegimas](deployment.md).

### Dokumento konvertavimas blokuoja įvykių ciklą { #blokuojantis-konvertavimas }

`DocumentService.convert_to_markdown()` yra `async` funkcija, tačiau pats
konvertavimas — sinchroninis iškvietimas:

```python
result = self.converter.convert(str(tmp_path))   # blokuoja, įvykių cikle
```

`markitdown`, analizuojantis DOCX ar PDF, yra apkrautas procesoriaus darbu ir
niekada neatiduoda valdymo. Kol jis vykdomas, **visas procesas neaptarnauja
nieko kito** — nei kitų naudotojų užklausų, nei konteinerio gyvumo tikrinimų.
Penkiasdešimt vienalaikių įkėlimų išsirikiuoja į eilę, o paslauga atrodo
užstrigusi.

Sprendimas — iškelti tai iš ciklo su `asyncio.to_thread()` arba paskelbti
maršrutą `def`, o ne `async def`, kad FastAPI leistų jį savo gijų telkinyje.

### 300 sekundžių užklausos limitas { #uzklausos-limitas }

Vertinimas vyksta **HTTP užklausos viduje**. Naršyklė laiko ryšį atvirą visą
vertinimo laiką; nėra nei darbų eilės, nei būsenos maršruto. `service.yaml`
nurodo `timeoutSeconds: 300`, kuris yra ir Cloud Run numatytoji reikšmė.

Pasiekus tą ribą, ryšys nutraukiamas ir **prarandamas visas rezultatas**,
įskaitant kiekvieną jau įvertintą kriterijų, nes daliniai rezultatai niekada
neįrašomi. Naudotojas mato nesėkmę, o už tokenus vis tiek sumokama.

### Neribotas teisėjų vienalaikiškumas { #neribotas-teiseju-vienalaikiskumas }

`Dataset.evaluate()` kviečiamas be `max_concurrency`, o pydantic-evals surenka
atvejo vertintojus be ribojimo, tad niekur nėra jokios išeinančių LLM
iškvietimų ribos. Nėra ir programos lygio semaforo.

`BATCH_EVALUATION_CONCURRENCY` nepadeda — tai tik CLI `--concurrency`
parametro numatytoji reikšmė, ir API jos niekada neklausia.

### Nėra pakartojimo prie greičio limitų { #nera-pakartojimo-prie-greicio-limitu }

2 250 vienalaikių iškvietimų ir ~32 mln. tokenų per minutę viršys bet kurio
OpenAI paskyros lygio minutines ribas. Kode nėra nei pakartojimo, nei
laipsniško atidėjimo.

Pasekmė blogesnė už klaidą, nes ji tyli: teisėjas, gavęs `429`,
užregistruojamas kaip nesėkmė, o **užklausa vis tiek grąžina
`status: "success"`**. Vienintelis signalas — `results.total_failures`.
Naudotojui dalinis vertinimas atrodo lygiai taip pat, kaip pilnas.

### Laikina failų saugykla { #laikina-saugykla }

`use_gcs` numatytai yra `false`, o `deploy.sh` nustato tik `ENV=production` —
tad įkelti failai rašomi į paties konteinerio failų sistemą. Perkrovus
egzempliorių jie prarandami ir nėra bendrinami tarp egzempliorių, o tai savo
ruožtu daro `--max-instances 1` reikšmingu: pakėlus jį neperėjus prie GCS,
užklausos keliautų į egzempliorius, kurie nemato vienas kito failų.

### Pasirengimas keliems naudotojams { #pasirengimas-keliems-naudotojams }

`Project` turi `user_id`, o `list_projects` pagal jį filtruoja, tad duomenų
modelis atskyrimą palaiko. Bet dauguma projektų maršrutų jo neužtikrina:
autentikuoto kvietėjo reikalauja tik `list_projects`, `create_project`,
`get_scores_grid`, `set_project_marked_good` ir `run_llm_detection`, o
`project.user_id` su juo lygina tik pastarieji du. `evaluate_version`,
`upload_version`, `get_project`, `delete_project` ir versijų maršrutai priima
neautentikuotas užklausas.

Su vienu naudotoju tai nematoma. Su 50 tai reiškia, kad naudotojai gali
pasiekti vieni kitų projektus, tad prieš bet kokį daugelio naudotojų paleidimą
tai būtina uždaryti.

## Ką pakeisti

1–6 punktai yra būtina sąlyga vienalaikiam naudojimui.

| Nr. | Pakeitimas | Sprendžia |
|---|---|---|
| 1 | **Perkelti vertinimą į foninį darbą.** Iš karto grąžinti vertinimo identifikatorių, leisti sąsajai apklausti būseną ir įrašyti kiekvieno kriterijaus rezultatą jam atėjus, kad laiko limitas negalėtų sunaikinti jau padaryto darbo | Užklausos limitas, vienas egzempliorius |
| 2 | **Apriboti vienalaikiškumą.** Perduoti `max_concurrency` į `Dataset.evaluate()` ir pridėti viso proceso semaforą, kad išeinantys iškvietimai niekada neviršytų paskyros ribų | Neribotas vienalaikiškumas |
| 3 | **Pakartoti su atidėjimu ir sušildyti podėlį.** Laipsniškas atidėjimas prie `429`/`5xx`; pirmą teisėjo iškvietimą leisti atskirai, kad likę pataikytų į užklausų podėlį — tai kartu nukerpa ~45 % kaštų | Greičio limitai, kaštai |
| 4 | **Suderinti ir pakelti diegimo ribas.** Vienas tiesos šaltinis `deploy.sh` ir `service.yaml`; pakelti `--max-instances`, pakelti atmintį, nustatyti `USE_GCS=true`, patvirtinti PostgreSQL | Vienas egzempliorius, laikina saugykla |
| 5 | **Iškelti konvertavimą iš įvykių ciklo** su `asyncio.to_thread()` | Blokuojantis konvertavimas |
| 6 | **Užtikrinti autentikaciją ir savininko tikrinimą** visuose projektų maršrutuose | Atskyrimas tarp naudotojų |
| 7 | **Užfiksuoti teisėjų modelį**, kad bibliotekos atnaujinimas negalėtų jo pakeisti | Korektiškumo rizika |
| 8 | **Įrašyti tokenų sąnaudas** kiekvienam vertinimui iš `result.usage()` | Kaštų matomumas, pakeičia įverčius |
| 9 | **Sutvarkyti kriterijų rinkinį** ir patikrinti pigesnį teisėjų modelį | Kaštai |

1–6 punktai yra įprastas darbas ant tvarkingos struktūros. Juos įgyvendinus, 50
naudotojų pliūpsnis tampa eile, kuri išsivalo tokiu tempu, kokį leidžia
teikėjas, o naudotojai laukia sąsajoje, ne atvirame ryšyje.

## Prieš tolesnį derinimą — išmatuokite

Trukmė gamyboje niekada nebuvo matuota — `evaluations` lentelė šio teksto
rašymo metu buvo tuščia, tad 5–15 sekundžių vienam teisėjo iškvietimui,
minimos puslapyje
[Modeliai ir tokenų kaštai](models-and-tokens.md#kas-neismatuota), yra
įvertinimas.

Logfire jau instrumentuoja FastAPI ir PydanticAI. Nustačius `LOGFIRE_TOKEN`,
įsijungia tikri kiekvieno iškvietimo laikai ir tokenų skaičiai — tai pigiausias
būdas pakeisti visus šių dviejų puslapių įverčius duomenimis.
