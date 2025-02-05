# Ethical Hacking Trojan Project

## Overzicht
Dit project bevat een Trojan-malware die verschillende functionaliteiten uitvoert op een geïnfecteerd systeem. Het is ontworpen voor educatieve doeleinden voor het vak "Ethical Hacking", waarbij verschillende modules worden gedownload en uitgevoerd.

Het project gebruikt een GitHub-repository om configuratiebestanden en modules te downloaden, en maakt gebruik van multithreading om meerdere taken tegelijk uit te voeren.

## Functies

- **Backdoor**:
  - Maakt screenshots en video van het systeem.
  - Neemt audio op (zowel invoer als uitvoer).
  
- **Network Scan**:
  - Voert netwerk scans uit om actieve apparaten, open poorten en besturingssystemen te detecteren.
  - Voert IP-geolocatie

- **Sniffer**:
  - Snifft netwerkverkeer en haalt HTTP POST-gegevens en andere netwerkpakketdetails uit.
  
## Installatie

1. **Clone deze repository**  
```bash
git clone https://github.com/Sirehtea/Ethical_Trojan.git
cd Ethical_Trojan
```

2. **Installeer requirements**  
```bash
pip install -r requirements.txt
```

3. **Setup**
- Maak een `.env` bestand en voeg je GitHub-token toe:
```
GITHUB_TOKEN=je_github_token_hier
```
- Zorg ervoor dat de `config.json` correct is ingesteld voor de gewenste modules en functies.

4. **Start applicatie**
```bash
python main.py
```

## Werking

1. Het script downloadt de configuratiebestanden en modules m.b.v. de Github token.
2. Het script controleert continu of er wijzigingen zijn in de configuratiebestand (`config.json`) op GitHub.
3. Afhankelijk van de configuratie, wordt elke module gedownload en de bijbehorende functies worden uitgevoerd.
4. De uitvoer van elke module wordt opgeslagen in de `data/` directory, onder een uniek UUID.

## Voorbeeldconfiguratie

Een voorbeeld van de configuratie in `config.json`:

```json
{
    "modules" : 
    [
        {
            "name" : "backdoor",
            "config" : 
            {
                "HOST" : "<IP-adres>",
                "PORT" : 5004,
                "BUFFER_SIZE" : 131072,

                "fps" : 12.0,

                "SAMPLE_RATE" : 48000,
                "RECORD_SEC" : 10
            },
            "functions" : 
            {
                "Screenshot" : "False",
                "Video" : "False",
                "Audio_Output" : "False",
                "Audio_Input" : "False"
            }
        },
        {
            "name" : "networkscan",
            "config" : 
            {
                "scan_range_ip" : "<IP-adres>/24",
                "target" : "<IP-adres>",
                "min" : 1,
                "max" : 1000
            },
            "functions" : 
            {
                "list_ip_and_mac" : "False",
                "list_pinged_devices" : "False",
                "scan_open_ports" : "False",
                "scan_common_open_ports" : "False",
                "OS_detection" : "False",
                "list_wifi_networks" : "False",
                "get_public_ip" : "False",
                "geolocate_ip" : "False"
            }
        },
        {
            "name" : "sniffer",
            "config" : 
            {
                "interface" : "Wi-Fi",
                "display_filter" : "http",
                "capture_duration" : 10,
                "filename" : "capture.pcap"
            },
            "functions" : 
            {
                "packet_details" : "False",
                "extract_http_post_data" : "False",
                "capture_and_save_pcap" : "False",
                "listen_dhcp" : "False"
            }
        }
    ]
}
```