![Paveikslėlis, kuriame yra Šriftas, tekstas, Elektrinė mėlyna spalva, mėlynas  Automatiškai sugeneruotas aprašymas](data:image/png;base64...)

Mokslinių tyrimų veiklos Nr. [1.1] ataskaita

Projekto pavadinimas: Nurodyti projekto Nr.

Projekto numeris: 0X-0XX-X-XXX

Projekto vykdytojas: *UAB „Įmonė1“*

Projekto partneris/-iai: UAB „Įmonė2“ (jei yra)

Veiklos numeris: 1.1

Veiklos pavadinimas: **Optimalių komponentų parinkimas, sąveikos problemų sprendimų metodikos**

Ataskaitos data: 2025-05-30

Lapų skaičius: ***Nurodyti***

**Turinys**

[1. Veiklos tikslas 3](#_Toc389153652)

[2. Veiklos užduotys 3](#_Toc389153653)

[3. Mokslinis neapibrėžtumas 3](#_Toc389153654)

[4. Tyrimų metodika 3](#_Toc389153655)

[5. Tyrimo eiga 3](#_Toc389153656)

[6. Įvykdyti paslaugų pirkimai 3](#_Toc389153657)

[7. Užduočių atlikimas 4](#_Toc389153660)

[8. Pasiekti tyrimų rezultatai 4](#_Toc389153662)

[9. Nepasiekti tyrimų rezultatai 4](#_Toc389153663)

[10. Veiklos vykdymo metu atliktų tyrimų eigos pakeitimai 4](#_Toc389153664)

[11. Nauda projekto rezultatams 4](#_Toc389153665)

# Veiklos tikslas

(Tikslas vienu sakiniu)

**Veiklos tikslas** – Sukurti metodiką, kuri atsakytų kaip integravimo ir optimizavimo metodus pritaikyti skirtingiems hibridinio įrenginio komponentams, kad jie efektyviai veiktų kaip vientisas mechanizmas.

# Veiklos užduotys

Šiuo metu nėra žinomas modelis/metodika, kaip reikėtų integruoti ir apjungti į visumą įrenginio komponentus, kurie atlieka skirtingas funkcijas. Todėl reikalinga atlikti vystomo hibridinio įrenginio skirtingų komponentų parinkimą, aptarti jų integravimą, tarpusavio sąsajų nustatymą ir funkcionalumą, kad įrenginys veiktų efektyviai kaip vientisa sistema. Todėl šiam tikslui įgyvendinti buvo iškelti šie veiklos uždaviniai:

1. **Nustatyti, kokie yra pagrindiniai hibridinio įrenginio komponentai, jų savybės, reikalavimai ir galimi veikimo modeliai.**
2. **Išnagrinėti kiekvieno komponento funkcionavimą atskirai ir su kitais komponentais.**
3. **Sukurti matematinį ir/arba kompiuterinį modelį, kuris atspindės hibridinio įrenginio veikimą.**
4. **Sukurtame virtualiame modelyje pritaikyti skirtingus integravimo ir optimizavimo metodus, siekiant išsiaiškinti, kurie komponentai apjungti tarpusavyje veikia geriausiai.**

# Mokslinis neapibrėžtumas

Trumpai aprašyti veikloje tiriamą problematiką bei nurodyti esamus neapibrėžtumus, kas buvo nežinoma iki veiklos pradžios

Pastatų valdymo sistemos, dar vadinamos pastatų automatizavimo sistemomis (angl. *Building Management System*, BMS), skirtos palaikyti pastato funkcionalumui, tačiau dėl sparčios technologijų raidos, pastarųjų integracijos sudėtingumo ir kintančių vartotojų bei saugumo reikalavimų susiduria su visa eile problemų. Tai ir optimalaus architektūrinio sprendimo parinkimas (centralizuota ar decentralizuota architektūra), įvairių technologinių standartų ir protokolų suderinamumo klausimai, sistemos plėtros ir efektyvaus architektūros modifikavimo ribotumas, neapibrėžta dirbtinio intelekto modelių integracija, ypač vertinant energijos vartojimą ir prognozuojant jos poreikį, taip pat labai svarbus ir BMS sistemos kibernetinis atsparumas. Be išvardintų problemų egzistuoja ir jutiklių tikslumo ir duomenų vientisumo bei valdymo algoritmų ir jų optimizavimo problematika, taip pat ir gyventojų komforto ir jų tipinio elgesio neįvertinimas.

Panašaus pobūdžio problematika yra sprendžiama naujausiuose tyrimuose, kurie orientuojasi į pastatų valdymo ir automatizavimo sistemų (BAMS) ir intelektualiųjų pastatų (angl. *Smart Buildings*) architektūrų tobulinimą. BIM-to-BRICK metodika semantinei sąveikai užtikrinti siūlomas automatinis BIM (angl. *Building Information Modeling*) duomenų transformavimas į BRICK semantinį modelį, kuris leidžia efektyviau identifikuoti įrenginius ir jų funkcijas, užtikrinant automatinį topologijos ir funkcinių ryšių atvaizdavimą BMS sistemose [1]. Šis požiūris yra artimas dinaminio valdymo algoritmo sudarymo idėjai, nes remiasi automatiniu įrenginių atpažinimu ir priskyrimu valdymo struktūroms. IoT kaip atskirų modulių integracija į BMS/BAS išmaniuosiuose pastatuose rankinio konfigūravimo pagalba nagrinėjama [2]. Pabrėžiamas pilnai išvystytų PnP mechanizmų poreikis, kurie leistų naujus įrenginius dinamiškai įtraukti į sistemą be rankinių veiksmų [3,4].

Dabartiniai komerciniai pastatų automatikos sprendimai neturi funkcionalumo, kuris leistų realiu laiku automatiškai generuoti valdymo algoritmus pagal įrenginių paskirtį ir funkcijas. Dažniausiai šios sistemos remiasi rankiniu būdu sudaromais algoritmais, kuriuos kuria ir pritaiko inžinierius, o tai riboja sistemos gebėjimą greitai prisitaikyti prie kintančių sąlygų [3]. Ši problema tampa ypač akivaizdi diegiant sudėtingesnes pastatų automatikos sistemas, kuriose įrenginių skaičius ir funkcijų įvairovė sparčiai auga. Šiuolaikinės sistemos negeba integruoti semantinių duomenų struktūrų su automatizuotu valdymo logikos kūrimu [3]. 1 paveikslėlyje pavaizduota DevOps įrankių grandinė inžineriniams procesams paremti, kurioje tačiau neišvengiama rankinio darbo [3].

![Paveikslėlis, kuriame yra tekstas, ekrano kopija, Šriftas, diagrama  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

**1 pav.** DevOps įrankių grandinė [3]

Ši grandinė leidžia efektyviau organizuoti darbą, bet nesprendžia automatinio algoritmų generavimo uždavinio, todėl akivaizdus poreikis plėtoti programinės įrangos galimybes šioje srityje (1 pav.).

Semantinės duomenų integracijos modelyje 2 pav.) orientuojamasi į efektyvesnę informacijos struktūrą, tačiau pats valdymo algoritmų kūrimas tebėra paliktas operatoriui [3].

![Paveikslėlis, kuriame yra tekstas, Šriftas, ekrano kopija  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

**2 pav.** Semantinės integracijos modelis [3]

Šis modelis atskleidžia, kaip galima struktūruoti duomenis pastatų automatikos sistemoje, tačiau pateikta koncepcija nenumato realiu laiku automatiškai generuojamų algoritmų pagal įrenginių funkcines savybes (2 pav.). Tai tik patvirtina, kad vien semantinių modelių nepakanka — būtina kurti sudėtingesnes, platesnio funkcionalumo programines platformas.

Tad, nors semantinių duomenų modeliai ir dirbtinio intelekto metodai yra aktyviai tiriami, jų pritaikymas realiuoju laiku valdymo algoritmų generacijai komercinėse sistemose tebėra tik koncepcijos pateikimo lygmenyje.

Nors siūloma B-SMART architektūra koncepciniu lygmeniu numato autonominį įrenginių valdymą, tačiau svarstoma tik jos bendroji struktūra, o ne realiai veikianti automatinės algoritmų generacijos sistema 3 pav. a) [4]. Tai tik įrodo, kad praktikoje dar nepasiektas visiškas automatizacijos lygmuo, kuris leistų sistemoms pačioms generuoti valdymo logiką pagal įrenginių paskirtį. 3 paveikslėlyje (b)) pateiktos B-SMART architektūros pagrindu teoriškai galėtų būti realizuota autonominė algoritmų kūrimo sistema, tačiau praktinė komercinių produktų įgyvendinimo stadija tokio funkcionalumo dar neturi [4]. Ir tai tik išryškina atotrūkį tarp koncepcinių tyrimų rezultatų ir realių rinkoje esančių sprendimų.

![Paveikslėlis, kuriame yra tekstas, ekrano kopija, diagrama, Planas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

a)

![Paveikslėlis, kuriame yra tekstas, ekrano kopija, kvitas, Šriftas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

b)

**3 pav.** B-SMART architektūra: a) schema; b) struktūra [4]

Tad ši spraga lemia didelį rankinio darbo poreikį projektuojant, diegiant ir prižiūrint pastatų valdymo sistemas, o mokslinė bendruomenė šiuo metu siūlo konceptualius modelius, kurie galėtų šią problemą spręsti ateityje [3] [4].

Įdiegus semantinius aprašus į keitiklių programinę įrangą, galima užtikrinti, jog naujai aptikti įrenginiai dinamiškai būtų integruojami į bendrą valdymo logiką [3] [5]. „B‑SMART“ aprašo architektūrą autonominių pastato valdymo sistemų sukūrimui, kurioje valdymo ciklai generuojami realių duomenų pagrindu [3]. Ši architektūra iš esmės orientuota į dinamišką prisitaikymą, nes remiasi nuolat besimokančių sistemų principais, kurių dėka atpažįstami nauji įrenginiai ir savarankiškai koreguojamos valdymo strategijos. Tad, siekiant automatizacijos lygio, kuris užtikrintų valdymo algoritmų automatinį generavimą pagal įrenginių paskirtį ir funkcijas, tikslinga plėtoti programinės įrangos funkcionalumą, nes egzistuojantys sprendimai dažniausiai apsiriboja tik duomenų struktūrizavimu ir inžinerinių procesų palaikymu, bet nesudaro sąlygų visiškai autonominiam valdymo logikos kūrimui.

Semantinės ir ontologijomis paremtos sistemos daugiausia orientuotos į suderinamumo užtikrinimą tarp skirtingų įrenginių bei paslaugų [5] (4 pav.).

![Paveikslėlis, kuriame yra diagrama, tekstas, linija, Planas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

a)

![Paveikslėlis, kuriame yra tekstas, diagrama, linija, Planas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

b)

**4 pav**. a) Sąveika tarp IoT įrenginių ir paslaugų:

a) funkcinė schema; b) semantine sąveika ir ontologija grįsta schema [5]

Nors siūlomas sprendimas (4 pav., a)) ir sukuria sąlygas efektyvesniam įrenginių tarpusavio suderinamumui, tačiau neapima automatinio valdymo algoritmų kūrimo funkcijos (4 pav.) 4 paveikslėlyje (b) parodyta semantinė sąveika tarp IoT įrenginių ir paslaugų užtikrina informacijos keitimą, bet neapima valdymo logikos kūrimo proceso: sistema / architektūra užtikrina, kad įrenginiai ir paslaugos gali tarpusavyje bendrauti, t. y. dalintis duomenimis, suprasti vieni kitus per ***semantinius modelius*** ir ***ontologiją*** (pvz., temperatūros jutiklis gali perduoti reikšmę šildymo įrenginiui, nes abu supranta, ką ta reikšmė reiškia), tačiau pati sistema pagal gautą informaciją nenumato automatinio valdymo taisyklių ar algoritmų sukūrimo (pvz., ji nesukuria sprendimo, pvz., „jei temperatūra < 20 °C, įjunk šildymą“, nebent žmogus tą taisyklę apibrėžia rankiniu būdu). Tokia sistema labai pagerina duomenų perdavimą ir įrenginių tarpusavio komunikavimą, tačiau nesugeneruoja valdymo strategijos pagal įrenginio paskirtį (pvz., kad šildytuvai šildytų ar žaliuzės užsivertų nuo saulės), taip pat nekuria realiu laiku taisyklių ar algoritmų, kurie apimtų įrenginių logiką pagal situaciją. Tai tik dar kartą pabrėžia poreikį programinės įrangos funkcionalumo plėtrai. Todėl be papildomų programinių sprendimų neįmanoma pasiekti visiškos autonomijos.

Semantinės sąveikos tarp IoT įrenginių ir paslaugų modeliavimo efektyvumas, kurio įvesties parametrai IoT įrenginių skaičius 100–500, ryšio protokolai MQTT, CoAP, HTTP; duomenų formatai JSON, XML, CSV; apdorojimo sluoksniai Edge, Cloud, atskleidžiamas 5 paveikslėlyje [5] [6].

![Paveikslėlis, kuriame yra tekstas, ekrano kopija, diagrama, linija  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...) ![Paveikslėlis, kuriame yra tekstas, ekrano kopija, diagrama, linija  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

a) b)

**5 pav.** Semantinės sąveikos tarp IoT įrenginių modeliavimo rezultatai:

a) ryšio protokolai; b) apdorojimo sluoksniai [5]

Sistemos išteklių naudojimo efektyvumas lyginant lokalių įrenginių (angl. *Edge*) ir *debesijos* (angl. Cloud) sprendimus buvo analizuojamas tyrime [5]. Eksperimento metu buvo vertinama, kaip skiriasi atsako laikas tarp lokalių įrenginių ir *debesijos*, kai vykdomi semantinių paslaugų užklausų apdorojimai. Rezultatai parodė, kad lokalių įrenginių sprendimai užtikrina daug mažesnę delsą realaus laiko scenarijuose, nei *debesijos* sprendimai dėl tinklo sąlygojamų duomenų perdavimo trukmių bei duomenų apdorojimo proceso *debesijos* infrastruktūroje. Kraštinių įrenginių architektūros pranašumas ypač ryškus tada, kai būtinas greitas atsakas, pvz. realaus laiko valdymo ar saugos scenarijuose (5 pav. b)). Tyrimas taip pat parodė, kad abiem atvejais vis dar nerealizuotas automatinio valdymo logikos kūrimas [5].

Šiuolaikinės BAMS sistemos tampa vis sudėtingesnės dėl didėjančio įvairių įrenginių ir protokolų įvairovės (6 pav.).

![Paveikslėlis, kuriame yra tekstas, ekrano kopija, diagrama, dizainas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

a)![Paveikslėlis, kuriame yra tekstas, diagrama, ekrano kopija, Šriftas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

b)

**6 pav**. Semantinių skaitmeninių dvynių a) veikimo schema; b) ontologija [9]

Integruojant įvairių gamintojų įrenginius (pvz., HVAC, apšvietimo, saugos sistemas), tenka spręsti protokolų suderinamumo problemas (Modbus, BACnet, CAN, M-Bus ir kt.). Mašininio mokymosi priemonės, integruotos su semantine architektūra, suteikia galimybę ne tik atpažinti įrenginius, bet ir iš jų veikimo duomenų kurti optimalius valdymo algoritmus [6-8]. Vienas iš pažangių sprendimų yra semantinių skaitmeninių dvynių naudojimas [9], kuris remiasi dirbtiniu intelektu (DI), siekiant automatiškai aptikti ir apibūdinti įrenginius bei sudaryti jiems tinkamus valdymo algoritmus (6 pav.). Tokios sistemos leidžia efektyviau valdyti įvairių protokolų įrenginius, užtikrinti duomenų srauto standartizavimą bei informacijos išsaugojimą konvertuojant skirtingų protokolų duomenis į pasirinktą bendrą standartą. Tai suteikia galimybę dinamiškai adaptuoti BAMS, įvedus naujus komponentus be būtinybės iš anksto numatyti kiekvieno įrenginio integracijos žingsnius [10]. Tokio funkcionalumo įgyvendinimui būtinos DI paremtos architektūros, kuriose būtų integruotos *Discovery, Subscribe* i*r PnP* funkcijos, galinčios realiu laiku kurti valdymo objektus ir algoritmus pagal įrenginių funkcijas [10, 11]. Tad, būtina plėsti programinės įrangos funkcionalumą, apimantį ne tik duomenų suderinamumą, bet ir autonominį valdymo logikos kūrimą.

**Probleminės analizės apibendrinimas**

1. Atsižvelgus į tai, kadBMS sistemai būtinas lankstumas, atvirų standartų laikymasis bei adaptavimasis prie įvairių vidinių bei išorinių veiksnių, duomenų srauto standartizavimas yra pagrindinis tikslas, siekiant suderinti įvairių protokolų įrenginių sąveiką, kartu neprarandant informacijos ir užtikrinant sistemos lankstumą bei dinaminį prisitaikymą.
2. Lokalių sprendimų atsako laikas yra daug mažesnis lyginant su *debesijos* sprendimais, o tai patvirtina, kad skaičiavimo resursų paskirstymas arčiau valdomų įrenginių gali gerokai pagerinti visos sistemos efektyvumą. Tačiau, šuo metu tokiam resursų paskirstymui dažnai reikia rankinio derinimo, o tai riboja sistemų autonomiją. Tad, siekiant užtikrinti efektyvią sistemų veiklą, būtina ne tik pagerinti automatizavimo funkcionalumą, bet ir diegti išmaniuosius resursų skaičiavimo ir paskirstymo mechanizmus, kurie leistų dinamiškai valdyti apkrovą tarp įvairių skaičiavimo sluoksnių (lokalių ir *debesijos*).
3. Šiuolaikiniai komerciniai sprendimai neturi pakankamai pažangių funkcijų, todėl naujai kuriama sistema turi būti grindžiama automatizuotą integraciją palaikančiomis technologijomis ir kuri dinamiškai sudarytų valdymo algoritmus, leidžiančius automatiškai aptikti naujus įrenginius. Tradicinės keitiklių programinės įrangos architektūros yra ribotos, nes jos daugiausia skirtos rankiniam įrenginių konfigūravimui ir statiniam jų valdymo algoritmų sudarymui (esami protokolų keitikliai nenaudoja automatinių *subscribe, discovery, plug&play* funkcijų). Minėtų problemų sprendimui būtina šias funkcijas integruoti, įgyvendinant DI veikimu pagrįstą architektūrą. Naudojant semantines ontologijas, mašininį mokymąsi bei DI principais grįstą valdymą galima automatiškai atpažinti naujus įrenginius, generuoti jiems valdymo objektus bei algoritmus, taip sumažinant rankinio darbo apimtis ir galimus konfigūravimo netikslumus.
4. Dabartinių komercinių sprendimų programinė įranga neapima analizės modelių ar autonominių valdymo algoritmų sudarymo mechanizmų, todėl kyla būtinybė naujiems programiniams sprendimams, kurie užtikrintų pažangios dinaminės valdymo sistemos veikimą. Taip pat, nors dauguma sukurtų BMS sprendimų remiasi programinės įrangos naudojimu, kuri leidžia valdyti pastatų sistemas nuotoliu, tačiau, nėra įrenginio, kuris galėtų veikti nepriklausomai nuo Interneto ar *debesyse* esančios programinės įrangos ir kuris lanksčiai apimtų visus reikalingus protokolus visapusiškam pastato valdymui. Visa tai ir būtų pagrindinis kuriamo įrenginio išskirtinumas.

Išskiriami šie moksliniai neapibrėžtumai:

**Iš pirmojo uždavinio** (Nustatyti, kokie yra pagrindiniai hibridinio įrenginio komponentai, jų savybės, reikalavimai ir galimi veikimo modeliai**):**

1. kokie hibridinio įrenginio architektūriniai sprendimai realizuotų naujų BAS įrenginių automatinį atpažinimą, generuoti jiems valdymo objektus bei algoritmus, taip sumažinant rankinio darbo apimtis ir galimus konfigūravimo netikslumus?
2. kokie hibridinio įrenginio komponentų specifikaciniai reikalavimai leistų palaikyti semantinių duomenų modelius?

**Iš antrojo uždavinio** (Išnagrinėti kiekvieno komponento funkcionavimą atskirai ir su kitais komponentais)**:**

1. kaip realizuoti *stand alone* (kitaip, black box) principą, kad įrenginys gebėtų pilnavertiškai valdyti visas pastato sistemas, nutrūkus belaidžio Interneto ryšiui (ryšiui su ESE duomenų baze)? Kokiomis technologijomis realizuoti automatizuotą naujų įrenginių integraciją?
2. kaip užtikrinti įvairių pastato funkcionavimą palaikančių sistemų patikimą kontrolę?
3. kaip realizuoti black box išmaniąsias funkcijas(*subscribe, discovery, plug&play*), kurios bus paremtos protokolų keitikliais?

**Iš trečio uždavinio (**Sukurti matematinį ir/arba kompiuterinį modelį, aprašantį hibridinio įrenginio veikimą):

1) kiek jutiklių gali efektyviai aptarnauti hibridinis įrenginys arba koks turėtų būti jo užklausų dažnis, kuris užtikrintų optimalų duomenų surinkimą, neviršijant sisteminių resursų ribų?

2) kokio dydžio resursai turi būti parenkami apdorojančiame mazge bei ryšio magistralėje (koks jos pralaidumas), remiantis srauto vėlinimo parametru?

3) kokio pralaidumo *Ethernet* kanalo reikia tarp pagrindinio valdymo mazgo ir komutatoriaus?

**Iš ketvirtojo uždavinio (**Virtualiame modelyje taikyti skirtingus integravimo ir optimizavimo metodus, siekiant išsiaiškinti, kurie komponentai apjungti tarpusavyje veikia geriausiai)**:**

1. kokios spartos duomenų perdavimo magistralė turėtų būti naudojama, siekiant išvengti duomenų blokavimo?
2. kiek protokolų valdiklių būtina numatyti projektuojamame hibridiniame įrenginyje, siekiant užtikrinti reikiamas duomenų srauto apdorojimo charakteristikas?
3. kokią būtina parinkti protokolų valdiklio buferio talpą?

# Tyrimų metodika

1. Mokslinės literatūros ir dokumentikos skaitmeninių išteklių analizė, sisteminimas, lyginimas, interpretavimas ir apibendrinimas.
2. Teletrafiko teorijos principai bei sukuriamų paraiškų srautų apdorojimo analizės metodai, leidžiantys kiekybiškai įvertinti kiekvieno komponento įtaką bendrosioms duomenų srautų charakteristikoms (hibridinio įrenginio komponentų parametrizavimo uždavinys).
3. Imitacinis modeliavimas hibridinio įrenginio funkcionavimo įvertinimui.

# Tyrimo eiga

Aprašyti tyrimų eigą (atskleidžiant darbo procesą):

* kas analizuota, kokia apimtimi, kiek tyrimų, bandymų ar eksperimentų atlikta šios veiklos metu, kokie rezultatai pasiekti, ar įvykdytos visos užduotys, ar pasiektas veiklos tikslas, kaip buvo pasiekti užsibrėžti uždaviniai, kokius tarpinius veiksmus reikėjo atlikti. Aprašyti ir tuos veiksmus, kurie buvo atlikti, tačiau nedavė rezultato.

Rekomenduojama apimtis – iki 5 psl.

**1. Nustatyti, kokie yra pagrindiniai hibridinio įrenginio komponentai, jų savybės, reikalavimai ir galimi veikimo modeliai.**

Tam būtina išanalizuoti rinkoje esančius pastatų valdymo sistemos analogus. Taip pat tikslinga atlikti valdymo sistemų ir protokolų keitiklių bei visų reikalingų komponentų analizę bei sudaryti įrenginio koncepciją/struktūrinę schemą. Taip pat, atliekant šį uždavinį, tikslinga apžvelgti atskirų sistemų charakteristikas. Šio įrenginio paskirtis bei jo eksploataciniai reikalavimai atspindimi sudarytoje įrenginio specifikacijoje.

*Nagrinėjamas objektas* yra tipinės pastato valdymo (automatizacijos) sistemos (angl*. Building Automation Systems,* BAS), kurių pagrindinės sudedamosios dalys ir jų tarpusavio ryšys pateiktas 7 pav. Šiuo metu rinkoje naudojami skirtingi pastato valdymo sistemų valdikliai (angl. *Building Management System*, BMS), kurie valdo skirtingus pastato įrenginius (P1 pav. a). Dauguma šiuolaikinių rinkoje tiekiamų BMS valdiklių pagrindinės funkcijos yra realizuotos (veikia) debesyse. **Todėl yra atsiradęs poreikis, kad esant interneto trikdžiams, ar visai nesant internetinio ryšio BMS sistemos galėtų valdyti įvairius išorinius elementus.**

*Kuriamas valdiklis* automatiškai valdytų pastato įrenginius bei valdytų įrenginių suvartojamą energiją, juos išjungiant ar įjungiant pagal užduotą algoritmą. *Pagrindinis tikslas* **savarankiškai ir izoliuotai valdyti įrenginius be interneto ryšio** (7 pav. b.), interneto ryšys naudojamas paimti /

![Paveikslėlis, kuriame yra tekstas, apskritimas, animacija, Šriftas  Dirbtinio intelekto sugeneruotas turinys gali būti neteisingas.](data:image/png;base64...)

a) b)

7 pav. Pastato valdymo (automatizacijos) sistemos architektūra: esamos sistemos, b) kuriama sistema

pateikti reikiamą informaciją į / iš ESE (centrinė renkamos informacijos sistema debesyse), valdymas taip pat bus pateikiamas kaip debesijos paslauga. Įrenginys sektų Nordpool prognozes: kadangi tai mokama paslauga, todėl visi duomenys iš pradžių keliautų į ESE, o iš jo būtų perduodami kuriamam įrenginiui. ESE analizuotų Nordpool prognozes ir **dinamiškai sudarytų valdymo algoritmus automatiškai aptinkamiems naujiems sistemos įrenginiams,** *kas**yra kuriamo įrenginio naujumas*. Kuriamas įrenginys valdo pagrindines pastato sistemas kaip šildymas/šaldymas, apšvietimas, apsauga, generuojamos energijos kaupimas ir paskirstymas ir kt. Įrenginys taupys elektros energiją, nes bus kontroliuojamas energijos suvartojimas įvairiuose pastato elementuose, atsižvelgiant į elektros kainą rinkoje. Visų BMS valdiklių visuma bus apjungta viename įrenginyje. Kuriamas įrenginys apima visas BMS valdiklių funkcijas ir gali veikti izoliuotai, t. y. savarankiškai be interneto (7 pav. b.).

Pastato valdymo sistemų (BMS) gamintojai siūlo platų valdiklių spektrą, skirtą įvairioms pastato inžinerinėms sistemoms valdyti ir integruoti (1.1 lentelė). Vieni iš lyderiaujančių gamintojų pasaulyje yra Siemens, Schneider Electric, Honeywell, Johnson Controls, Tridium (Niagara Framework), ABB, Delta Controls ir kt. Šių gamintojų valdikliai pasižymi universalumu, atvirų komunikacijos protokolų palaikymu ir galimybe integruotis su debesijos platformomis.

L1 lentelė: Komunikacijos protokolai pagal gamintojus ir sistemas

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Gamintojas** | **Baterijų krovimas** | **Išmanūs skaitikliai** | **Šildymo sistemos** | **Apšvietimo sistemos** | **Apsauga / praėjimas** | **Gaisro apsauga** | **Vėdinimas / rekuperacija** |
| **Siemens** | Modbus, BACnet, CAN | Modbus, M-Bus, CAN | BACnet, Modbus, CAN | DALI, BACnet | BACnet, CAN | BACnet | BACnet, Modbus, CAN |
| **Schneider Electric** | Modbus, BACnet, CAN | Modbus, M-Bus, CAN | BACnet, Modbus, CAN | DALI, BACnet | BACnet, Modbus, CAN | BACnet, Modbus | BACnet, Modbus, CAN |
| **Honeywell** | Modbus, BACnet, CAN | Modbus, M-Bus, CAN | BACnet, CAN | BACnet, DALI | BACnet, Modbus, CAN | BACnet | BACnet, CAN |
| **Johnson Controls** | BACnet, Modbus, CAN | BACnet, M-Bus, CAN | BACnet, CAN | BACnet, DALI | BACnet, Modbus, CAN | BACnet | BACnet, CAN |
| **ABB** | Modbus, CAN | Modbus, M-Bus, CAN | Modbus, CAN | DALI | CAN | Modbus | Modbus, CAN |
| **Tridium (Niagara)** | Modbus, BACnet, CAN | Modbus, M-Bus, CAN | BACnet, CAN | BACnet, DALI | BACnet, Modbus, CAN | BACnet | BACnet, CAN |
| **Delta Controls** | BACnet, CAN | BACnet, CAN | BACnet, CAN | BACnet, DALI | BACnet, CAN | BACnet | BACnet, CAN |

**Baterijų krovimo valdymas:** dažniausiai realizuojamas su integruotais energijos valdymo valdikliais. Siemens (pvz., Desigo CC platforma), Schneider Electric (EcoStruxure Power), ir ABB (Ability Energy Manager) siūlo sprendimus, leidžiančius stebėti akumuliatorių būklę, valdyti krovimo / iškrovimo procesus ir optimizuoti energijos srautus.

**Išmanūs skaitikliai:** integruojami į BMS siekiant realiu laiku stebėti energijos, vandens ar kitų resursų suvartojimą. Siemens, Schneider Electric, ABB ir Honeywell siūlo išmaniųjų skaitiklių sprendimus, kurie perduoda duomenis į valdymo sistemas per Modbus, M-Bus, BACnet ar kitus protokolus. Šie sprendimai padeda optimizuoti energijos sąnaudas, identifikuoti nuostolius ir užtikrinti tikslų atsiskaitymą.

**Šildymo sistemos:** valdymui Honeywell, Johnson Controls ir Siemens siūlo pažangius HVAC valdiklius. Šie įrenginiai palaiko zoninį reguliavimą, šilumos punktų valdymą ir sąveiką su termomodernizacijos sprendimais.

**Apšvietimo sistemos:** integruojamos naudojant valdiklius, galinčius dirbti su DALI, KNX ar BACnet. Schneider Electric (SpaceLogic), ABB (i-bus KNX) ir Siemens (GAMMA Instabus) produktai užtikrina lankstų ir energiją taupantį apšvietimo valdymą, įskaitant scenarijų kūrimą ir automatinį pritaikymą prie natūralios šviesos.

**Apsaugos ir praėjimo kontrolės sistemos:** dažniausiai diegiamos naudojant Honeywell (Pro-Watch), Johnson Controls (C CURE), ir Siemens (SiPass) sprendimus. Šios sistemos suderinamos su pastato BMS ir užtikrina tiek apsaugos įrenginių valdymą, tiek duomenų mainus su kitomis pastato sistemomis.

**Gaisro apsaugos sistemos:** valdymui dominuoja Siemens (Cerberus PRO), Honeywell (Notifier, Esser) ir Johnson Controls (Simplex) sprendimai. Šios sistemos dažnai naudoja adresinius detektorius ir sąveikauja su BMS platformomis per BACnet ar Modbus.

**Ventiliacijos ir rekuperacijos sistemos:** daugiausia valdomos Siemens, Johnson Controls ir Honeywell HVAC valdikliais. Jie užtikrina oro kokybės, srautų ir energijos efektyvumo kontrolę, dažnai integruojami į bendrą energijos valdymo sistemą.

**Valdymo debesijos sprendimai:** didieji BMS gamintojai siūlo debesijos sprendimus, leidžiančius centralizuotai stebėti, valdyti ir optimizuoti pastato inžinerines sistemas. Schneider Electric EcoStruxure suteikia prieigą prie energijos suvartojimo analizės, įrangos būklės stebėsenos ir įspėjimų apie trikdžius. Siemens Desigo CC Cloud siūlo nuotolinę priežiūrą, analitinius įrankius ir integraciją su dirbtinio intelekto sprendimais, skirtais energijos optimizavimui. Honeywell Forge platforma orientuojasi į didelių objektų valdymą, siūlydama skalę pramonės ir komercinių pastatų segmentams. Johnson Controls OpenBlue debesijos sprendimas suteikia galimybę kurti skaitmeninius pastato dvynius ir valdyti energijos efektyvumą realiu laiku. Šie debesijos sprendimai dažniausiai naudoja šifruotus ryšio kanalus ir API sąsajas integracijai su kitomis BAS sistemomis.

**L2 lentelė:** Valdiklių, keitiklių ir įrenginių matrica pagal gamintojus ir komunikacinius protokolus

|  |  |  |  |
| --- | --- | --- | --- |
| **Sistema** | **Valdiklis**  **(protokolas)** | **Keitiklis**  **(protokolas)** | **Įrenginys**  **(protokolas)** |
| **Baterijų krovimas** | Schneider SmartX MP-C  (BACnet, Modbus) | HMS Anybus Modbus TCP ↔ CANopen gateway | Victron Quattro inverter (CANopen) |
| **Išmanūs skaitikliai** | Siemens Desigo PX  (BACnet/IP) | Phoenix Contact EEM-MA600 M-Bus ↔ Modbus | Kamstrup Multical 603  (M-Bus) |
| **Šildymo sistemos** | Johnson FX-PCG  (BACnet MS/TP, Modbus) | HMS Anybus Modbus ↔ CAN gateway | Wilo Stratos MAXO siurblys  (CAN) |
| **Apšvietimo sistemos** | Tridium JACE 8000  (BACnet, Modbus) | Helvar DIGIDIM 910 DALI ↔ BACnet Ethernet | Philips DALI LED driver  (DALI) |
| **Apsauga / praėjimo kontrolė** | Schneider EcoStruxure Automation Server  (BACnet/IP) | HMS Anybus BACnet ↔ CANopen gateway | HID VertX V2000  (CAN) |
| **Gaisro apsaugos sistemos** | Honeywell XLS3000  (BACnet/IP) | nereikalingas (tiesioginė BACnet integracija) | Honeywell gaisro detektoriai  (BACnet) |
| **Ventiliacija / rekuperacija** | Siemens Climatix POL904  (BACnet MS/TP, Modbus) | HMS Anybus Modbus ↔ CAN gateway | Systemair Topvex  (CAN) |

Pagrindiniai BMS gamintojai siūlo universalius sprendimus, kurie palaiko atvirus komunikacijos protokolus, leidžiančius integruoti skirtingų gamintojų įrangą. Modbus ir BACnet dominuoja kaip pagrindiniai protokolai, o M-Bus, CAN ir DALI naudojami specifinėms pastato sistemoms (apskaitai, apšvietimui, HVAC). Debesijos sprendimai tampa standartine BMS dalimi, suteikdami galimybę nuotoliniu būdu valdyti sistemas, analizuoti duomenis ir didinti pastatų energinį efektyvumą. Apibendrinus L1 ir L2 lenteles, galime matyti, kad pastato valdymo sistemos naudoja įvairius komunikacijos protokolus, todėl **sklandžiai integracijai yra būtini protokolų keitikliai (**pavyzdinė (P1 pav. a) sistema galėtų būti sudaryta iš komponentų, pateiktų L2 lentelėje):

**Valdikliai:**

* Schneider Electric SmartX MP-C – išmanus pastatų automatikos valdiklis, skirtas šildymo, vėdinimo, oro kondicionavimo ir kitų pastato inžinerinių sistemų valdymui. Palaikomi protokolai: BACnet MS/TP, BACnet/IP, Modbus TCP, paskirtis: patalpų klimato kontrolė, energijos valdymas, integracija su kitomis sistemomis.
* Siemens Desigo PX – modulinis BMS valdiklis su stipria BACnet integracija, tinkamas didelėms pastatų sistemoms. Palaikomi protokolai: BACnet/IP, Modbus (per priedus), paskirtis: energijos valdymas, šildymas, vėdinimas, apšvietimas, apsauga.
* Johnson Controls FX-PCG – lankstus valdiklis, skirtas patalpų ir įrangos kontrolei. Palaikomi protokolai: BACnet MS/TP, Modbus, paskirtis: HVAC įrangos valdymas, siurblių, vožtuvų, ventiliatorių kontrolė.
* Tridium JACE 8000 –atvira platforma su Niagara Framework, skirta integruoti įvairias pastato sistemas. Palaikomi protokolai: BACnet, Modbus, SNMP, LON, DALI (per papildinius), paskirtis: universalus tinklų, pastato sistemų integratorius.
* Schneider EcoStruxure Automation Server – pastato automatikos serveris, skirtas integruoti įvairias BMS funkcijas vienoje platformoje. Palaikomi protokolai: BACnet/IP, Modbus TCP, LonWorks (priedai), paskirtis: bendras sistemų valdymas ir monitoringas.
* Honeywell XLS3000 – pažangus gaisro apsaugos valdiklis su BACnet integracija. Palaikomi protokolai: BACnet/IP, paskirtis: gaisro signalizacijos sistema, tiesioginis ryšys su BMS.
* Siemens Climatix POL904 – valdiklis skirtas HVAC įrangos kontrolei, palaiko išorinę komunikaciją. Palaikomi protokolai: BACnet MS/TP, Modbus RTU/TCP, paskirtis: šildymo, vėdinimo, rekuperacijos sistemų valdymas.

**Protokolų keitikliai:**

* HMS Anybus X-gateway – universalūs keitikliai, leidžiantys integruoti skirtingus pramoninius protokolus. Galimi variantai: Modbus ↔ CANopen, BACnet ↔ CANopen, Modbus ↔ CAN, paskirtis: ryšio tiltas tarp skirtingų protokolų (Modbus, BACnet, CAN magistralės).
* Phoenix Contact EEM-MA600 –keitiklis, skirtas surinkti duomenis iš M-Bus skaitiklių ir perduoti į Modbus tinklą. Palaikomi protokolai: M-Bus (slave), Modbus TCP/RTU (master), paskirtis: energijos skaitiklių duomenų surinkimas.
* Helvar DIGIDIM 910 router – DALI apšvietimo valdymo tinklo maršrutizatorius su BACnet integracija. Palaikomi protokolai: DALI, BACnet/IP, paskirtis: apšvietimo kontrolė, ryšys tarp BMS ir DALI šviestuvų.

**Įrenginiai:**

* Victron Energy Quattro inverter/charger – inverteris/įkroviklis su CAN sąsaja, skirtas sudėtingoms akumuliatorių sistemoms. Paskirtis: baterijų įkrovimas, energijos srautų valdymas hibridinėse sistemose.
* Kamstrup Multical 603 – šilumos skaitiklis su M-Bus ryšiu. Paskirtis: šilumos suvartojimo matavimas, duomenų perdavimas.
* Wilo Stratos MAXO – išmanus siurblys su integruota CAN magistralės sąsaja. Paskirtis: šildymo ir vėsinimo sistemų hidraulinis valdymas.
* Philips DALI LED driver – LED šviestuvų maitinimo blokas su DALI valdymu. Paskirtis: apšvietimo valdymas (šviesos intensyvumo reguliavimas).
* HID VertX V2000 – Praėjimo kontrolės modulis su CAN ryšiu. Paskirtis: praėjimo punktų ir durų užraktų valdymas.
* Honeywell gaisro detektoriai – prie BACnet tinklo jungiami detektoriai. Paskirtis: gaisro signalizacijos informacijos perdavimas.
* Systemair Topvex – rekuperacijos įrenginys su CAN ryšiu. Paskirtis: vėdinimas ir rekuperacija.

Siekiant įvertinti sistemos sudėtingumą ir integracijos kaštus, atliekama analizė, kuri pagal sprendinių struktūrą (valdiklis → keitiklis → įrenginys) ir naudojamus protokolus sprendžia kiekskirtingų programinių sprendimų / platformų reikėtų valdyti šiai sistemai:

* **Pastato valdymo pagrindinė platforma (BMS)** – tai valdymo sistema, jungianti visus BACnet, Modbus protokolą. Ši platforma centralizuotai surenka, apdoroja ir vizualizuoja duomenis. Galimi variantai:
  + Tridium Niagara Framework (pvz., su JACE 8000)
  + Schneider EcoStruxure Building Operation
  + Siemens Desigo CC
* **Protokolų keitiklių konfigūravimo įrankiai** – kiekvienam keitikliui reikės savo konfigūravimo programinės įrangos, skirta sukonfigūruoti ryšio parametrus tarp valdiklių ir įrenginių.:
  + HMS Anybus Configuration Manager
  + Phoenix Contact M-Bus konfiguratorius
  + Helvar Toolbox / Designer (DALI tinklams)
* **Specializuotų įrenginių valdymo ir monitoringo programos** – kai kurie įrenginiai turi savo sąsajas / programinę įrangą, naudojama įrenginių stebėsenai, parametrų derinimui, aparinės programinės įrangos (angl. firmware) atnaujinimams:
  + Victron VRM Portal / VictronConnect (baterijų sistemoms)
  + HID VertX NGC programinė įranga (praėjimo kontrolei)
  + Systemair Connect (rekuperacijos įrenginiui)
* **Gaisro sistemos konfigūravimo programinė įranga** – skirta gaisro aptikimo logikai, zonų ir prietaisų nustatymams konfigūruoti:
  + Honeywell XLS-CAB Configurator
* **Cloud platformos / nuotolinio valdymo sprendimai** –valdyti nuotoliniu būdu arba naudoti debesijos analizę:
  + EcoStruxure Building Advisor (Schneider)
  + Niagara Cloud Suite
  + Desigo CC Cloud (Siemens)
* **Papildomas programinis sprendimas** energijos analizėms, nuotoliniam monitoringui.

Įvertinus rinkos analogus pagal jų galimybes užtikrinti sudarytoje įrenginio specifikacijoje nurodytas charakteristikas, pasiūloma projektuojamo hibridinio įrenginio principinė schema (8 pav.), apimanti tiek funkcinius hibridinio įrenginio blokus, jų paskirtį, tiek ir jų tarpusavio ryšius.

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)

**8 pav.** Principinė hibridinio įrenginio schema

**Pagrindiniai reikalavimai kuriant pastato valdymo sistemą:**

1. **Lankstumas.** Modulinė struktūra sukonfigūruojama pagal kliento poreikius ir pritaikoma individualiam vartotojui su galimybė išplėsti protokolo taškų skaičių pagal poreikius.
2. **Universalumas.** Turi tikti visiems vienos linijos prietaisams, t. y. visiems pasirinkto protokolo prietaisams ar vieno tipo prietaisams. Tokiu būdu neprisirišama prie konkretaus modelio ar konkrečios kompanijos modulių linijos. Visi unikalūs valdikliai lieka išorėje.
3. **Plug-and-play (PnP) modelis.** Galimybė automatiškai prijungti išorinius prietaisus, modulius ir valdiklius, kurių parametrai yra iš anksto surašyti kuriamo įrenginio kompiuterio duomenų bazėje arba yra parenkami/pritaikomi pagal įrenginio atliekamas funkcijas.
4. **Suderinamumas**. Naujo komponento jungimas nedaro reikšmingos įtakos ir sistemai nesukleipia sistemos veikimo sutrikimo ir nereikalauja esminio sistemos perkonfigūravimo.

Sistema, sudaryta iš skirtingų valdiklių, keitiklių ir įrenginių, nors funkcionaliai apimtų visas reikiamas pastato inžinerines sistemas, tik iš dalies atitinka pagrindinius reikalavimus valdymo sistemai, nes:

1. **Sistema nėra lanksti**: dėl skirtingų gamintojų įrangos ir daug skirtingų protokolų reikia specifinių keitiklių ir programinės įrangos kiekvienam komponentui konfigūruoti. Modulinė struktūra tokiu atveju tampa fragmentuota, o bet kokia plėtra (pvz., protokolo taškų ar prietaisų papildymas) reikalauja naujų keitiklių arba atskirų sprendimų derinimo, o ne paprasto modulio pridėjimo prie bendros sistemos.
2. **Sistemos universalumas** stipriai priklauso nuo konkrečių gamintojų komponentų ir jų protokolų: kiekvienas įrenginys (pvz., siurblys, gaisro detektorius ar inverteris) dažnai reikalauja specifinio valdiklio arba keitiklio, tad nesusiformuoja vieninga „vienos linijos“ architektūra, kurioje visi įrenginiai būtų keičiami ar papildomi nepriklausomai nuo gamintojo. Tai reiškia, kad įsigijus ar integruojant kitų tiekėjų įrangą, sistemos pritaikymas tampa sudėtingas ir brangus.
3. **Sistema neatitinka Plug-and-play (PnP) principo**: naujų įrenginių prijungimas reikalauja rankinio konfigūravimo, specifinės programinės įrangos ir suderinimo veiksmų. Nėra galimybės, kad įrenginiai būtų automatiškai atpažįstami ir integruojami į sistemą pagal iš anksto apibrėžtus šablonus ar funkcijas.
4. **Sistema neužtikrina reikalaujamo suderinamumo**: naujo komponento jungimas gali turėti reikšmingos įtakos visos sistemos veikimui, sukelti veikimo sutrikimus ar reikalauti esminio sistemos perkonfigūravimo. Dėl daugybės skirtingų protokolų ir keitiklių kiekvienas pakeitimas sistemoje tampa jautrus ir reikalauja papildomų suderinimo darbų. Tai sumažina sistemos patikimumą ir apsunkina jos administravimą. Taip pat tokia heterogeninė sistema negali užtikrinti esminių reikalavimų, keliamų pažangioms valdymo platformoms - ***dinamiškai sudaryti valdymo algoritmus automatiškai aptinkamiems naujiems sistemos įrenginiams***. Ši funkcija yra esminė, nes jos dėka būtų galima savarankiškai atpažinti naujus komponentus, juos integruoti į bendrą valdymo struktūrą ir užtikrinti sklandų jų veikimą be sudėtingo rankinio konfigūravimo ar perprogramavimo.

Todėl siūloma pasirinkti pagrindinius protokolus – BACnet, Modbus, M-Bus, CAN ar DALI –kaip centrinę komunikacinę ašį kuriamame įrenginyje. Šiuo metu nėra galutinai žinoma, kuris protokolas tinkamiausias įgyvendinti Discovery, Subscribe ir PnP funkcijas, kurios būtinos, kad sistema galėtų automatiškai atpažinti naujus prietaisus ir dinamiškai sudaryti jiems pritaikytus valdymo algoritmus. Tokia analizė turi apimti kiekvieno protokolo galimybes palaikyti duomenų srauto standartizavimą, užtikrinti duomenų vientisumą konvertuojant tarp skirtingų protokolų ir realiu laiku kurti naujus valdymo scenarijus pagal aptiktų įrenginių funkcijas.

Preliminariai galima teigti, kad BACnet turi daugiausia potencialo dėl savo objektinio modelio, prenumeratos galimybių ir atviros architektūros, tačiau šis pasirinkimas turi būti pagrįstas išsamiais tyrimų ir praktinių bandymų rezultatais.

Tam, kad būtų įgyvendinta dinaminė sistema, keitiklių programinėje įrangoje turi būti įdiegtos naujos **Discovery**, **Subscribe** ir **PnP** funkcijos, galinčios automatiškai identifikuoti įrenginius ir sukurti jiems tinkamus valdymo objektus ir algoritmus.

Esama keitiklių programinė įranga šiandien šio tikslo pasiekti negali, nes ji neturi mechanizmų automatiškai kurti naujų objektų ir pritaikyti valdymo algoritmus pagal įrenginių funkcijas realiu laiku. Todėl būtina kurti naujus programinius sprendimus, kurie užtikrintų duomenų srauto standartizavimą, konvertavimą į pasirinktą pagrindinį protokolą (potencialiai BACnet) neprarandant informacijos ir užtikrinant, kad kiekvienam naujam įrenginiui būtų automatiškai sudaromi valdymo algoritmai pagal jo savybes ir funkcijas. Tik tokiu keliu galima pasiekti tikros pažangios valdymo sistemos viziją, atitinkančią modernius pastatų valdymo reikalavimus

**Kuriamas hibridinis įrenginys išlaiko pagrindinius reikalavimus kuriant pastato valdymo sistemas ir praplečia pastato valdymo sistemos funkcionalumą:**

1. **Lankstumas.** Modulinė struktūra sukonfigūruojama pagal kliento poreikius ir pritaikoma individualiam vartotojui su galimybė išplėsti protokolo taškų skaičių pagal poreikius.
2. **Universalumas.** Turi tikti visiems vienos linijos prietaisams, t. y. visiems pasirinkto protokolo prietaisams ar vieno tipo prietaisams. Tokiu būdu neprisirišama prie konkretaus modelio ar konkrečios kompanijos modulių linijos. Visi unikalūs valdikliai lieka išorėje.
3. **Plug-and-play (PnP) modelis.** Galimybė automatiškai prijungti išorinius prietaisus, modulius ir valdiklius, kurių parametrai yra iš anksto surašyti kuriamo įrenginio kompiuterio duomenų bazėje arba yra parenkami/pritaikomi pagal įrenginio atliekamas funkcijas.
4. **Suderinamumas**. Naujo komponento jungimas nedaro reikšmingos įtakos ir sistemai nesukleipia sistemos veikimo sutrikimo ir nereikalauja esminio sistemos perkonfigūravimo.
5. **Duomenų srauto standartizavimas**. Galimybė skirtingų protokolų duomenis konvertuoti į vieną (pagrindinį) komunikacinį protokolą, neprarandant informacijos, kas leis lanksčiau integruoti kuriamą įrenginį į esamas pastato valdymo sistemas.
6. **Apima visas BMS valdiklių funkcijas.** Kuriamas įrenginys panaikina poreikį sistemą sudaryti iš skirtingų gamintojų BMS, kas centralizuoja ir unifikuoja valdymo ir konfigūravimo programinę įrangą.
7. **Dinaminė konfigūracija.** Įrenginys sudarytų valdymo algoritmus automatiškai aptinkamiems naujiems sistemos įrenginiams.
8. **Gali veikti izoliuotai.** Turi valdymo algoritmus ir scenarijų šablonus, todėl gali funkcionuoti savarankiškai be interneto ryšio.

Esminis kuriamo įrenginio naujumas tai **duomenų srauto standartizavimas, dinaminė konfigūracija ir galimybė veikti izoliuotai –** tai funkcijos kurių trūksta daugeliui esamų BMS / BAS sprendimų. Ši funkcija leidžia skirtingų protokolų (pvz., Modbus, BACnet, M-Bus, CAN, DALI) duomenis konvertuoti į pasirinktą pagrindinį komunikacinį protokolą be informacijos praradimo, taip užtikrinant sklandų ir patikimą skirtingų sistemų tarpusavio bendradarbiavimą (8 pav.). Tokia galimybė ženkliai sumažina integracijos kaštus ir klaidų riziką, nes duomenys yra vienodai apdorojami ir atvaizduojami nepriklausomai nuo jų pradinio šaltinio. Kuriamas įrenginys automatiškai aptinka naujus sistemos komponentus ir sudaro jiems pritaikytus valdymo algoritmus ir scenarijus. Tai reiškia, kad sistema sugeba savarankiškai prisitaikyti prie naujų įrenginių įdiegimo realiu laiku, be papildomos rankinės konfigūracijos. Toks gebėjimas šiuo metu nėra būdingas standartiniams BMS/BAS, kurie dažniausiai reikalauja sudėtingo rankinio įrenginių įvedimo ir algoritmų sudarymo, nepriklausomai nuo interneto ryšio ar išorinių serverių. Jame integruoti valdymo algoritmai ir scenarijų šablonai užtikrina pastato inžinerinių sistemų funkcionavimą net ir nutraukus ryšį su debesijos paslaugomis. Ši savybė suteikia sistemos veiklai patikimumo ir saugumo kritinėse situacijose, kai būtina užtikrinti nenutrūkstamą pastato inžinerinių sistemų darbą.

Įrenginys iš esmės **centralizuoja BMS funkcijas**, nes apjungia visų valdiklių darbą į vieningą programinės įrangos aplinką. Tai eliminuoja poreikį naudoti skirtingų gamintojų BMS sprendimus, kurie dažnai apsunkina integraciją dėl tarpusavyje nesuderinamų valdymo ir konfigūravimo įrankių. Visa valdymo logika ir konfigūravimas vykdomi per vieną platformą, todėl sumažinamas administravimo sudėtingumas ir klaidų tikimybė. Apibendrinant galima teigti, kad kuriamas įrenginys ženkliai pranoksta tradicinius BMS / BAS sprendimus, nes siūlo centralizuotą, lankstų, savarankišką ir dinamiškai prisitaikantį valdymo sprendimą, kuris atveria naujas galimybes efektyviai ir patikimai valdyti modernius pastatus.

Įrenginio komponentai (8 pav.): pagrindinis kompiuteris/valdiklis, tinklo analizatorius ND30BAC, protokolų keitikliai (MODBUS/BACNet, DALI/BACNet, M-BUS/BACNet, BACNet/CAN), išmanaus pastato kontroleris ISMA-B-MIX18-IP, ABB galios komutatorius OTM63F4C21D400C, vidinė rezervinė galios baterija QUINT4-CAP/24DC/10/8KJ, du maitinimo šaltiniai +24V STEP3-PS/1AC/24DC/Į/PT, USB jungtis, skirta programuoti ESP32, naudojant Arduino IDE. Pusinio dupleksinio ryšio RS485 prievadas. Integruota EEPROM mikroschema duomenų saugojimui. Dvi programuojamos LED indikacijos. (Tx ir Rx LED) Pasirenkamas RS485 siųstuvo-imtuvo įtampos lygis. (5 V ir 3,3 V) Pramoninis korpusas su DIN tvirtinimu ir kompaktišku PCB dydžiu. Didžiausia darbinė įtampa Un 415 V (AC), nominali ilgalaikė srovė In 63 A, nominali trumpalaikė srovė 2.5 kA, apsaugos klasė IP20, ilgis – 131 mm, plotis – 283 mm, aukštis – 103 mm, svoris – 2,11 kg. Pagal realią srovę konkrečiame pastate šį perjungiklį galima pakeisti su didesne In (125, 200, 400). Šis perjungiklis palaiko BACnet protokolą.

Įrenginys turi galimybę matuoti sroves ir energijos srautus bei jų pagrindu vertinti sistemos efektyvumą. Siekiant nustatyti hibridinio įrenginio pagrindinių komponentų integracijos įrenginyje lygmenį, buvo tikslinga įvertinti inverterių panaudojimo klausimą.

Kuriamas įrenginys taip pat gali apimti vieną pagrindinių saulės elektrinių funkcijų - įtampos tipo keitimą. Paprastai šią funkciją atlieka inverteriai, kurie sumontuojami kartu su kitais elektrinės elementais statybos metu. Inverterių kiekis ir galia gali būti labai įvairūs, nes statomų elektrinių galia skiriasi nuo kelių kW iki kelių MW. Taip pat, vykstant elektros konvertavimui, išsiskiria dideli šilumos kiekiai. Iki 5 % nuo konvertuojamos galios pavirsta šilumos nuostoliais. Montuojant inverterį kuriamo prietaiso viduje, tampa neapibrėžti jo išoriniai matmenys, taip pat atsiranda aušinimo poreikis, kuris pagrįstas žemiau pateiktais skaičiavimais.

Priimama, kad iki 2 % procentų inverterio turimos galios pavirsta šilumos nuostoliais, tad naudojant 120 kW inverterį, išsiskiria apie 2,4 kW šilumos (1):

![A black background with letters  AI-generated content may be incorrect.](data:image/png;base64...) (1)

čia *Rth –* šiluminė varža, [K/W], kuri susideda iš šilumos laidumo ir konvekcijos, where *q* – šilumos srautas statmenas jos paviršiui *A*, [W], *T* – temperatūra [K].

Bendrai šiluminei varžai reikia įvertinti korpuso ir patalpos temperatūrą. Dažniausiai elektronikos prietaisų korpuso temperatūra neturi viršyti 40-45 °C, tam, kad būtų saugu prilietus korpusą. Toks reikalavimas taikomas ir inverterio išorės įrenginio korpusui. Patalpos temperatūra laikoma apie 20 °C. Bendra viso inverterio šiluminė varža apskaičiuojama:

![A black background with white text  AI-generated content may be incorrect.](data:image/png;base64...) (2)

Dėžės šiluminė talpa:

![](data:image/png;base64...) (3)

čia *Vi* – esančios medžiagos tūris [m3], *ρ* – medžiagos tankis [kg/m3], *cp* – specifinė šiluminė talpa [J/(kg·K)], *C –* šiluminė talpa, [J/kg]. Šiluminė talpa (*C*) apskaičiuojama orui ir korpuso metalui. Oro specifinė šiluminė talpa 1.006kJ/kgK, o oro tankis – 1,293 kg/m3. Kuriamo įrenginio dėžės matmenys 1000 x 750 x 300 mm, medžiaga - metalas.

Dėžės korpuso sienelių šiluminė varža:

![](data:image/png;base64...) (4)

čia

![A black background with blue and red text  AI-generated content may be incorrect.](data:image/png;base64...), ![A black background with blue and red text  AI-generated content may be incorrect.](data:image/png;base64...) (5)

čia *k* – medžiagos šilumos laidumas [W/(m·K)], *A* – paviršiaus plotas per kurį teka šiluma [m2], *L* – medžiagos storis per kurią teka šiluma, [m], *h* – konvekcinis šilumos perdavimo koeficientas [W/m2K]. Dažniausiai metalinių korpusų šilumos laidumas yra apie 50 – 55 [W/(m·K)]. Konvekcinis šilumos perdavimo koeficientas skaičiuojama natūraliai konvekcijai, kuri yra daugiausiai taikoma išorei ir vidui apie 5 W/(m2K).

Šilumos atidavimui modeliuojama tuščia uždara dėžė, kurioje sumontuotas inverteris. Modeliavimui sudaryta RC grandinė, kuri simuliuota naudojant *Ltspice* programinę įrangą (9 pav.).

![A diagram of a circuit  AI-generated content may be incorrect.](data:image/png;base64...)

**9 pav.** RC grandinė skirta modeliuoti temperatūrai (detalus modelis)

Atlikus simuliaciją, nustatyta, jog 120 kW inverteris gali įkaisti dėžės viduje iki 308 °C. Tai parodo, kad, norint integruoti dėžės viduje tokius inverterius, reikia specialiai projektuoti aušinimą, o tai reikalauja papildomų lėšų, nes be visa to, kiekvienu inverterio atveju, būtų reikalinga įvertinti skirtingą aušinimo poreikį dėl skirtingų inverterių. Tai taip pat turėtų įtakos tokio įrenginio patikimumui.

Kitas svarbus aspektas - inverterių gabaritai, kadangi jie gaminami skirtingų dydžių. Dauguma iki 120 kW galios inverterių yra gana dideli ir turi panašius matmenis, kaip kuriamo įrenginio korpusas. O, norint montuoti jų daugiau vienoje dėžėje, tai tampa keblu, nes kiekvienu atveju reiktų gaminti vis skirtingą dėžę, kas išbrangina tokio įrenginio gamybą.

Trečiasis argumentas - saulės elektrinių inverteriai, paprastai, yra sukurti montavimui pastato viduje arba išorėje, todėl montuojami pastato viduje ar lauke ant sienos, bet nėra dedami į uždarą bloką. Visi šie faktoriai ir lėmė, kad nuspręsta atsisakyti vidinio inverterio.

**2. Išnagrinėti kiekvieno komponento funkcionavimą atskirai ir su kitais komponentais**

Hibridinis įrenginys realizuojamas moduliniu principu, taip užtikrinant nepriklausomą kiekvieno funkcinio bloko kūrimą, testavimą/modifikavimą, taip palengvinant galimą įrenginio išplėtimą ir jo priežiūrą. Norint parinkti ir išnagrinėti kaip vidiniai komponentai funkcionuos atskirai ir su kitais komponentais, buvo suformuoti šie reikalavimai hibridiniam įrenginiui:

* *lankstumas* (modulinė struktūra sukonfigūruojama pagal kliento poreikius ir pritaikoma individualiam vartotojui su plėtros galimybe). Galimybė išplėsti protokolo taškų skaičių pagal poreikius.
* *universalumas* (tinka visiems pasirinkto protokolo ar vieno tipo prietaisams, nes neprisirišama prie konkretaus modelio ar konkrečios kompanijos modulių linijos, kai unikalūs valdikliai lieka išorėje),
* *duomenų srauto standartizavimas* (visų protokolų duomenys konvertuojami į BACNet/IP protokolą),
* *suderinamumas* (visi integruoti į vieningą sistemą įrenginio komponentai funkcionuoja korektiškai),
* realizuotas *Plug-and-play modelis* (PnP), t.y. galimybė automatiškai prijungti išorinius prietaisus, modulius ir valdiklius, kurių parametrai yra surašyti kuriamo įrenginio kompiuterio duomenų bazėje).
* Subscribe funkcija. Ji ne BaCNet protokoluose nėra numatyta dėl Meistras – Pavaldinys (Master – Slave) architektūros. Tai reiškia, kad pavaldus prietaisas (o tai galinis valdiklis, skaitliukas ar jutiklis) negali pats inicializuoti komunikacijos nei su Meistru, nei su kitu pavaldiniu. Todėl sumanymas yra toks, kad ją turėtų inicijuoti ir realizuoti protololų keitiklis pasinaudodamas Discovery procedūra savo protokolo (ModBus, Dali, MBus ir t.t. ) tinkle. T.y. protokolo keitiklis pats periodiškai apklausinėja (Pooling arba sudėtingesnis mechanizmas) galutinio valdiklio registrą (Duomenų tašką), ir aptikęs jo vertės pakeitimą, išsiunčia jo vertę kaip BaCNet objektą į BacNet/IP magistralę pagrindiniam BlackBox kompiuteriui.
* Discovery funkcija. BacNet protokole tai yra realizuojama kaip užklausos Who-is, Who-has. Tačiau kituose protokoluose jos nėra, arba ji labai ribota. Todėl kiekvienas protokolų keitiklis Discovery funkciją turėtų realizuoti per konkrečias procedūras savo protokole. Modbus vienaip, Dali kitaip, M-BUS dar kitaip ir t.t. Discovery funkcija numato naujo galinio valdiklio prijungimo ir atjungimo automatinį aptikimą ir jo adreso magistralėje nustatymą. Be to aptinkami prietaiso registrai ir jų adresai. Taip pat Discovery funkcija leidžia aptikti konfliktus magistralėje, kai du ar daugiau galinių prietaisų turi tą patį adresą.

Galima teigti, kad šiuo metu rinkoje naudojami įvairūs pastatų valdymo sistemų (angl. Building Management System – BMS) valdikliai. Šie valdikliai veikia *debesyse,* tačiau, esant interneto trikdžiams, BMS sistemoms aktualu išlaikyti įvairių išorinių elementų valdymą ir todėl nuspręsta atsisakyti standartinių išmaniųjų BMS valdiklių (SmartX Controller AS-P), o skirtingų valdiklių funkcijas apjungti į vieną įrenginį. Jo funkcijas atlieka kuriamo įrenginio kompiuteris, kuris valdytų pagrindinius protokolų keitiklius bei kitus būtinus komponentus reikalingus pastato efektyviam energijos valdymui ir greitam duomenų apdorojimui. Įrenginys komunikuoja su išorės įrenginiais per laidinę terpę (interneto kabeliu). Tai leis padidinti sistemos patikimumą, pagreitės įrenginio instaliavimas.

Įrenginyje bus integruoti standartiniai ir plačiai paplitę komunikacijos protokolų keitikliai (DALI, ModBus, Mbus, CAN), kurie konvertuoja į Bacnet protokolą ir taip užtikrina įrenginio sąveiką su įvairiomis sistemomis. Remiantis minėtais reikalavimais, pagrindinis tikslas, jog visi parinkti komponentai veiktų ir komunikuotų su pagrindiniu kompiuteriu nepriklausomai vienas nuo kito.

Įprasti protokolų keitikliai dažnai negali patenkinti visų techninių reikalavimų, nes jie apima tik pagrindines funkcijas. Todėl priimtas sprendimas naudoti atskirus protokolų keitiklius, atliekančius specifines funkcijas tam tikram išoriniam prijungtam moduliui. Šie keitikliai gali palaikyti mažiau populiarius arba nestandartinius protokolus, kuriems nėra rinkoje universalių sprendimų. Taip pat vienu metu galima palaikyti kelis protokolus ir tiesiogiai bendrauti su valdymo sistema per centralizuotą sąsają. Toks sprendimas optimizuoja konversijos procesus (sumažina atsako laiką, padidina sistemos reakcijos greitį ir duomenų perdavimo efektyvumą). Tiesioginė vidinė komunikacija su valdančiuoju kompiuteriu sumažina duomenų srauto delsą, kas yra ypač svarbu realiuoju laiku veikiančioms sistemoms, pasiekiant aukštesnį funkcionalumo, universalumo, saugumo ir sistemos našumo lygį. Tokie keitikliai taip pat leidžia ir lengviau prisitaikyti prie ateities poreikių.

Remiantis šiais išvardintais reikalavimais, buvo sudaryta įrenginio vidinė sujungimų schema, kuri pateikta 10 paveikslėlyje:

![A diagram of a computer  AI-generated content may be incorrect.](data:image/jpeg;base64...)

**10 pav.** Kuriamo įrenginio pirminė vidinė pajungimų schema

Visi parinkti schemoje komponentai bendrauja su pagrindiniu kompiuteriu naudojant Bacnet protokolą kaip pagrindinį komunikacijos protokolą. Preliminarūs dėžės signaliniai prievadai yra naudojami šie:

1. Ethernet prievadai internetui į išorinį tinklą,

2. Trys Ethernet prievadai (vidiniam BACNet/IP).

3. Du RS-485 prievadai,

4. Du USB įrenginio prievadai, vidiniam PC.

5. HDMI prievadas vidinio PC monitoriui.

6. RS485 du prievadai.

7. ESO Elektros tinklo trifazės srovės AC 360V prievadas

8. Atsarginio rezervinio tinklo trifazės srovės AC360V prievadas.

Kaip matyti iš pateiktos įrenginio sujungimų schemos, vidiniai komponentai yra naudojami šie:

* ModBUS (RS485)-Bacnet protokolų keitiklis MGate 5217, kuris konvertuoja Modbus RTU/ACSII/TCP į BACnet/IP protokolą
* iSMA-B-MIX18-IP išplėtimo modulis, lengvai konfigūruojamas 18 įėjimų/išėjimų (5UI, 5DI, 4AO, 4DO) išplėtimo modulis yra vienas iš universaliausių ir ekonomiškai optimaliausių sprendimų su RS485 ir 2x Ethernet sąsajomis palaiko atviro tipo Modbus (ASCII, RTU, TCP/IP) ir  BACnet (MSTP, IP) protokolus
* M-bus-Bacnet protokolų keitiklis su Mbus impulsų skaitiklis, MBHS-8
* Dali-Bacnet protokolų keitiklisCAN - BACNet/IP (ethernet) protokolų keitikliai. Galimybė prijungti 30 galinių prietaisų (600 – 1200 duomenų taškų).
* Tinklo analizatorius ND30bac (1 ir 3 fazių elektros tinklo skaitiklis komunikuojantis per BACnet protokolą)
* ABB 360V el. tinklo perjungėjas OTM63F4C21D400C PERJUNGIKLIS perjungia maitinimą iš rezervinės linijos arba generatorių.
* Industrinis PC - Pagrindinis kompiuteris, serveris (2 Ethernet prievadai).
* Ethernet HUB, tinkantis BACnet/IP standartui.
* Baterija QUINT4-CAP/ 24DC/10/8KJ
* Įrenginys turės kontrolerį, du 24 V maitinimo šaltinius (STEP3-PS/1AC/24DC/5/PT).

Kuriame įrenginyje BACNet skirtas komunikacijai su vidiniais komponentais, kurie palaiko BACNet protokolą. Jo pagrindinis tikslas – per jį stebėti, valdyti ir konfigūruoti pastatų automatizacijos sistemas (šildymą, vėdinimą, oro kondicionavimą, apšvietimą ir kt.).

Komunikacijai su išoriniais įrenginiais, šiuo atveju ModBus protokolas naudoja RS485 magistralę. Įrenginyje yra vienas RS485 prievadas, todėl galime naudoti Modbus/RTU, „Modbus ASCII“, ir BacNet/IP. Šis keitiklis konvertuoja Modbus RTU/ACSII/TCP į BACnet/IP protokolą ir o pagrindinės savybės:

* Palaiko pramoninę įtampą iki 6–35 V nuolatinės srovės.
* Integruoti **„Wi-Fi“** ir **Ethernet** interneto ryšiui.
* **100 Mb** Ethernet sąsaja.
* ESP32-WROOM-32D WiFi/BLE modulis. ( **Dviejų branduolių** galimybės).
* USB jungtis, skirta lengvai programuoti **ESP32** naudojant Arduino IDE.
* Pusiau dvipusis **RS485 ryšio** prievadas **.**
* Integruota **EEPROM** mikroschema duomenims saugoti.
* Automatinis duomenų srauto valdymas RS485.
* Du programuojami LED indikatoriai. (kaip siųstuvo ir imtuvo LED indikatorius)
* Pasirenkamas RS485 siųstuvo-imtuvo įtampos lygis (5 V ir 3,3 V).
* Pramoninis korpusas su DIN tvirtinimu ir kompaktišku PCB dydžiu.

RS485 sąsaja naudoja diferencinę įtampą, kad ryšys būtų be klaidų. Todėl reikalinga RS485 siųstuvo-imtuvo, kuris konvertuos įprastus TTL signalus į RS485 diferencinės įtampos signalus.

1. MAX485 (veikia esant 5 V įėjimo įtampai)
2. MAX3485 (veikia esant 3,3 V įėjimo įtampai)

RS485 naudojamas tolimojo nuotolio laidiniam ryšiui modulis palaiko ryšį iki 1 km atstumu, jei duomenų perdavimo sparta buvo 9600 bodų. Šiuo atveju, RS485 magistralės apsaugai panaudojome nedidelį SM712 serijos 600 W asimetrinį TVS diodų masyvą. SM712 yra specialiai sukurtas apsaugoti RS-485 taikymus su asimetrinėmis darbinėmis įtampomis (nuo -7 V iki 12 V) nuo pažeidimų dėl elektrostatinės iškrovos (ESD), greitųjų elektros pereinamųjų procesų (EFT) ir žaibo sukeltų viršįtampių.

Remiantis duomenų lapu, jis suteikia šias apsaugos priemones:

* ESD, IEC 61000-4-2, ±30 kV kontaktinis, ±30 kV oru
* EFT, IEC 61000-4-4, 50A (5/50ns)
* Saugiklis, IEC 61000-4-5 2-asis leidimas, 19 A (tP = 8/20 μs)

Pramoninis korpusas su DIN tvirtinimu ir kompaktišku PCB dydžiu.

Komunikacijai tarp BacNet/IP- Modbus protokolo keitiklio pateikta žemiau principinė schema (11 pav.):

![A screenshot of a computer program  AI-generated content may be incorrect.](data:image/png;base64...)![A screenshot of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**11 pav.** Modbus keitiklio principinė schema

Dali protokolų keitiklis….

CAN protokolų keitiklis ….

MQTT komunikuoja tiesiai per Bacnet.

Mbus protokolų keitiklis ….

iSMA-B-MIX18-IP išplėtimo modulis komunikuoja per maršrutizatorių su pagrindiniu kompiuteriu

Tinklo analizatorius komunikuoja naudodamas Bacnet protokolą ir per mašrutizatorių su pagrindiniu kompiuteriu…..

ABB 360V el. tinklo perjungėjas OTM63F4C21D400C PERJUNGIKLIS

Po vieną pastraipą parašyti kiekvienam protokolų keitikliui. Komponentų funkcionavimas gali būti paaiškinimas per pateiktą 10 pav. schemą.

**Po susitikimo (2025-07-17) papildomi komentarai:**

* Komponentai veikia pagal savo paskirtį ir dar tiesiogiai „*bendrauja*“ su kompiuteriu. Todėl reiktų aprašyti atskirai veikiančius komponentus, akcentuojant jų funkcionalumą.
* Nesieti naujumų prie tinklo analizatoriaus bei galios keitiklio, nes jie nėra pagrindiniai viso kuriamo įrenginio objektai, o tik sudedamosios dalys. Geriau koncentruotis į protokolų keitiklius.

Tam būtina atlikti technologijų analizę, įvertinus kokiais realizavimo būdais komponentas gali būti įgyvendintas, taip pat nustatyti komponentų integravimo ir optimizavimo metodų įtaką hibridinio įrenginio funkcionalumui, kartu pasiūlant optimalų sprendimą.

1. **Sukurti matematinį ir/arba kompiuterinį modelį, kuris aprašytų hibridinio įrenginio veikimą**

Hibridinio įrenginio protokolų keitiklio sistemos parametrizavimui, įvertinus ir jos rezervavimo poreikį, **s**ukurtas analitinis mazgo (protokolų keitiklio) modelis, kuriame taikomi skirtingi integravimo ir optimizavimo metodai (5 pav.).

![A diagram of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**5 pav.** Apibendrintos protokolų keitiklio sistemos struktūros modelis

Protokolų keitiklio sistema (5 pav.) yra hierarchinė ir susideda iš pagrindinio valdymo įrenginio (angl. Main Control Unit (MCU)), Ethernet komutatoriaus bei prie jo prijungtų įvairių žemesnės hierarchijos protokolų valdiklių (angl. Control arba Master Devices (MD)) su magistralėmis (BACnet, DALI, Modbus, CAN r kt.), kurios jungia jutiklius, skaitiklius, aktuatorius ar kitus valdikliui pavaldžius galinius įrenginius (angl. Subordinate arba Slave Devices (SD)). Duomenų atnaujinimui MCU siunčia užklausas arba komandas MD įrenginiams, o šie turi sau pavaldžius SD įrenginius, iš kurių informaciją surenka juos apklausiant. Dažnai toks apklausų ciklas yra determinuotas ir periodinis, todėl jį ir galima sumodeliuoti įvertinant apklausų dažnumą, surenkamų duomenų kiekį, trukmę. Apdorojęs duomenis iš SD surinktus duomenis, MD persiunčia juos atgal į MCU.

Kadangi MQTT, M-bus, DALI, Modbus ir CAN įrenginiai turi ribotą komunikacijos spartą, būtina įvertinti, kaip valdiklio užklausų dažnis veikia jų veikimą. Jei užklausos siunčiamos per dažnai, tai gali atsirasti duomenų praradimas arba dideli vėlavimai. Nors komutatorius užtikrina aukštą pralaidumą, tačiau kritinė sąsaja yra tarp MCU ir komutatoriaus, nes per ją keliauja visos užklausos ir atsakymai. Modeliavimas galėtų padėti nustatyti, kokio pralaidumo turėtų būti ryšio sąsajos, koks yra optimalus užklausų intensyvumas ir kaip paskirstyti apkrovą tarp jutiklių ir valdiklių. Modeliuojant duomenų srautus galima įvertinti apkrovas skirtinguose tinklo segmentuose, duomenų paketų vėlinimus ir praradimus, dinaminius tinklo pokyčius ir reagavimo strategijas. Pagrindinis valdiklis ir protokolų keitikliai gali inicijuoti užklausas galiniams įrenginiams, todėl analitinis modelis gali padėti nustatyti, kaip tinkamai paskirstyti ar valdyti srautus tarp skirtingų technologijų keitiklių, kad būtų išvengta perteklinio apkrovimo.

Analitinis modelis įvertina kiekvieno protokolo/valdiklio užklausų intensyvumą, skirtingų protokolų atsako laiką ir apkrovų pasiskirstymą tinkle. Modeliuojant srautus taikomi *Puasono* procesai arba *Markovo* modeliai, kurie leidžia nustatyti, pavyzdžiui, kiek sensorių gali būti aptarnaujama efektyviai, arba koks turėtų būti užklausų dažnis, kuris užtikrina optimalų duomenų surinkimą, neviršijant sisteminių resursų ribų.

**Sistemos mazgo analitinis matematinis modelis**

Kiekvienas sistemos komponentas laikomas atskiru mazgu, kuriam taikomi analitiniai matematiniai modeliai. Taikant analitinį modelį, analizuoti tokioje sistemoje sukuriamų užklausų srautai pagal jų atėjimo intensyvumą, apdorojimo intensyvumus, skirtingų protokolų atsako laikus ir atskirose tinklo dalyse sukuriamas apkrovas.

Ši protokolų keitiklio sistema (5 pav.) sumodeliuota kaip ryšių kanalais sujungtų mazgų tinklas, o kiekvienas mazgas ar duomenų perdavimo kanalas sumodeliuotas naudojant teletrafiko teorijoje taikomus aptarnavimo sistemų su eilėmis modelius (6 pav.). Taip buvo įvertinta mazgui tenkanti apkrova, užklausų (duomenų paketų) praradimai, vėlinimas eilėse ar bendra užklausų (paraiškų, paketų) aptarnavimo trukmė sistemoje.

![A white and black logo  AI-generated content may be incorrect.](data:image/png;base64...)

**6 pav.** Aptarnavimo sistemos atskiro mazgo modelis

Įvertinti šie aptarnavimo sistemos mazgo su eile modelio pradiniai **parametrai,** apibūdinantys paraiškųatėjimo į sistemą srautą:

* $Δt$ – laikotarpių tarp gretimų paraiškų aritmetinis vidurkis,
* $σ\_{Δt}$ – laikotarpių tarp gretimų paraiškų standartinis nuokrypis,
* $λ=1/Δt $– paraiškų atėjimo intensyvumas,

apibūdinantys paraiškųaptarnavimą (apdorojimą):

* + - $τ$ – paraiškos aptarnavimo vidutinė trukmė,
    - $σ\_{τ}$– paraiškos aptarnavimo trukmės standartinis nuokrypis.
    - $μ=1/τ$ – paraiškų aptarnavimo (apdorojimo) intensyvumas,
    - $n$ – kanalų skaičius,
    - $B$ – buferio talpa.

Apskaičiuojami parametrai:

* $A$ – apkrovos intensyvumas,
* $λ\_{a}$ – aptarnautų paraiškų intensyvumas,
* $λ\_{o}$ – išeinančių paraiškų intensyvumas,
* $λ\_{b}$ – prarastų arba blokuotų paraiškų intensyvumas,
* $P\_{b}$ – paraiškų blokavimo (praradimo) tikimybė,
* $W\_{q}$ – vidutinis laukimo laikas eilėje,
* $N\_{q}$ – vidutinis eilėje laukiančių paraiškų skaičius,
* $W=W\_{q}+τ$ – vidutinis aptarnautos paraiškos buvimo laikas mazge.

Tolimesnei analizei ir apibendrintam sistemos modeliui sudaryti naudojami vienkanalių sistemų su eilėmis modeliai. Buferių užimtumai ir rekomenduotinas jų dydis bus įvertinti atliekant atitinkamus skaičiavimus pagal sukuriamas apkrovas ir vidutines laukimo eilėse trukmes pagal *Little‘o* formulę. Tokie modeliai leidžia įvertinti mazgų parametrus skirtingo pobūdžio srautams ir skirtingiems aptarnavimo trukmių skirstiniams.

Analitiniai modeliai skirtingiems duomenų srautams ir aptarnavimo trukmių skirstiniams dažnai apibūdinami pagal *Kendall‘o* pasiūlytą žymėjimą: X/Y/1/K, X – nusako paraiškų srauto pobūdį, Y – aptarnavimo trukmių skirstinį, 1 – vienas kanalas, K – mazgo talpa (kiek paraiškų gali tilpti mazge – eilėje ir kanale, jei nenurodyta, tai $\infty $). Galima išskirti tris pagrindinius paraiškų srautų tipus: M – paprastasis (arba Puasono – laikotarpiai tarp paraiškų pasiskirstę pagal eksponentinį skirstinį), D –  determinuotas (laikotarpiai tarp paraiškų determinuoti – vienodi) ir G  – bendrasis (laikotarpių tarp paraiškų skirstinys apibūdinamas pasirenkant $Δt$ ir $σ\_{Δt}$). Tomis pačiomis raidėmis žymimas ir aptarnavimo trukmių skirstinys: M – eksponentinis, D –  determinuotas, G – bendrasis. Pavyzdžiui, žymėjimas M/D/1 reiškia, kad paraiškų srautas yra paprastasis, o aptarnavimo trukmė determinuota.

Paprastasis arba Puasono paraiškų srautas yra ordinarus (vienu laiko momentu gali ateiti tik viena paraiška), o laiko intervalų tarp gretimų paraiškų trukmės yra nepriklausomi atsitiktiniai dydžiai, pasiskirstę pagal eksponentinį skirstinį (jam $σ\_{Δt}=Δt$).

**Protokolo valdiklio ir jam pavaldžių galinių įrenginių tinklo modelis**

Protokolo valdiklio (MD) ir jam pavaldžių SD įrenginių posistemę galima sumodeliuoti naudojant mazgų analitines formules. Tačiau parenkant modelio parametrus reikia atsižvelgti į skirtingų technologijų specifiką ar techninius parametrus, pavyzdžių kokio dydžio yra duomenų paketai, koks magistralės, prie kurios prijungti SD įrenginiai, pralaidumas, kaip tie srautai formuojami.

Nagrinėjamoje hierarchinėje struktūroje (5 pav.) MCU yra pagrindinis valdiklis. Tam, kad atnaujintų duomenis, MCU siunčia užklausas arba komandas MD įrenginiams, o šie turi sau pavaldžius SD įrenginius iš kurių informaciją surenka juos apklausiant. Dažnai toks apklausų ciklas yra determinuotas ir periodinis, todėl jį galima sumodeliuoti įvertinant apklausų dažnumą, surenkamų duomenų kiekį, trukmę. Apdorojęs duomenis iš SD surinktus duomenis MD persiunčia juos atgal į MCU.

**Protokolo valdiklio posistemės duomenų srautai**

Galima išskirti tris pagrindinius duomenų srautus protokolo valdiklio posistemėje.

**MCU → MD: Užklausų srautas**

Užklausų iš MCU srautas modeliuojamas kaip $λ\_{mcu\_{i}}$ intensyvumo Puasono paraiškų srautas, kuris paduodamas į *i*-ojo MD eilę (buferį). Kiekviena užklausa inicijuoja apklausos ciklą MD potinklyje (7 pav.). Pavyzdžiui, jei naudojamas BACnet protokolas, tai apklausiant SD įrenginius naudojama ReadProperty užklausa, o SD atsakas yra ReadProperty response.

![](data:image/png;base64...)

**7 pav.** Valdiklio ir jam pavaldžių SD įrenginių potinklio modelio schema

MD posistemę galima sumodeliuoti naudojant M/M/1/K modelį, kuris leidžia įvertinti ne tik MD buferio apkrautumą, bet ir paraiškų praradimus, jei jų intensyvumas yra per didelis.

**MD užklausų ciklas: Vidinis valdomųjų SD apklausimas**

Modeliuojamas procesas (8 pav.), kurio metu *i*-asis MD cikliškai apklausia $S\_{i}$ jam pavaldžių SD įrenginių. Jei kiekvienas SD atsako su fiksuoto dydžio paketu, tai tokį procesą galima sumodeliuoti naudojant M/D/1 modelį. Jei atsakų į užklausas paketų dydžiai nėra vienodi arba dėl duomenų perdavimo bendra magistrale atsiranda perdavimo trukmių variacijos, tai tokį procesą galima sumodeliuoti M/M/1, M/G/1 arba G/G/1 modeliais.

![A diagram of a diagram of a diagram  AI-generated content may be incorrect.](data:image/png;base64...)

**8 pav.** Apklausų ciklo MD potinklyje tarp SD įrenginių laikinė diagrama

Jei *i*-asis MD apklausia $S\_{i}$ įrenginių, tai bendra MD mazgo duomenų ciklo surinkimo trukmė

$τ= \sum\_{j=1}^{S\_{i}}τ\_{poll}\_{j}$*.* (6)

čia $τ\_{poll}\_{j}$– kiekvieno $j$-ojo SD įrenginio apklausos ciklo trukmė

$τ\_{poll\_{j}}=τ\_{ifg\_{i}}+τ\_{req\_{j}}+τ\_{resp\_{j}}$, (7)

čia $τ\_{ifg\_{i}}$ – laiko intervalas (angl. interframe gap) tarp kadrų [s], kuris priklauso nuo *i*-ojo MD su SD jungiančios magistralės protokolo (pvz., 10 ms BACnet MP/TP atveju), bei atitinkamos duomenų užklausos ir atsako kadrų perdavimo trukmės

$τ\_{req\_{j}}= \frac{8⋅L\_{req\_{j}}}{C\_{i}}$[s]*,* (8)

$τ\_{resp\_{j}}= \frac{8⋅L\_{resp\_{j}}}{C\_{i}}$[s]*,* (9)

čia $C\_{i}$ –magistralės duomenų perdavimo bitų sparta [bps] (1 lentelė), $L\_{req}\_{j}$ir$L\_{resp}\_{j}$yra atitinkamai užklausos nuskaityti *j*-ojo SD įrenginio duomenis ir atsako kadrų dydžiai [B].

**1 lentelė.** Skirtingų protokolų parametrų suvestinė

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Protokolas** | **Paketo ilgis, baitai** | **Bitų sparta** | **Dalinimosi mechanizmas** | **Max SD** | **Paketų antraščių dedamosios** |
| **BACnet MS/TP** | ~488 | 9.6 – 115.2 kbps | Token passing | 32 (iki  128) | Preamble, Frame Type, Src/Dst Addr, CRC |
| **BACnet/IP** | ~1518 (Ethernet) | 100 Mbps – 1  Gbps | Ethernet/  IP switching | 100-ai–1000-ai | Ethernet, IP, UDP, BVLC |
| **BACnet/LonTalk** | ~250–300 | 78 kbps | CSMA/CA | 64–254 | Preamble, Control, Addressing, CRC |
| **BACnet/IPv6** | ~1280 | Kintanti (Ethernet, 6LoWPAN) | IP-based | Neribotai | Ethernet, IPv6, UDP, BVLC |
| **MQTT** | 10–100 (tipinis) | 100 Mbps+ (TCP/IP) | Broker pub/sub over TCP/IP | 1000-ai | Fixed + Variable + Optional Payload |
| **M-Bus** | 6–260 | 300 – 9600 bps | Master–slave polling | 250 | Start, Control, Addr, Control Info, Checksum |
| **DALI** | 2 + 1 | 1200 bps | Master–slave | 64 | Addr/Cmd (1B), Data (1B), Response (1B) |
| **Modbus RTU** | 4–256 | Iki 115.2 kbps | Master–slave polling | 247 | Slave Addr, Func Code, Data, CRC |
| **Modbus TCP** | Iki 260 | 100 Mbps+ | TCP/IP | Neribotai | MBAP (7B) + PDU |
| **CAN (Classical)** | ~6–16 | 10 kbps – 1  Mbps | CSMA/CR (priority by ID) | ~110 | Identifier, Control, DLC, CRC |
| **CAN FD** | ~8–72 | Iki 5 Mbps | CSMA/CR | ~110 | Tas pats kaip Classical, daugiau talpina duomenų |

**2 lentelė**. Antraščių ir naudingos duomenų dalies palyginimas skirtingiems protokolams

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Protokolas** | **Antraštė, baitai** | **Naudingų duomenų dalis, baitai** | **Suminis paketo ilgis, baitai** | **Pastabos** |
| **BACnet MS/TP** | 8 | 1–480 (tipinis: 32) | 40 (tipinis) iki 488 | MSTP talpina iki 480 baitų |
| **Modbus RTU** | 3  (addr  +  function  +  CRC) | 1–252 | 4–256 | Standartinis RTU paketas per RS485 |
| **MQTT over TCP/IP** | ~12 (TCP/IP) + 2– 4  MQTT  hdr | 1–1024+ (pvz.  JSON) | 30–1000+ | Priklauso nuo transportinio lygmens (TCP/IP) |
| **M-Bus (wired)** | 9 (control  +  header) | 1–252 (tipinis: 64) | ~70–270 |  |
| **DALI** | 1 | 1 | 2 | 8-bit komanda + 8-bit adresas |
| **CAN (2.0A)** | 5 | 0–8 | 13 | Max = 8 baitai (standartinis kadras) |
| **CAN FD** | 5 | 0–64 | 13–77 | Palaiko kintančio ilgio kadrus |

Duomenų kadrų paketus sudaro

$L\_{read}\_{j}=L\_{header\_{i}}+L\_{req\\_data}\_{j}$*,* (10)

$L\_{resp}\_{j}=L\_{header\_{i}}+L\_{resp\\_data}\_{j}$*,* (11)

čia $L\_{header\_{i}}$ – *i*-ojo MD magistralės duomenų kadrų antraštės, o $L\_{req\\_data}\_{j}$ ir $L\_{resp\\_data}\_{j}$ yra naudingų duomenų (angl.  data payload) dalis (2 lentelė). Toks atskyrimas yra naudingas, nes tolimesniam perdavimui ir saugojimui bus naudojama tik $L\_{resp\\_data}\_{j}$ naudingų duomenų dalis.

**MD → MCU: Atsako srautas**

Kiekvieno apklausos ciklo metu iš SD gauti atsakai išsaugomi MD atminties registruose. Užbaigus apklausos ciklą, MD surinktus duomenis sugrupuoja į didesnius duomenų paketus ir siunčia juos į MCU. Suminis naudingų duomenų kiekis surinktas apklausos ciklo metu yra

$L\_{poll\_{i}}=\sum\_{j=1}^{S\_{i}}L\_{resp\\_data}\_{j}$*.* (12)

Jei iš *j*-ojo SD užklausos metu surenkama$N\_{prop}\_{j}$objekto savybių (angl. object properties), tai bendras taip vadinamų duomenų taškų (angl. data points) skaičius surinktas užklausų ciklo metu:

$N\_{dp}\_{i}=\sum\_{j=1}^{S\_{i}}N\_{prop}\_{j}.$(13)

Jei bus *p*-ojo tipo objektų skaičius $O\_{p}$, kurių duomenys užima $L\_{p}$ baitų (pvz., 3 lentelė), tai

$L\_{resp\\_data}\_{j}= \sum\_{p=1}^{N\_{prop}\_{j}}[O\_{p}⋅L\_{p}]$*.* (14)

**3 lentelė.** Tipinės BACnet savybės, jų duomenų tipai ir dydžiai

|  |  |  |  |
| --- | --- | --- | --- |
| **Objekto savybės pavadinimas** | **BACnet duomenų tipas** | **Tipinis ilgis, baitai** | **Pastabos** |
| object-identifier | BACnetObjectIdentifier | 4 | 4 baitai (fiksuota) |
| object-name | CharacterString | Kintantis  (1– 64+) | UTF-8 arba ANSI, tipinis  ≤  64 |
| object-type | BACnetObjectType (enum) | 1 | Enum, telpa 1 baite |
| present-value | Priklauso nuo objekto tipo | 1–8 | Pvz., BOOLEAN (1), REAL (4), ENUM (1) |
| status-flags | BitString (4 bitai) | 1 | Telpa 1 baite |
| event-state | BACnetEventState (enum) | 1 | Enum |
| out-of-service | BOOLEAN | 1 | True/False |
| units | BACnetEngineeringUnits | 2 | UINT16 enum |
| description | CharacterString | Kintantis | Dažnai ≤ 64 chars |
| device-type | CharacterString | Kintantis | Dažnai ≤ 64 chars |
| location | CharacterString | Kintantis | Nebūtinas, tekstas |
| vendor-identifier | Unsigned (UINT16) | 2 | Vendor ID |
| protocol-version | Unsigned (UINT8) | 1 | Normally = 1 |
| protocol-revision | Unsigned (UINT8) | 1 | Version number |
| segmentation-supported | BACnetSegmentation (enum) | 1 | Enum |
| apdu-timeout | Unsigned (UINT16) | 2 | ms |
| number-of-APDU-retries | Unsigned (UINT8) | 1 | Pakartojimai (Retries) |

Kadangi MD su MCU sujungti per Ethernet komutatorių, tai visi apklausos ciklo metu surinkti duomenys bus perduodami toliau Ethernet kadrais. Maksimalus Ethernet kadre telpančių naudingų duomenų kiekis, jei naudojami IP ir UDP yra 1460 B, todėl Ethernet kadrų skaičius, kurio reikės apklausos ciklo metu surinktiems duomenims perduoti

$N\_{eth\_{i}}=\left⌈L\_{poll\_{i}}/1460\right⌉$*.* (15)

Taip sukuriamas *i*-ojo MD duomenų srautas į MCU, kurio intensyvumas

$λ\_{md}\_{i}=λ\_{mcu}\_{i}⋅(1-P\_{b\_{i}})/N\_{eth}\_{i}$. (16)

Jo perdavimas per Ethernet komutatorių, suminio srauto suformavimas už komutatoriaus, kai sutankinami kitų MD siunčiami srautai, ir jo apdorojimas MCU įrenginyje irgi gali būti analizuojamas taikant kiekvienam etapui analitinius mazgų su eilėmis modelius.

**Analitinio protokolų keitiklio tinklo modelio taikymas**

Protokolo valdiklio (MD) ir jam pavaldžių įrenginių (SD) posistemės veikimas modeliuotas naudojant mazgų analitines formules. Tačiau, parenkant modelio parametrus, buvo būtina atsižvelgti į skirtingų technologijų specifiką ar techninius parametrus: kokio dydžio yra duomenų paketai, koks magistralės, prie kurios prijungti pavaldūs įrenginiai, pralaidumas, kaip tie srautai formuojami.

Analitiškai aprašyti trys protokolo valdiklio posistemės duomenų srautai:

1. MCU – MD;
2. MD užklausų ciklas: vidinis valdomųjų SD apklausimas;
3. MD → MCU: atsako srautas.

Atsižvelgus į protokolų keitiklio sistemos veikimo principus, sudarytas visos sistemos analitinis modelis AnalitinisModelis.slx MATLAB *Simulink* aplinkoje (9 pav.), panaudojus teletrafiko teorijos principus bei sukuriamų paraiškų srautų apdorojimo analizės metodus. Sugeneruoti užklausų srautai analizuojami, įvertinant jų atvykimo ir apdorojimo intensyvumus, skirtingų protokolų parametrus bei šių srautų paskirstymą tinkle. Taip galima kiekybiškai įvertinti kiekvieno komponento įtaką bendram duomenų srauto elgesiui.

![A diagram of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**9 pav.** Protokolų keitiklio tinklo modelis *Simulink* aplinkoje

Buvo priimta, kad protokolų keitiklio tinklas veikia BACnet/IP technologijos pagrindu. Pagrindinis valdymo įrenginys (MCU) su žemesnės hierarchijos valdiklių (master arba MD) įrenginiais komunikuoja per Ethernet komutatorių. MCU siunčia duomenų nuskaitymo arba valdymo užklausas, o MD įrenginiai nuskaito duomenis iš prie jų prijungtų pavaldžių (slave tipo (SD)) įrenginių arba juos valdo ir grąžina MCU nuskaitytus duomenis.

Kiekvienas tinklo mazgas yra *Simulink* komponentų posistemė.

Nagrinėjamu atveju sudarytas modelis, kai naudojami 4 MD įrenginiai. Kiekvienas MD mazgas atitinka MD tinklą su jam pavaldžiais SD įrenginiais, kurių skaičių galima keisti. Taip pat kiekvienam mazgui galima nurodyti kokio protokolo magistralė yra naudojama prijungti SD įrenginiams, kiek savybių (angl. Properties arba Data Points) kiekvienas SD turi, kokio tipo analitinį modelį (M/M/1, M/D/1, M/M/1/K) jam taikyti, kokį MD buferio dydį naudoti.

Nagrinėjamu atveju protokolų keitiklio tinklas veikia BACnet/IP technologijos pagrindu. Pagrindinis valdymo įrenginys (MCU) su žemesnės hierarchijos valdiklių (angl. Master arba MD) įrenginiais komunikuoja per Ethernet komutatorių. MCU siunčia duomenų nuskaitymo arba valdymo užklausas, o MD įrenginiai nuskaito duomenis iš prie jų prijungtų pavaldžių (slave tipo (SD)) įrenginių arba juos valdo ir grąžina MCU nuskaitytus duomenis.

Kiekvienas tinklo mazgas yra *Simulink* komponentų posistemė, kurią galima atidaryti ir pažiūrėti kas yra jos viduje, kokie parametrai ar vidinės funkcijos naudojamos.

**Parametrų nustatymas**

Modeliuojant MD parametrai apskaičiuojami automatiškai naudojant *evaluate\_params* funkciją, į kurią paduodami parametrai: protokolo tipas (galimi variantai: BACnet MSTP, BACnet IP, Modbus RTU, Modbus TCP, MQTT TCP/IP, MBus wired, DALI, CAN Classical, CAN FD, KNX TP1, KNXnet IP), SD įrenginių skaičius ir iš SD nuskaitomų savybių skaičius. Pagal protokolo tipą parenkamos tipinės parametrų reikšmės, kurios naudojamos pasirinktiems protokolams. Jos gali būti pakoreguotos funkcijos viduje konkrečiam taikymui, pavyzdžiui, žinant konkrečius parametrų tipus pagal realią situaciją.

Nagrinėjamas scenarijus, kai protokolo keitiklio tinkle yra 4 skirtingų protokolų MD. Nurodomi kiekvieno MD tinklo protokolai, SD įrenginių skaičius, objektų skaičius užklausos pakete, savybių (data points arba properties) skaičius. Apskaičiuoti kiekvieno MD užklausų ir atsakų paketų dydžiai, jų perdavimo trukmės, aptarnavimo intensyvumas.

**Pastaba:** Pilnas taikymo pavyzdžio ir *evaluate\_params* funkcijos kodas, kuris leidžia įvertinti ir kitų protokolų naudojimą arba atlikti modeliavimą su kitais parametrais yra pateiktas AnalitinioModelioValdymoScriptas.mlx faile (žr. į priedą).

**Protokolų keitiklio tinklo parametrų modeliavimas taikant analitinį modelį**

Analitinio modelio dėka įvertinama MCU siunčiamų užklausų srauto į MD intensyvumo įtaka skirtingiems MD parametrams analizuojamame protokolų keitiklio tinkle. Modeliuojant galima įvertinti kiekvieno 5 paveikslėlyje parodyto tinklo mazgo parametrus. Pavyzdžiui, 4 lentelėje parodytas vėlinimas tinklo mazguose, kai MCU siunčia užklausas į kiekvieną MD tokiais intensyvumais: $λ\_{md}\_{1}$=54 req/s, $λ\_{md}\_{2}$=75 req/s, $λ\_{md}\_{3}$=34 req/s, $λ\_{md}\_{4}$=43  req/s.

**4 lentelė. Vėlinimo verčių tinklo mazguose vertės**

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | Wmcu\_sw, s | Wsw\_md, s | Wmd, s | Wmd\_sw, s | Wsw\_mcu, s | Wmcu proc, s | Wtotal\_md, s |
| MD1 | 5.7684e-05 | 2.4833e-05 | 0.0184 | 6.6316e-05 | 9.7781e-05 | 3.9616e-05 | 0.0187 |
| MD2 | 5.7684e-05 | 6.9027e-05 | 0.0134 | 1.0377e-04 | 9.7781e-05 | 3.9616e-05 | 0.0138 |
| MD3 | 5.7684e-05 | 1.1033e-04 | 0.0303 | 1.1149e-04 | 9.7781e-05 | 3.9616e-05 | 0.0307 |
| MD4 | 5.7684e-05 | 1.4569e-05 | 0.0233 | 3.5414e-05 | 9.7781e-05 | 3.9616e-05 | 0.0236 |

Atlikus gautų rezultatų analizę, pastebėta, kad didžiausią įtaką duomenų surinkimo trukmei turi MD potinkliai, kurių duomenų perdavimo sparta yra daug kartų mažesnė už tinklo mazgus apjungiančio Ethernet komutatoriaus kanalų spartą. Todėl toliau pateikiami tik MD parametrų modeliavimo rezultatai.

Sukūrus analitinį modelį, atlikta visa eilė modeliavimų, keičiant MCU siunčiamų užklausų į MD įrenginius intensyvumą. Modeliuojama sistemos atsako trukmė (10 pav.), blokuotos apkrovos priklausomybė (11 pav.), taip pat aptarnauta ir blokuota apkrova (12 pav.) bei atliktas užklausų intensyvumo modeliavimas, tiriant apkrovos (Erlangais) priklausomybes (13 pav.).

|  |  |
| --- | --- |
| ![](data:image/x-emf;base64...) | ![](data:image/x-emf;base64...) |
| **10 pav.** $W\_{md}$ priklausomybė nuo $λ\_{md}$ | **11 pav.** $P\_{b md}$ priklausomybė nuo $λ\_{md}$ |
| ![](data:image/x-emf;base64...) | ![](data:image/x-emf;base64...) |
| **12 pav.** Aptarnautos ir blokuotos apkrovos priklausomybė nuo $λ\_{md}$ | **13 pav.** Duomenų surinkimo trukmės $T\_{dp poll}$ priklausomybė nuo $λ\_{md}$ |

**Užklausos ir atsako trukmės modeliavimas**

Iš gautų rezultatų matyti (10 pav.), kad $W\_{md}$ didėja, kai didėja $λ\_{md}$, bet nevienodai skirtingiems protokolams; šiuo atveju MD potinkliuose suformuojami skirtingo dydžio duomenų paketai, o ir jų duomenų perdavimo magistralių sparta skiriasi. Nuo to priklauso ir MD paraiškų aptarnavimo intensyvumas $μ\_{md}$. Todėl $W\_{md}$ pradeda didėti greičiau dėl vėlinimo eilėje trukmės didėjimo, kai paraiškų intensyvumo $λ\_{md}$ vertė priartėja prie paraiškų aptarnavimo intensyvumo $μ\_{md}$ vertės.

**Paraiškų blokavimo tikimybės modeliavimas**

Kaip nuo MCU siunčiamų užklausų į MD įrenginius intensyvumo $λ\_{md}$ priklauso paraiškų blokavimo tikimybė MD mazge $P\_{b md} $parodyta 11 pav. Gauti rezultatai rodo, kad $P\_{b md}$ pradeda staigiai didėti, kai paraiškų intensyvumo $λ\_{md}$ vertė priartėja prie paraiškų aptarnavimo intensyvumo $μ\_{md}$ vertės dėl to, kad MD nebespėja aptarnauti paraiškų ir jo buferis perpildomas.

**Aptarnauta ir blokuota apkrova**

Aptarnautos ir blokuotos apkrovos dalis priklauso taip pat priklauso nuo paraiškų intensyvumo $λ\_{md} $(12 pav.). Didėjant paraiškų intensyvumui $λ\_{md}$, didėja ir aptarnauta apkrovos dalis, bet ji nusistovi ties 1, kai $λ\_{md}$ viršija paraiškų aptarnavimo intensyvumą $μ\_{md}$ (12 pav.). Blokuotos apkrovos dalis tiesiogiai priklauso nuo $P\_{b md}$.

**Užklausų intensyvumo optimizavimas**

Siekiant nustatyti optimalų užklausų siuntimo dažnį $λ\_{md}$, kai reikia apklausti žinomą kiekį SD tipo įrenginių ir siekiama kuo greičiau surinkti visų savybių (angl. data points) reikšmes, galima naudotis duomenų surinkimo trukmės $T\_{dp poll}$ priklausomybės nuo $λ\_{md}$ grafiku (13 pav.).

Jame kiekvieno *i*-ojo valdiklio (MD) iš jam pavaldžių SD įrenginių savybių surinkimo trukmių $T\_{dp poll\_{i}}$ vertės apskaičiuojamos pagal formulę:

$T\_{dp poll\_{i}}=S\_{i}⋅min⁡(\frac{1}{λ\_{md\_{i}}},W\_{md\_{i}})$(17)

čia $S\_{i}$ – i-ojo valdiklio SD įrenginių skaičius, $λ\_{md\_{i}}$ – paraiškų nuskaityti duomenis dažnis, $W\_{md\_{i}}$ – duomenų nuskaitymo (polling) trukmė, kuri gauta įvertinant kiek savybių (data points) yra nuskaitoma, laukimo eilėje (buferyje) laikus ir jų priklausomybes nuo konkretaus protokolo duomenų paketų dydžių, duomenų perdavimo magistralės spartos.

Kai užklausų intensyvumas yra žemas, kiekvieno atsakymo trukmė būna trumpesnė už laikotarpį tarp užklausų, dėl to visas duomenų surinkimo ciklas trunka ilgiau ir grafike galime matyti, kad prie mažų $λ\_{md}$ verčių $T\_{dp poll}$ yra didelis. Didinant $λ\_{md}$ intensyvumą, duomenų surinkimo trukmė mažėja, kol pasiekiamas optimalus taškas. Viršijus šį tašką, pradeda formuotis užklausų eilės, sistemos apkrova didėja, o bendras duomenų surinkimo laikas vėl pradeda augti.

1. **Įvertinti atskirų komponentų charakteristikų įtaką viso įrenginio funkcionavimui (remiantis duomenų srautų iš įvairių sistemų modeliavimu**

Imitaciniam duomenų srautų perduodamų protokolų keitiklio tinkle modeliavimui pasirinktas MATLAB *SimEvents* diskretinių įvykių modeliavimo paketas (14 pav.).

![A diagram of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**14 pav**. Imitacinis protokolų keitiklio tinklo modelis

Kiekvienas tinklo mazgas imituojamas naudojant *SimEvents* eilės komponentą *Entity Queue*, skirtą buferiui, laukimo laikui eilėje ir praradimams įvertinti, ir *Entity Server* komponentą duomenų kanalui. Kiekvienas 14 paveikslėlyje pavaizduoto tinkle mazgas yra *Simulink* posistemė, kurios viduje yra iš komponentų ir papildomų MATLAB funkcijų sudarytas tinklo mazgo modelis. Tokios mazgo posistemės pavyzdys parodytas 15 paveikslėlyje:

![A diagram of a computer program  AI-generated content may be incorrect.](data:image/png;base64...)

**15 pav.** Imitacinio modelio posistemės pavyzdys

Naudojant imitacinį modelį imituojamas kiekvieno paketo perdavimas. Todėl MCU mazge yra *Entity Generator* tipo *SimEvents* blokas, kurio viduje yra funkcija, aprašanti, kokio pobūdžio srautas turėtų būti generuojamas, pavyzdžiui, nurodant laikotarpių tarp gretimų paraiškų atsitiktinio generavimo parametrus ar determinuotas vertes.

**Pastaba**: Detaliau su kiekvienu mazgu ir jų vidinėmis funkcijomis galima susipažinti atsidarius Simulink formato “ImitacinisModelis.slx” failą.

Modeliuojant protokolų keitiklio parametrus, sudarytas BACnet IP protokolo pagrindu veikiančio protokolų keitiklio modelis, kuriame naudojami 4 žemesnės hierarchijos MD valdikliai, nuskaitantys iš jiems pavaldžių SD įrenginių duomenis.

Paketų dydžiai apskaičiuojami automatiškai, naudojant tam sukurtas funkcijas, pagal tai, kiek objektų yra duomenų pakete, koks transportinis protokolas naudojamas ir ar naudojami masyvo indeksų masyvai. Kontrolei apskaičiuojami paketų dydžiai buvo patikrinti su realiais duomenimis ir buvo analizuojami su Wireshark programa (16 pav.).

![A screenshot of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**16 pav.** Realaus BACnet MS/TP atsako paketo pavyzdys

Nustatyta, kad sukurtos funkcijos, prie tų pačių parametrų apskaičiuoja tokį patį užklausos ir atsako paketų dydį:

n\_prop\_per\_obj = 1; n\_obj\_per\_packet=1; with\_array\_index=true; transport\_md='mstp'; avg\_value\_size=4;

L\_req\_from\_md\_to\_sd = bacnet\_readmultiple\_request\_size(transport\_md, n\_obj\_per\_packet, n\_prop\_per\_obj, with\_array\_index)

L\_req\_from\_md\_to\_sd = 34

L\_resp\_from\_sd\_to\_md = bacnet\_readmultiple\_response\_size(transport\_md, n\_obj\_per\_packet, n\_prop\_per\_obj, with\_array\_index, avg\_value\_size)

L\_resp\_from\_sd\_to\_md = 41

Tinklo darbingumo parametrų įvertinimui buvo sukurti atskiri scenarijai MATLAB aplinkoje, kurie keičia parametrus ir juos pritaiko imitaciniam tinklo modeliui, o gautus modeliavimo rezultatus išsaugo \*.mat tipo failuose.

Toliau pateikiama gautų rezultatų analizė.

**MD potinklio magistralės spartos įtaka parametrams**

Šiuo tyrimu buvo siekiama nustatyti kaip pagrindiniai BACnet MS/TP valdiklio darbingumo parametrai: duomenų surinkimo trukmė $W\_{md}$ ir blokavimo tikimybė $P\_{b md}$, priklauso nuo MCU generuojamo suminio paraiškų intensyvumo $λ\_{mcuΣ}$, esant skirtingai MD duomenų perdavimo magistralės spartai $C\_{md}$. Tokia analizė būtina, siekiant įvertinti kokios spartos duomenų perdavimo magistralė turėtų būti naudojama arba kokią spartą nustatyti konfigūruojant, jei siekiama užtikrinti tam tikrą kritinį $W\_{md}$, arba jei siekiama išvengti paraiškų blokavimo, kuris gali būti kai dėl nepakankamo pralaidumo MD nebespėja surinkti duomenų iš SD įrenginių.

$W\_{md} $priklausomybė nuo $λ\_{mcuΣ}$ prie skirtingų $C\_{md}$, kai imitacinio modelio parametrai atitinka analitinio modelio M/D/1 srautų pobūdį, buferio talpa – 4 req., savybių skaičius kiekvienam obj. – 4, vidutinis savybės duomenų dydis – 4 baitai, o paraiškų srautas nukreipiamas į vieną MD potinklį pateikta 17 paveikslėlyje. Gauti rezultatai rodo, kad $W\_{md} $yra mažesnė prie didesnių $C\_{md}$ verčių. Taip yra todėl, kad prie didesnių $C\_{md}$ verčių gaunamas ir didesnis paraiškų aptarnavimo intensyvumas $μ\_{md}$. Prie didesnių $λ\_{mcuΣ}$ verčių $W\_{md}$ pakyla iki slenkstinio lygio, kuris kaip parodys kituose skyreliuose analizuojami rezultatai, priklauso nuo buferio dydžio, bet yra nevienodas skirtingoms $C\_{md}$ vertėms. Taip pat prie skirtingų $C\_{md}$ verčių yra tam tikras slenkstinis $λ\_{mcuΣ}$, kurį pasiekus $W\_{md}$ kreivėje matomas pakilimas iki nusistovėjusios vertės.

Paraiškų blokavimo tikimybės $P\_{b md} $priklausomybės nuo $λ\_{mcuΣ}$ prie skirtingų $C\_{md}$ kreivės, gautos prie tų pačių aukščiau aprašytų sistemos pradinių parametrų, pateiktos 18 paveikslėlyje. Iš gautų $P\_{b md}$ grafikų taip pat matome, kad blokavimo tikimybė auga didėjant $λ\_{mcuΣ}$, kai pasiekiamas kanalo pralaidumas. Todėl iš šio grafiko galima nustatyti didžiausią $λ\_{mcuΣ}$, pagal tam tikrą $P\_{b md}$ ribą, pavyzdžiui (0,001), kuri neturėtų būti viršyta.

|  |  |
| --- | --- |
| ![](data:image/x-emf;base64...)  **17 pav.** $W\_{md}$ priklausomybė nuo $λ\_{mcuΣ}$ prie skirtingų $C\_{md}$ | ![](data:image/x-emf;base64...)  **18 pav.** $P\_{b md}$ priklausomybė nuo $λ\_{mcuΣ}$ prie skirtingų $C\_{md}$ |

**MD įrenginių skaičiaus įtaka parametrams**

Šis tyrimas parodo kas būtų, jei MCU generuojamų paraiškų srautas, kurio intensyvumas $λ\_{mcuΣ}$, būtų paskirstytas tarp kelių tokio paties tipo MD įrenginių. Tai leidžia imituoti situaciją, kai įvertinami rezervavimo scenarijai ar bandoma įvertinti kokią įtaką daro srautų paskirstymas jų perdavimo ir aptarnavimo parametrams.

19 ir 20 paveikslėliuose, atitinkamai, parodytos $W\_{md} $ir $P\_{b md}$ priklausomybės nuo $λ\_{mcuΣ}$, jei paraiškų srautas nukreipiamas į skirtingą skaičių to paties tipo ir parametrų MD įrenginių, kai $C\_{md}$ = 19200 bps, imitacinio modelio parametrai atitinka analitinio modelio M/D/1 srautų pobūdį, buferio talpa – 4 req., savybių skaičius kiekvienam obj. – 4, vidutinis savybės duomenų dydis – 4 baitai.

|  |  |
| --- | --- |
| ![](data:image/x-emf;base64...)  **19 pav.** $W\_{md}$ priklausomybė nuo $λ\_{mcuΣ}$, kai naudojamas skirtingas MD skaičius | ![](data:image/x-emf;base64...)  **20 pav.** $P\_{b md}$ priklausomybė nuo $λ\_{mcuΣ}$, kai naudojamas skirtingas MD skaičius |

Gauti rezultatai (19, 20 pav.) rodo, kad kuo didesnis MD skaičius, tarp kurių paskirstomas bendras MCU generuojamų paraiškų intensyvumas $λ\_{mcuΣ}$, tuo mažesnė apkrova tenka kiekvienam MD įrenginiui. Tokiu būdu, gaunami rezultatai gali būti panaudoti įvertinant, kiek MD įrenginių reikėtų parinkti, siekiant tam tikro kriterijaus, pavyzdžiui, kad nebūtų viršyta tam tikra kritinė $W\_{md}$ arba $P\_{b md}$ vertė.

**MD įrenginių buferio talpos įtaka parametrams**

Buferis leidžia patalpinti gaunamas paraiškas į eilę, jei, pavyzdžiui, nauja paraiška nuskaityti duomenis atėjo dar negavus ankstesnės paraiškos duomenų. Todėl, jei laikotarpiai tarp ateinančių paraiškų yra nevienodi, tai didesnis buferis leidžia sumažinti jų blokavimo (arba išmetimo dėl buferio perkrovimo) tikimybę. 21 ir 22 paveikslėliuose, atitinkamai, parodytos $W\_{md} $ir $P\_{b md}$ priklausomybės nuo $λ\_{mcuΣ}$, jei naudojama nevienoda buferio talpa, kai $C\_{md}$ = 38400 bps, imitacinio modelio parametrai atitinka analitinio modelio M/D/1 srautų pobūdį, buferio talpa – 4 req., savybių skaičius kiekvienam obj. – 4, vidutinis savybės duomenų dydis – 4 baitai, o paraiškų srautas nukreipiamas į vieną MD potinklį.

|  |  |
| --- | --- |
| ![](data:image/x-emf;base64...)  **21 pav.** $W\_{md}$ priklausomybė nuo $λ\_{mcuΣ}$, kai naudojama skirtinga MD buferio talpa | ![](data:image/x-emf;base64...)  **22 pav.** $P\_{b md}$ priklausomybė nuo $λ\_{mcuΣ}$, kai naudojama skirtinga MD buferio talpa |

Iš gautų rezultatų (21, 22 pav.) matyti, kad esant didesnei buferio talpai gaunama mažesnė $P\_{b md}$ prie tos pačios $λ\_{mcuΣ}$ vertės, o $W\_{md}$ galioja atvirkštinė priklausomybė, nes kuo didesnė buferio talpa, tuo didesnis galimas aptarnautų paraiškų laukimo eilėje laikas.

**Paraiškų srautų pobūdžio įtaka parametrams**

Naudojant imitacinį modelį, galima įvertinti paraiškų srauto pobūdžio įtaką protokolų valdiklio tinklo srautų aptarnavimo parametrams. Nuo jo priklauso koks yra laikotarpių tarp gretimų paraiškų skirstinys. Tai leidžia įvertinti atvejus, kai, pavyzdžiui, dėl papildomų duomenų srautų tinkle, kurie nėra tiesiogiai susiję su MCU paraiškomis ir jų atsakais, pastarieji yra įtakojami nes kanalų pralaidumai yra naudojami kitų duomenų perdavimui. Dėl to gali pasireikšti vėlinimų ir laikotarpių tarp gretimų paraiškų fluktuacijos. Jei laikotarpiai tarp paraiškų yra nevienodi, tai toks paraiškų srautas gali būti įvertintas taikant M/D/1 modelio atitikmenį, kai paraiškų srautas yra paprastasis, o laikotarpiai tarp paraiškų pasiskirstę pagal eksponentinį skirstinį. Kitas atvejis būtų, jei tinklas yra pilnai susinchronizuotas arba suderintas, t.y., kai laikotarpiai tarp paraiškų ir jų aptarnavimo trukmės yra determinuoti – atitinka D/D/1 modelį.

23 ir 24 paveikslėliuose, atitinkamai, parodytos $W\_{md} $ir $P\_{b md}$ priklausomybės nuo $λ\_{mcuΣ}$, kai paraiškų srauto pobūdis atsitiktinis arba determinuotas, prie $C\_{md}$ = 9600, 19200, 38400 bit/s, buferio talpa – 4 req., savybių skaičius kiekvienam obj. – 4, vidutinis savybės duomenų dydis – 4 baitai, o paraiškų srautas vienodai paskirstomas tarp keturių vienodų MD potinklių.

|  |  |
| --- | --- |
| ![](data:image/x-emf;base64...)  **23 pav.** $W\_{md}$ priklausomybė nuo $λ\_{mcuΣ}$, prie skirtingų $C\_{md}$, kai srautas atsitiktinis ir determinuotas | ![](data:image/x-emf;base64...)  **24 pav.** $P\_{b md}$ priklausomybė nuo $λ\_{mcuΣ}$, prie skirtingų $C\_{md}$, kai srautas atsitiktinis ir determinuotas |

Išanalizavus gautus rezultatus (23 ir 24 pav.), matyti, kad, esant determinuotam srautų pobūdžiui, net kai kiti parametrai yra tokie patys, yra gaunamos tinkamesnės charakteristikos – mažesnis vėlinimas ir blokavimo tikimybė. Taip yra todėl, kad šiuo atveju teoriškai galima eliminuoti laukimo laikus eilėse, kol paraiškos bus aptarnaujamos iki ateis nauja paraiška, bet taip gali būti tik kol paraiškų srauto intensyvumas yra mažesnis už jų aptarnavimo intensyvumą.

# Įvykdyti paslaugų pirkimai

Išvardinti veiklos metu įvykdytus paslaugų pirkimus bei aprašyti kaip jie įtakojo veiklos rezultatus. Naudoti lentelės formą). Reagentų/medžiagų/mažaverčio inventoriaus pirkimų čia nurodyti nereikia.

| **Nr.** | **Pirkimo objektas** | **Tiekėjas** | **Paslaugos aprašymas ir nauda veiklai** |
| --- | --- | --- | --- |
| *Projekto vykdytojas/partneris:* **UAB XXXXX** | | | |
| 1. |  |  |  |
| 2. |  |  |  |
| 3. |  |  |  |

Kartu su ataskaita prašome pateikti įsigytos paslaugos rezultatą (ataskaitą, tyrimo protokolą ar pan.), jei nebuvo pateikta anksčiau.

# Užduočių atlikimas

Pateikti informaciją, kokios užduotys buvo atliktos projektą vykdančių asmenų, kas jas atliko, kiek laiko tam skyrė, naudoti lentelės formą.

| **Nr.** | **Užduotis** | **Darbuotojai/darbovietė** | **Laiko sąnaudos valandomis** |
| --- | --- | --- | --- |
| 1. |  |  |  |
| 2. |  |  |  |
| 3. |  |  |  |
| 4. |  |  |  |
| 5. |  |  |  |

Jeigu tai pačiai užduočiai atlikti buvo įsigytos paslaugos ir skirtas projektą vykdančių asmenų darbo laikas bei išmokėtas darbo užmokestis, būtina atskirti paslaugos teikėjo ir projektą vykdančių asmenų indėlį į rezultatą, paaiškinti, kaip paslaugos rezultatus papildė projektą vykdančių asmenų darbas.

# Pasiekti tyrimų rezultatai

Trumpai aprašyti pasiektus rezultatus, sprendžiant šios ataskaitos 3 punkte nurodytus neapibrėžtumus. Rekomenduojama apimtis - 2 psl. kiekvienam rezultatui.

**I.** Nustatyti, kokie yra pagrindiniai hibridinio įrenginio komponentai, jų savybės, reikalavimai ir galimi veikimo modeliai

**1. Išspręstas neapibrėžtumas:** kokie hibridinio įrenginio architektūriniai sprendimai leistų efektyviai realizuotinaujų BAS įrenginių atpažinimą, generuoti jiems valdymo objektus bei algoritmus, taip sumažinant rankinio darbo apimtis ir galimus konfigūravimo netikslumus?

Naudojant semantines ontologijas, mašininį mokymąsi bei DI principais grįstą valdymą galima automatiškai atpažinti naujus įrenginius, generuoti jiems valdymo objektus bei algoritmus, taip sumažinant rankinio darbo apimtis ir galimus konfigūravimo netikslumus. Tam būtina kurti naujus programinius sprendimus, kurie užtikrintų pažangios dinaminės valdymo sistemos veikimą.

Šie sprendimai – tai .... Aš manau, jog semantines ontologijas reikės išmesti iš teksto, koncentruotis vien tik trimis smart subscribe, P&P, discovery funkcijomis. Martynas min4jo, jog DI jie neplanuoja naudoti.

**2. Išspręstas neapibrėžtumas**: kokie hibridinio įrenginio komponentų specifikaciniai reikalavimai leistų palaikyti semantinių duomenų modelius?

....aprašyti konkrečius reikalavimus atskiriems projektuojamo įrenginio komponentams, kurie leistų išspręsti neapibrėžtume nurodytą funkcionalumą

**II.** Išnagrinėti kiekvieno komponento funkcionavimą atskirai ir su kitais komponentais

**1. Išspręstas neapibrėžtumas:** kaip realizuoti *stand alone* (kitaip, black box) principą, kad įrenginys gebėtų pilnavertiškai valdyti visas pastato sistemas, nutrūkus belaidžio Interneto ryšiui (ryšiui su ESE duomenų baze)? Kokiomis technologijomis realizuoti automatizuotą naujų įrenginių integraciją?

Šiuo metu rinkoje naudojami įvairūs pastatų valdymo sistemų BMS valdikliai, kurie veikia *debesyse*. Tačiau, esant interneto trikdžiams, BMS sistemoms aktualu išlaikyti įvairių išorinių elementų valdymą, ir todėl nuspręsta atsisakyti standartinių išmaniųjų BMS valdiklių (SmartX Controller AS-P), o skirtingų valdiklių funkcijas apjungti į vieną įrenginį - kuriamo įrenginio kompiuterį. Hibridinis įrenginys komunikuoja su išorės įrenginiais per laidinę terpę (interneto kabeliu). Tai padidina sistemos patikimumą, be to, supaprastėjo įrenginio instaliavimas.

**2. Išspręstas neapibrėžtumas:** kaip užtikrinti įvairių pastato funkcionavimą palaikančių sistemų patikimą kontrolę?

Hibridiniame įrenginyje naudojami mikrovaldikliai ir mikroprocesoriai pastato efektyviam energijos valdymui ir greitam duomenų apdorojimui.

Integruoti standartiniai, plačiai paplitę komunikacijos protokolai (ModBus, BACNet) užtikrins įrenginio sąveiką su įvairiomis sistemomis. Tačiau, įvertinus tai, kad įprasti protokolų keitikliai dažnai negali patenkinti visų techninių reikalavimų, nes jie apima tik pagrindines funkcijas, priimtas sprendimas naudoti atskirus protokolų keitiklius, atliekančius specifines funkcijas tam tikram išoriniam moduliui. Šie keitikliai palaikys ir mažiau populiarius arba nestandartinius protokolus, kuriems nėra rinkoje universalių sprendimų. Taip pat vienu metu bus galima palaikyti kelis protokolus ir tiesiogiai bendrauti su valdymo sistema per centralizuotą sąsają. Toks sprendimas leis optimizuoti konversijos procesus (sumažinti atsako laiką, padidinti sistemos reakcijos greitį ir duomenų perdavimo efektyvumą).

Taip pat tiesioginė vidinė komunikacija su valdančiuoju kompiuteriu sumažina duomenų srauto delsą, kas yra ypač svarbu realaus laiko sistemoms, pasiekiant aukštesnį funkcionalumo, universalumo, saugumo ir sistemos našumo lygį. Tokie keitikliai taip pat leidžia ir lengviau prisitaikyti prie ateities poreikių.

**3. Išspręstas neapibrėžtumas:** kaip realizuoti black box išmaniąsias funkcijas(*subscribe, discovery, plug&play*), kurios bus paremtos protokolų keitikliais?

Aprašyti

**III.** Sukurti matematinį ir/arba kompiuterinį modelį, aprašantį hibridinio įrenginio veikimą

Sudarytas visos protokolų keitiklio kaip juodos dėžės (angl. black box) sistemos tinklo modelis. Parametrizuoti įvairūs hibridinio įrenginio mazgai (pagrindinis valdymo įrenginys, protokolų keitiklis ir pan.), modeliuojant įvairias srauto charakteristikas: sukuriamų užklausų srautų intensyvumą, apdorojimo intensyvumą, skirtingų protokolų atsako laiką, apkrovos pasiskirstymą tinkle ir pan. Modeliuojant srautus buvo taikomi *Puasono* procesai arba *Markovo* modeliai, kurie leido nustatyti kiek jutiklių gali būti aptarnaujama efektyviai, arba koks turi būti užklausų dažnis, kuris užtikrina optimalų duomenų surinkimą, neviršijant sisteminių resursų ribų.

Nustatyta, jog, nors komutatorius užtikrina aukštą pralaidumą, tačiau kritinė sąsaja yra tarp pagrindinio valdymo įrenginio ir komutatoriaus, nes per ją perduodamos visos užklausos ir atsakymai. Modeliavimas padėjo nustatyti, kokio pralaidumo turėtų būti ryšio sąsajos, koks yra optimalus užklausų intensyvumas ir kaip paskirstyti apkrovą tarp jutiklių ir valdiklių.

Taip pat modeliavimas leido įvertinti apkrovas skirtinguose tinklo segmentuose, duomenų paketų vėlinimą ir praradimus, dinaminius tinklo pokyčius ir reagavimo strategijas.

Pagrindinis valdiklis ir protokolų valdikliai gali inicijuoti užklausas galiniams įrenginiams, todėl analitinis modelis padėjo nustatyti, kaip tinkamai paskirstyti ar valdyti srautus tarp skirtingų technologijų keitiklių, kad būtų išvengta perteklinio apkrovimo.

**1. Išspręstas neapibrėžtumas**: kiek jutiklių gali būti efektyviai aptarnaujama hibridinio įrenginio arba koks turėtų būti užklausų dažnis, kuris užtikrina optimalų duomenų surinkimą, neviršijant sisteminių resursų ribų?

Kadangi MQTT, M-bus, DALI, Modbus ir CAN įrenginiai turi ribotą komunikacijos spartą, buvo būtina įvertinti valdiklio užklausų dažnio įtaką minėtų įrenginių veikimui. Jei užklausos siunčiamos per dažnai, duomenys prarandami arba atsiranda dideli vėlinimai. Jei registruojamų duomenų reikšmės kinta lėtai, tai nėra pagrindo siųsti užklausas dideliu intensyvumu – tokiu atveju duomenų bazėje galimai kauptųsi pertekliniai duomenys, o tinklo mazgai būtų be reikalo apkraunami. Minimalus užklausų dažnis pagal klasikinę diskretizavimo teoriją, turi būti bent daugiau nei dvigubai didesnis už registruojamų parametrų kitimo dažnį, arba turi būti parenkamas pagal konkrečią specifiką.

Nors komutatorius ir užtikrina aukštą pralaidumą (kokios jo charakteristikos?), kritinė sąsaja yra tarp pagrindinio valdymo įrenginio ir komutatoriaus, nes per ją perduodamos visos užklausos ir atsakymai. Gauti rezultatai leido įvertinti optimalų duomenų srauto intensyvumą, kuris priklauso nuo dviejų pagrindinių veiksnių: 1) nuo techninės įrangos ar protokolo, naudojamo duomenims surinkti, ypatybių t. y. kokiu dažniu ir per kiek laiko įrenginiai gali atsakyti į užklausas, ir 2) nuo optimizavimo kriterijų, pagal kuriuos vertinamas surinkimo proceso efektyvumas, pavyzdžiui, ar siekiama minimizuoti tinklo apkrovą, ar kuo greičiau atnaujinti visų duomenų taškų reikšmes.

Tai kiek konkrečiai jutiklių galėtų būti efektyviai aptarnaujama hibridinio įrenginio?

**2. Išspręstas neapibrėžtumas**: kokie turi būti parenkami apdorojančio mazgo resursai bei ryšio magistralės pralaidumas?

Vertinant poreikį magistralės pralaidumui, reikėjo atsižvelgti į tai, koks bus užklausų duomenų surinkimo intensyvumas (arba periodas) ir kokio dydžio duomenų paketai bus suformuojami, priklausomai nuo protokolo tipo ir juose talpinamų duomenų. Kokie protokolai bus naudojami ir kiek duomenų sugeneruojama, paprastai, priklauso nuo to, iš kokių galinių įrenginių bus nuskaitomi duomenys. Pagal tai buvo galima įvertinti sukuriamų užklausų ir atsakų į jas duomenų paketų dydžius. Tam galima buvo panaudoti tipinius paketų dydžius skirtingiems protokolams arba pasiūlyta naudoti analitinio bei imitacinio modelio funkcijas, kurios apskaičiuoja duomenų paketų dydžius. Tai leido įvertinti kiek laiko truks duomenų surinkimas ir perdavimas (apskaičiuojamas reikiamas aptarnavimo intensyvumas), ir pagal tai apsprendžiami reikiamo dydžio resursai apdorojančiame mazge bei ryšio magistralėje. Tai žinant, galima apskaičiuoti kokia yra sugeneruojama duomenų sparta, pagal kurią parenkami įrangos ir kanalų pralaidumai (turi būti už ją didesni). Modeliavimo rezultatuose tai atitiko atvejus, kai paraiškų intensyvumas yra mažesnis už paraiškų aptarnavimo intensyvumą.

Kaip rodo atliktų tyrimų rezultatai, jei paraiškų atėjimo intensyvumas yra mažesnis nei 60-70% paraiškų aptarnavimo intensyvumo, tai net ir esant atsitiktiniam srautų pobūdžiui ir vėlinimas, ir blokavimo tikimybė bus nereikšmingi. Tai kokio dydžio resursai turi būti konkrečiai?

**3.** **Išspręstas neapibrėžtumas**: kokio pralaidumo *Ethernet* kanalo reikia tarp pagrindinio valdymo mazgo ir komutatoriaus?

Žemesnės hierarchijos valdikliai surenka duomenis iš jiems pavaldžių galinių įrenginių per magistrales, kurių duomenų sparta yra daug kartų mažesnė nei juos jungiančio *Ethernet* komutatoriaus. Nustatyta, kad būtent šie valdikliai, kurie surenka duomenis iš jiems pavaldžių galinių įrenginių per magistrales, turi didžiausią įtaką bendram duomenų surinkimo vėlinimui. Todėl iš jų sukuriamas duomenų srautas nesudaro reikšmingos apkrovos duomenų kanale, kuris yra tarp pagrindinio valdiklio ir komutatoriaus. Priešingu atveju reikėtų arba pasirinkti didesnės spartos *Ethernet* komutatorių arba dalį perteklinę apkrovą generuojančių žemesnės hierarchijos valdiklių prijungti prie kito pagrindinio valdiklio. Tai kokio pralaidumo *Ethernet* kanalo reikia tarp pagrindinio valdiklio ir komutatoriaus?

**IV.** Virtualiame modelyje taikyti skirtingus integravimo ir optimizavimo metodus, siekiant išsiaiškinti, kurie komponentai apjungti tarpusavyje veikia geriausiai

**1. Išspręstas neapibrėžtumas:** kokios spartos duomenų perdavimo magistralė turėtų būti naudojama, siekiant išvengti duomenų blokavimo?

Iš pateiktų priklausomybių nustatytas leistinas duomenų srauto intensyvumas $λ\_{mcuΣ}$, pagal tam tikrą blokavimo tikimybės $P\_{b md}$ ribą, kuri neturėtų būti viršyta. Tai leido apspręsti poreikį duomenų perdavimo magistralės dydžiui, kuris turi būti.....

**2. Išspręstas neapibrėžtumas:** kiek protokolų valdiklių būtina numatyti projektuojamame hibridiniame įrenginyje, siekiant užtikrinti reikiamas duomenų srauto apdorojimo charakteristikas?

Atliktas tyrimas atskleidė protokolų valdiklių skaičiaus poreikį, tiriant situaciją, kai pagrindinio valdymo įrenginio generuojamų paraiškų srautas yra paskirstytas tarp kelių protokolų valdiklių.

Modeliuojant protokolų keitiklio parametrus, sudarytas BACnet IP protokolo pagrindu veikiančio protokolų keitiklio modelis, kuriame panaudoti 4 žemesnės hierarchijos protokolų valdikliai, nuskaitantys iš jiems pavaldžių įrenginių duomenis. Paketų dydžiai buvo apskaičiuoti automatiškai, panaudojus tam sukurtas funkcijas (kiek objektų yra duomenų pakete, koks transportinis protokolas naudojamas ir ar naudojami masyvo indeksų masyvai). Kontrolei apskaičiuoti paketų dydžiai buvo patikrinti su realiais duomenimis (*Wireshark* pagalba). Tai leido modeliuoti situaciją su rezervavimo scenarijais, taip pat įvertinti, kokią įtaką srautų paskirstymas turi jų perdavimo ir aptarnavimo parametrams. Akivaizdu, kad kuo daugiau protokolų valdiklių įrenginyje, tarp kurių paskirstomas bendras pagrindinio valdymo įrenginio generuojamų paraiškų srautas, tuo jiems tenka mažesnė apkrova. Gautos priklausomybės leido įvertinti protokolų valdiklių kiekį, būtiną siekiant tam tikro kriterijaus, pavyzdžiui, kad nebūtų viršyta tam tikra kritinė $W\_{md}$ arba $P\_{b md}$ vertė. Nustatyta, jog būtinas protokolų valdiklių kiekis turi būti....

**3. Išspręstas neapibrėžtumas:** kokią būtina parinkti protokolų valdiklio buferio talpą?

Įvertinus ateinančio duomenų srauto iš skirtingų BAS valdomų įrenginių intensyvumą ir kad laikotarpiai tarp jų yra nevienodi, sudarytos priklausomybės leido nustatyti protokolų valdiklio buferio talpos poreikį, siekiant sumažinti duomenų blokavimo (arba jų išmetimo dėl buferio perkrovimo) tikimybę. Nustatyta, jog....

# Veiklos vykdymo metu atliktų tyrimų eigos pakeitimai

Aprašyti darbų, kurie turėjo būti atlikti pagal MTEP veiklų planą ir faktiškai atliktų darbų skirtumus, paaiškinti, kokios aplinkybės lėmė jų atsiradimą. Išvardinti MTEP veiklų plane planuotus, bet nepasiektus užduočių rezultatus, jei tokių buvo, ir pateikti pagrindimą, kodėl jie nebuvo pasiekti. Išvardinti tolimesnių veiklų pakeitimus, jei po šios veiklos atsiranda poreikis korekcijoms ir pateikti pagrindimą, nurodant priežastis.

Nebuvo pakeitimų

# Nauda projekto rezultatams

Trumpai paaiškinti, kaip gauti veiklos rezultatai prisidėjo prie galutinio projekto rezultato, kodėl jie būtini. Rekomenduojama apimtis - 1 psl.

Būtina aptarti visų išsikeltų uždavinių rezultatus

**Literatūra**

[1] Vittori, Filippo & Fu Tan, Chuan & Pisello, Anna Laura & Chong ,Adrian & Miller, Clayton (2023). BIM-to-BRICK: Using graph modeling for IoT/BMS and spatial semantic data interoperability. arXiv preprint arXiv:2307.13197. <https://doi.org/10.48550/arXiv.2307.13197>

[2] Ożadowicz, Andrzej. (2023). Generic IoT for Smart Buildings and Field-level Automation - Challenges, Threats, Approaches and Solutions. 10.20944/preprints202312.1994.v1. <https://doi.org/10.3390/computers13020045>

[3] Mitzutani, Iori & Ramanathan, Ganesh & Mayer, Simon. (2021). Semantic data integration with DevOps to support engineering process of intelligent building automation systems. 294-297. 10.1145/3486611.3492413. <http://dx.doi.org/10.1145/3486611.3492413>

[4] Genkin, A., & McArthur, J. (2022). B-SMART: A Reference Architecture for Artificially Intelligent Autonomic Smart Buildings. Journal of Building Engineering, 57, 104942. <https://doi.org/10.48550/arXiv.2211.03219>

[5] Ranpara, Ripal. (2025). A semantic and ontology-based framework for enhancing interoperability and automation in IoT systems. Discover Internet of Things. 5. 10.1007/s43926-025-00122-8. <http://dx.doi.org/10.1007/s43926-025-00122-8>

[6] Qaswar, Fahad & Mokhtar, Rahmah & Raza, Muhammad & Ahmad, Noraziah & Alkazemi, Basem & Fauziah, Zulvy & Hassan, Mohd Khairul Azmi & Sharaf, Ahmed. (2022). Applications of Ontology in the Internet of Things: A Systematic Analysis. Electronics. 12. 111. 10.3390/electronics12010111. <http://dx.doi.org/10.3390/electronics12010111>

[7] Ruta, Michele & Scioscia, Floriano & Loseto, Giuseppe & Pinto, Agnese & Di Sciascio, Eugenio. (2018). Machine learning in the Internet of Things: A semantic-enhanced approach. Semantic Web. 10. 183-204. 10.3233/SW-180314. <http://dx.doi.org/10.3233/SW-180314>

[8] Liu, Fagui & Li, Ping & Deng, Dacheng. (2017). Device-Oriented Automatic Semantic Annotation in IoT. Journal of Sensors. 2017. 1-14. 10.1155/2017/9589064. <http://dx.doi.org/10.1155/2017/9589064>

[9] Ramanathan, G., & Mayer, S. (2024). A Match Made in Semantics: Physics‑infused Digital Twins for Smart Building Automation. arXiv preprint arXiv:2406.13247. <https://doi.org/10.48550/arXiv.2406.13247>

[10] Iddianozie, C., & Palmes, P. (2020). AI‑big data: Addressing semantic heterogeneity in building management systems using discriminative models. arXiv preprint arXiv:2008.07414. <https://doi.org/10.48550/arXiv.2008.07414>

[11] Himeur, Y & Elnour, M & Fadli, F·& Meskin, N & Petri, I & Rezgui, Y & Bensaali, F & Amira, A. (2022). AI‑big data analytics for building automation and management systems: a survey, actual challenges and future perspectives. Artificial Intelligence Review. <https://doi.org/10.1007/s10462-022-10286-2>
