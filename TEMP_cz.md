# Verze 1 - na desce v1

teplota / vlhkost / osvětlení

použito pouze v PP1 (1812)

http://www.octopusengine.org/api/hydrop/?sel=place&place=PP1&limit=3000

## monitoring - stávající a chystané

- Teplota: 

Dallas čidlo - čínské várky umějí být hodně nepovedené
některé mají jen posun (většinou o 1-2 st dolů) 
ale pro hrubý monitoring, že se teplota držela v hrubých mezích (10-30st? s přesností 1-2?) dostačující

- Světlo:

I2C senzor BH1750 zatím vypadá dobře
bude zase záležet na přesném umístění senzoru - ideální by bylo mít ve všech boxech na stejném mísě

- Vlhkost:

aby se čidlo elektrolýzou brzy nezničilo, zapínáme jen po dobu měření
měří se napětí vestavěným A/D převodníkem
čidlo měří poměrně nepřesně - je tam hodně šumu, měříme proto po sobě tři hodnoty a posíláme až jejich průměr 

- PH:

Zatím jen v laboratorních podmínkách jednoho boxu v octopusLAB


- Konduktivita:

Zkusíme vyvinout vlastní hrubý konduktometr, bylo by možné ho osadit do všech boxů, když bude levný, jednoduchý, stabilní a dávat relevantní hodnoty v přijatelném rozmezí

- Průtokoměr

asi také osadíme jen v jdnom boxu - mohlo by se sledovat, že třba klesá průtok? zanášení čerpadla? a pod


# Verze 2 (12V) - na desce v2

testováno (1902) v octopusLAB a určeno do prvních 5-6 mini interiérových 3x3 boxů

http://www.octopusengine.org/api/hydrop/?sel=place&place=octopus1&limit=3000


## akce:

přidáváme Relé a upravený MOS-FET

relé: 

spíná oběhové čerpadlo - šlo by nahradid PWM (plánujeme do verze 3)


MOS-FET spíná PWM (pulsní modulace) Led pásek

# Verze 3 - 

HW: ? samostatná GARDEN-board, 3x PWM, specifická čidla přímo přopojitelná, možná jen známka ESP? SMD ledky a pod
použitelná jsko IoT - vyráběná již osazená?

odlasit krabičku, konektory a pod

## todo1903:

- frontend:
experimenty s reactem, možná i Google data a Grafana?

- webové setup rozhraní

alfa:
https://www.octopusengine.org/api/hydrop/setup.php



x) db rozšířit na delší ID / nebo použijeme druhou osmici (po druhé PP sklizni)

- otestovat čerpadlo i na PWM > verze 3 by mohla mít jen 3x PWM FET
