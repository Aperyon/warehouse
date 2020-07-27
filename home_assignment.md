# Backend Position Home Assignment

Üdv!

A feladat esemény-vezérelt raktárkezelés. Az egyszerűség kedvéért kétféle eseménnyel kell dolgoznod:

* készletfeltöltés - új készlet érkezik a boltba (event_type: "incoming")
* eladás - a boltban lévő termékből x db-ot eladtak (event_type: "sale")

## A rendszer 4 komponensből fog állni:

* importer: adatok feldolgozása
* kafka: feldolgozott adatok továbbítása (message bus)
* service: feldolgozott adatok kiértékelése és raktárkészlet frissítés
* postgres: aktuális raktárkészlet állapot perzisztálása

Gondolom kitaláltad, hogy ezen a ponton a négy komponensből kettőt neked kell majd implementálni:

* Az importer komponsens egy adott mappában csv fájlokat keres és megfelelő formátumban felpakolja az events nevű kafka topic-ra.
* A service nevű komponens figyeli az events kafka topic-ot és ha új esemény érkezik frissíti az adatbázisban tárolt állapotot.

Mivel mind a küldő, mind a fogadó oldalt te implementálod, ezért az üzenetekhez használt adat-formátumot teljesen rád bízzuk. A service alatti postgresql adatbázis sémájának kialakítása is a te feladatod. Példa csv fájokat csatolva megtalálod.

## Egyéb követelmények / szempontok 

Néha előfordulhatnak hibás formátumú csv-k, melyekben egy vagy több érték hiányzik, esetleg bizonyos értékek típusa eltér. Ilyen esetekben az importer logoljon hibát, de indokolatlanul ne halljon meg. Egyetlen sorban szereplő hiba ne vezessen egy egész fájl elvesztéséhez.

Mivel a boltok nem tudnak olyan terméket eladni, ami nem létezik, ezért a negatív készlet nem fordulhat elő. A service-ben kezeld ezt az esetet. Szerinted mi lenne egy jó hibakezelési stratégia ebben az esetben?

Meghibásodások, leállások esetén előfordulhat, hogy bizonyos üzenetek többször is kiolvasásra kerülnek. Készítsd fel erre a rendszert!
