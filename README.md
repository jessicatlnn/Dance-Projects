# Tanssiprojektit

## Sovelluksen toiminnot

- Sovelluksessa käyttäjät voivat jakaa tanssiprojektejaan ja osallistua muiden käyttäjien projekteihin.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen tanssiprojekteja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään projekteja.
- Käyttäjä näkee sovellukseen lisätyt projektit. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät projektit.
- Käyttäjä pystyy etsimään tanssiprojekteja hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä projekteja.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja (esim. projektien ja osallistujien määrät) ja käyttäjän lisäämät projektit.
- Tanssiprojektille valitaan tanssityyli tietokantaan tallennetuista vaihtoehdoista (esim. Hip Hop, Commercial, Heels, Contemporary, Jazz tai Street), oma taitotaso ja projektin sijainnit. 
- Käyttäjä voi osallistua sekä omiin että muiden käyttäjien projekteihin. Projektien sivuilla näkyvät osallistujamäärät.

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


## Suuren tietomäärän käsittely

Sovellusta testattiin 10 000 projektilla ja testidataa luotiin seed.py-tiedoston avulla. Suuren tietomäärän käsittelyä varten projektien listauksessa käytetään sivutusta, jossa näytetään 10 projektia kerrallaan. Sivutus on käytössä sekä etusivulla että projektien hakutuloksissa.

Tietokantaan lisättiin indeksit projektien tanssityylille, tasolle ja sijainnille. Indeksit nopeuttavat projektien hakua erityisesti suurilla tietomäärillä.

Testauksessa sivutus ja projektien haku toimivat normaalisti 10 000 projektin tietomäärällä.
