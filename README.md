# Tanssiprojektit

## Sovelluksen toiminnot

- Sovelluksessa käyttäjät voivat jakaa tanssiprojektejaan ja osallistua muiden käyttäjien projekteihin.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen tanssiprojekteja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään projekteja.
- Käyttäjä näkee sovellukseen lisätyt projektit. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät projektit.
- Käyttäjä pystyy etsimään tanssiprojekteja hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä projekteja.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja (esim. projektien ja osallistujien määrät) ja käyttäjän lisäämät projektit.
- Tanssiprojektille valitaan tanssityyli tietokantaan tallennetuista vaihtoehdoista (esim. Hip Hop, Commercial, Heels, Contemporary, Jazz tai Street), oma taitotaso ja projektin sijainnit. 
- Käyttäjä voi osallistua sekä omiin että muiden käyttäjien projekteihin. Projektien sivuilla näkyvät osallistujat ja osallistujamäärät.

## Sovelluksen asennus

Luo virtuaaliympäristö:
```bash
$ python3 -m venv venv
```
Aktivoi virtuaaliympäristö:
```bash
$ source venv/bin/activate
```

Asenna Flask-kirjasto:
```bash
$ pip install flask
```

Luo tietokanta ja lisää tietokannan rakenne:
```bash
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:
```bash
$ flask run
```

Sovellus löytyy osoitteesta:
`http://127.0.0.1:5000/`
