# Ethical Hacking - Python Trojan
*door: Turgay Yasar*

## Bevindingen

- Een Trojan is een soort malware die zich voordoet als legitieme software, maar die in werkelijkheid kwaadaardige intenties heeft. Het kan bijvoorbeeld gegevens stelen, systemen ondermijnen of zelfs volledige controle over een computer verkrijgen.
<br>
- Trojans kunnen veel verschillende functies uitvoeren afhankelijk van hun ontwerp, zoals het creëren van backdoors, het uitvoeren van keylogging, het onderscheppen van netwerkverkeer, of het starten van DDoS-aanvallen. De veelzijdigheid maakt Trojans gevaarlijke tools voor hackers.

## Keuzes

- Backdoor: De backdoor-module zorgt voor verborgen toegang tot het geïnfecteerde systeem via TCP- of HTTP-verbindingen. Hiermee kan ik op afstand commando’s uitvoeren en toegang behouden tot het systeem.
<br>
- Networkscan: Deze module wordt gebruikt om netwerken te scannen en open poorten te identificeren. Dit helpt bij het vinden van mogelijke toegangspunten in het netwerk, zoals onbeveiligde poorten, en maakt het makkelijker om kwetsbaarheden te ontdekken.
<br>
- Sniffer: De sniffer-module monitort netwerkverkeer op het geïnfecteerde systeem. Het logt HTTP-verzoeken en -antwoorden om gevoelige informatie, zoals logingegevens, te onderscheppen. Deze module biedt inzichten in de communicatie van de gebruiker, wat kan helpen bij het verzamelen van gevoelige gegevens.

### interessante libraries

om de functionaliteiten van deze modules te kunnen implementeren heb ik veel libraries gebruikt. De interessante zijn:

- pyshark: Gebruikt voor het analyseren van netwerkverkeer en het extraheren van informatie uit netwerkpakketten. Het is een handige tool voor het implementeren van de sniffer-module.
<br>
- scapy: Essentieel voor het uitvoeren van netwerkscans, omdat het de mogelijkheid biedt om netwerkverkeer te creëren, analyseren en manipuleren. Het ondersteunt allerlei netwerkprotocollen, waardoor het ideaal is voor het scannen van poorten en het uitvoeren van andere netwerkgerelateerde aanvallen.
<br>
- socket: Cruciaal voor het implementeren van de `reverse_shell()` functie in de backdoor module. Het maakt het mogelijk om netwerkverbindingen te maken en te beheren, zodat de Trojan op afstand kan communiceren met de server en de aanvaller toegang kan krijgen tot het geïnfecteerde systeem.

## uitdagingen 

- De documentatie van de libraries die ik heb gebruikt waren vrij gemakkelijk om te volgen
<br>
- Bij bepaalde onderwerpen die ik niet helemaal meer wist, zoals asyncio en logging, heb ik mijn oude samenvattingen geraadpleegd.
<br>
- In het begin had ik print statements gebruikt om te debuggen, omdat dit makkelijk was om te zien of de Trojan werkte. Later moest ik dit aanpassen zodat de data niet meer geprint werd naar de terminal, maar in de data-directory werd opgeslagen.
<br>
- De `config.json` implementeren om bepaalde functies te kunnen uitvoeren van mijn modules vond ik in het begin moeilijk, zeker omdat ik dit eerder nooit had gedaan. Op het internet had ik dan paar voorbeelden gevonden over hoe het structuur ervan zou kunnen uitzien. 
<br>
- Het vreemde was dat de gegevens van zowel de sniffer als de networkscan module toch in hetzelfde log-bestand terechtkwamen, terwijl de code er correct uitziet:

`networkscan.py`

```py
log_dir = get_log_dir()
log_path = os.path.join(log_dir, "network_scan_results.log") #!

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename=log_path, filemode='a')
```

`sniffer.py`

```py
log_dir = get_log_dir()
log_path = os.path.join(log_dir, "sniffer_scan_results.log") #!

logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')
```

## ethische inzichten

- Trojans kunnen door kwaadwillenden gebruikt worden om toegang te krijgen tot privégegevens, systemen te saboteren of systemen te gebruiken als 'zombie' voor botnets. Dit kan leiden tot identiteitsdiefstal, financiële schade, en onzichtbare aanvallen zoals DDoS. 
<br>
- Het is belangrijk om Trojans alleen in gecontroleerde, ethische omgevingen te gebruiken, en altijd met de toestemming van de betrokkenen. Onwettig gebruik kan leiden tot juridische gevolgen.
