# Verze 1 - na desce v1

## monitoring

Teplota: 
Dallas čidlo - čínské várky umějí být hodně nepovedené
některé mají jen posun (většinou o 1-2 st dolů) 
ale pro hrubý monitoring, že se teplota držela v hrubých mezích (10-30st? s přesností 1-2?) dostačující

Světlo: 
I2C senzor BH1750 zatím vypadá dobře
bude zase záležet na přesném usístění senzoru - ideální by bylo mít ve všech boxech na stejném mísě

Vlhost: 
aby se čidlo elektrolýzou brzy nezničilo, zapínáme jen po dobu měření
- měří se napětí vestavěným A/D převodníkem
čidlo měří poměrně nepřesně - je tam hodně šumu, měříme proto po sobě tři hodnoty a posíláme až jejich průměr 

# Verze 2 (12V) - na desce v2

## akce:

přidáváme Relé a upravený MOS-FET
relé: spíná oběhové čerpadlo - šlo by nahradid PWM (plánujeme do verze 3)

MOS-FET spíná PWM (pulsní modulace) Led pásek


## todo1902:

db rozšířit na delší ID / nebo použijeme druhou osmici (po druhé PP sklizni)

testovat čerpadlo i na PWM > verze 3 by mohla mít jen 3x PWM FET
