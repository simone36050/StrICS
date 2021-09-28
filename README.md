# StrICS
Questo software usa il feed RSS del Ministero delle infrastrutture e dei trasporti per generare un calendario in formato ICS con gli scioperi.

È anche possibile mettere dei filtri in base al tipo di sciopero (ferroviario, aereo, ...) e in base alla rilevanza (nazionale, regionale, ...).

## In produzione
È possibile mettere in produzione il software, è necessario un server web che supporta PHP, inoltre Python3 deve essere installato nella macchina. In alternativa l'ho messo in produzione io, è raggiungibile da qui: https://apps.simone36050.it/strikes/calendar.php. 

## Filtro
Per impostare un filtro devi aggiungere dei parametri nell'URL.

Esempio:
https://apps.simone36050.it/strikes/calendar.php?filters[]=trasporto%20pubblico%20locale%7Cvicenza&filters[]=trasporto%20pubblico%20locale%7Ctrento&filters[]=Ferroviario%7Ctrentino-alto%20adige&filters[]=Ferroviario%7Cveneto

In questo modo si ottengono solo eventi riferiti a:
- Trasporto pubblico locale di Vicenza
- Trasporto pubblico locale di Trento
- Ferroviario del Veneto
- Ferroviario del Trentino-Alto Adige
