# PPM_Polling-Application-API 📊

* **Studente:** Levi Di Martino Serafim
* **Matricola:** 7083297
* **Progetto:** REST API (Traccia 6)
* **Framework:** Django 5 / Django REST Framework
* **Autenticazione:** JWT (JSON Web Tokens)

---

## 1. Descrizione
API REST per la gestione di sondaggi in tempo reale. Il sistema permette di consultare, creare, votare ed eliminare quesiti e relative opzioni (choices). L'applicazione implementa logiche di controllo stringenti sia sui permessi di modifica che sull'unicità del voto per singolo utente.

---

## 2. Funzionalità e Ruoli
* **Anonimo:** Può visualizzare la lista dei sondaggi, i singoli dettagli e i risultati in tempo reale.
* **Utente Autenticato (Standard):** Può creare nuovi sondaggi, esprimere al massimo un singolo voto per sondaggio e modificare/cancellare esclusivamente i sondaggi da lui creati (*Object-level permissions*).
* **Amministratore (Superuser):** Possiede permessi totali di moderazione globale, inclusa la cancellazione di qualsiasi sondaggio o voto presente nel database.

---

## 3. Deployment & Database Demo
L'API è pubblicata in cloud ed è pienamente operativa al seguente indirizzo:
🌐 **[http://levidimartino.pythonanywhere.com/api/](http://levidimartino.pythonanywhere.com/api/)**

Il database di produzione include già dati realistici di test. Per le verifiche sono disponibili i seguenti account pre-configurati:

| Ruolo | Username | Password | Permessi operativi |
| :--- | :--- | :--- | :--- |
| **Utente Standard 1** | `user_demo` | `user12345` | Gestisce solo i propri dati, vota |
| **Utente Standard 2** | `user_demo2` | `user12345` | Utilizzato per testare le azioni vietate |
| **Amministratore** | `admin_demo` | `admin12345` | Controllo e moderazione globale totale |

---

## 4. Endpoints dell'Applicazione

| Metodo | URL | Auth | JSON Body (Esempio) | Descrizione |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/token/` | No | `{"username": "...", "password": "..."}` | Ottenimento Token JWT (Access & Refresh) |
| **GET** | `/api/polls/` | No | - | Lista globale dei sondaggi |
| **GET** | `/api/polls/<id>/` | No | - | Dettaglio singolo sondaggio (con opzioni annidate) |
| **GET** | `/api/polls/<id>/results/` | No | - | Endpoint dedicato ai soli risultati del sondaggio |
| **POST** | `/api/polls/` | **Sì (JWT)** | `{"question": "Testo domanda?"}` | Creazione di un nuovo sondaggio |
| **DELETE**| `/api/polls/<id>/` | **Sì (JWT)** | - | Cancellazione sondaggio (Solo proprietario o Admin) |
| **POST** | `/api/polls/<id>/vote/` | **Sì (JWT)** | `{"choice": <id_opzione>}` | Invio votazione (Max 1 voto per utente) |

---

## 5. Scenario di Test Guidato (con HTTPie)

Di seguito viene riportato il flusso logico sequenziale consigliato per testare l'intera API direttamente da terminale tramite **HTTPie**.

### Fase 1: Richieste Pubbliche (Anonimo)
Chiunque può consultare l'elenco dei sondaggi attivi e i relativi risultati.

```bash
# 1. Recupera la lista di tutti i sondaggi presenti
http GET [http://levidimartino.pythonanywhere.com/api/polls/](http://levidimartino.pythonanywhere.com/api/polls/)

# 2. Visualizza l'endpoint specifico dei risultati per il sondaggio ID 1
http GET [http://levidimartino.pythonanywhere.com/api/polls/1/results/](http://levidimartino.pythonanywhere.com/api/polls/1/results/)
```
Fase 2: Autenticazione (Ottenimento Token JWT)
Per eseguire operazioni di scrittura, l'utente deve scambiare le proprie credenziali con un token di accesso.

# 3. Esegui il login con l'utente standard
http POST [http://levidimartino.pythonanywhere.com/api/token/](http://levidimartino.pythonanywhere.com/api/token/) username="user_demo" password="user12345"

Nota per il testing: Copia il valore della stringa access ricevuta nel JSON di risposta. Sostituisci questo valore nei comandi successivi al posto della dicitura <INSERISCI_TOKEN_ACCESS>.
```
Fase 3: Operazioni Protette (Autenticato)
Utilizzando il token JWT all'interno dell'header Authorization, l'utente può ora interagire attivamente con l'applicazione.

# 4. Creazione di un nuovo sondaggio personale
http POST [http://levidimartino.pythonanywhere.com/api/polls/](http://levidimartino.pythonanywhere.com/api/polls/) \
  "Authorization: Bearer <INSERISCI_TOKEN_ACCESS>" \
  question="Quale framework preferisci per lo sviluppo delle REST API?"

# 5. Invio di un voto per una scelta specifica (es. opzione ID 1 sul sondaggio ID 1, altrimenti cambia ID tra quelli possibili)

http POST [http://levidimartino.pythonanywhere.com/api/polls/1/vote/](http://levidimartino.pythonanywhere.com/api/polls/1/vote/) \
  "Authorization: Bearer <INSERISCI_TOKEN_ACCESS>" \
  choice=1
```
Fase 4: Test delle Restrizioni e Azioni Vietate (Security Check)
Il sistema è progettato per respingere tempestivamente i tentativi di violazione delle regole di business.

# 6. TEST DOPPIO VOTO (Restrizione unicità)
# Esegui nuovamente lo stesso identico comando di voto precedente:
http POST [http://levidimartino.pythonanywhere.com/api/polls/1/vote/](http://levidimartino.pythonanywhere.com/api/polls/1/vote/) \
  "Authorization: Bearer <INSERISCI_TOKEN_ACCESS>" \
  choice=1
# Il sistema intercetta la violazione e risponde con: HTTP 400 Bad Request ("You have already voted in this poll.")

# 7. TEST PERMESSI DI OGGETTO (Restrizione modifica/cancellazione)
# Richiedi un token per l'utente 'user_demo2' e prova a cancellare il sondaggio ID 1 (creato da un altro utente):
http DELETE [http://levidimartino.pythonanywhere.com/api/polls/1/](http://levidimartino.pythonanywhere.com/api/polls/1/) \
  "Authorization: Bearer <TOKEN_DI_USER_DEMO_2>"
# Il sistema blocca la richiesta rispondendo con: HTTP 403 Forbidden ("You do not have permission to perform this action.")
```
6. Installazione e Avvio Locale (Opzionale)
Qualora si preferisse eseguire ed ispezionare il server in un ambiente di sviluppo locale:

# Clonazione ed accesso alla cartella
git clone <URL_DELLA_REPOSITOR_GITHUB>
cd PPM_Polling-Application-API

# Configurazione dell'ambiente virtuale Python
python -m venv venv
source venv/Scripts/activate  # Su Windows usa: venv\Scripts\activate

# Installazione dipendenze e avvio
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Il server locale sarà raggiungibile all'indirizzo standard http://127.0.0.1:8000/.
