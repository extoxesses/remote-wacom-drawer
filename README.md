# Remote Wacom Drawer

## Architettura

L'applicazione ha tre componenti principali:

1. **Server** ([server.py](server.py))
   - Server Flask/SocketIO che gestisce le connessioni WebSocket e l'instradamento degli eventi
   - Utilizza Redis per la gestione delle sessioni e MongoDB per la persistenza dei dati
   - Gestisce le stanze per le connessioni drawer/viewer
   - Implementato in Python usando Flask e Flask-SocketIO

2. **Drawing Client** ([app.py](app.py))
   - Client Python che cattura l'input del tablet/stylus
   - Utilizza pyautogui per simulare i movimenti del mouse
   - Si connette al server tramite WebSocket
   - Gestisce la calibrazione tra le dimensioni dello schermo

3. **Web Viewer** ([resources/templates/viewer.html](resources/templates/viewer.html))
   - Interfaccia web per visualizzare il disegno in tempo reale
   - Canvas HTML5 per il rendering
   - Si connette al server tramite WebSocket
   - Supporta sia la modalità normale che la modalità "lavagna"

## Funzionalità Principali

1. **Disegno in Tempo Reale**
   - Gli eventi di disegno vengono catturati e trasmessi tramite WebSocket
   - Supporta i movimenti del mouse, i clic e la sensibilità alla pressione
   - Calibrazione dello schermo per gestire diverse dimensioni di display

2. **Modalità di Disegno**
   - Modalità normale con ombra/traccia del cursore
   - Modalità lavagna per il disegno diretto
   - Supporto per la gomma tramite il pulsante secondario

3. **Gestione delle Stanze**
   - I drawer possono creare stanze
   - Più viewer possono connettersi a un drawer
   - Autenticazione tramite chiavi API e segreti

4. **Eventi WebSocket** ([commons/topic.py](commons/topic.py))
   - `mouse/move`: Aggiornamenti della posizione del cursore
   - `mouse/click`: Eventi dei pulsanti del mouse
   - `screen/calibration`: Sincronizzazione delle dimensioni del display

## Componenti Chiave

### Lato Server

- [`WebsocketService`](server/service/websocket_service.py): Gestisce le connessioni WebSocket e la gestione delle stanze
- [`SessionService`](server/service/session_service.py): Gestisce le sessioni utente e l'autenticazione
- [`MongoDbService`](server/service/mongodb_service.py): Gestisce la persistenza dei dati

### Lato Client

- [`websocket_api.py`](app/api/websocket_api.py): Gestori degli eventi WebSocket del client
- [`WebsocketService`](app/service/websocket_service.py): Servizio lato client per la gestione dell'input
- [`drawer.js`](resources/static/js/drawer.js): Funzionalità di disegno dell'interfaccia web

## Setup

L'applicazione richiede:
- Ambiente Python per server e client
- Redis per la gestione delle sessioni
- MongoDB per la persistenza dei dati (opzionale)
- Docker per le dipendenze di sviluppo

Un file Docker Compose ([docker/docker-compose.yaml](docker/docker-compose.yaml)) è fornito per configurare Redis e MongoDB.

L'applicazione utilizza variabili d'ambiente per la configurazione, definite in [.env](.env).

Questa è un'applicazione complessa che dimostra la comunicazione WebSocket, la gestione degli eventi in tempo reale e la sincronizzazione dell'input tra dispositivi, principalmente focalizzata sull'abilitazione delle capacità di disegno remoto.

## Environment Setup
```bash
python -m venv .venv-server
source .venv-server/bin/activate
pip install -r requirements.txt
```

Or in PowerShell:
```powershell
python -m venv .venv-server
.venv-server\Scripts\activate
pip install -r requirements.txt
```
