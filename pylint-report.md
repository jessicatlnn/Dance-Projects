# Pylint-raportti

```text
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:16: W0613: Unused argument 'e' (unused-argument)
app.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:33:14: W0613: Unused argument 'e' (unused-argument)
app.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:37:19: W0613: Unused argument 'e' (unused-argument)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:120:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:144:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:205:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:238:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:314:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:335:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:341:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:398:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:423:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:431:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.97/10 (previous run: 8.97/10, +0.00)
```

## Docstring ilmoitukset

Suurin osa raportin ilmoituksista on seuraavanlaisia:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Tämä tarkoittaa, että funktioissa tai moduuleissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty päätös siitä, että ei käytetä docstring-kommentteja.

## Unused argument ilmoitukset

Raporteissa on muutama
```
app.py:33:14: W0613: Unused argument 'e' (unused-argument)
```
tyyppinen ilmoitus. Parametri tarvitaan Flaskin virheenkäsittelyssä, vaikka sen arvoa ei tässä sovelluksessa käytetä.
