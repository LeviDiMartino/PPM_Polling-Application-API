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
| **Utente 0** | `AuthenticatedUser0` | `SafePolls0` | Gestisce solo i propri dati, vota |
| **Utente 1** | `AuthenticatedUser1` | `SafePolls1` | Utilizzato per testare le azioni vietate |
| **Utente 2** | `AuthenticatedUser2` | `SafePolls2` | Utilizzato per aggiungere voti |
| **Utente 3** | `AuthenticatedUser3` | `SafePolls3` | Utilizzato per aggiungere voti |
| **Utente 4** | `AuthenticatedUser4` | `SafePolls4` | Utilizzato per aggiungere voti |
| **Utente 5** | `AuthenticatedUser3` | `SafePolls3` | Utilizzato per aggiungere voti |
| **Amministratore** | `admin` | `admin1234` | Controllo e moderazione globale totale |

Tutti gli utenti, compreso l'admin ed escluso l'Utente 0, hanno già espresso un voto per ogni sondaggio attualmente disponibile.
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

Di seguito sono riportate ordinatamente le istruzioni da eseguire per testare l'intera API da terminale tramite **HTTPie**. Sostituisci le stringhe come <INCOLLA_TOKEN_UTENTE_1> con il token reale ottenuto nei primi passaggi.

### Fase 1: Richieste di Accesso Pubbliche (Anonimo, nessun token)
Chiunque può consultare l'elenco dei sondaggi attivi e i relativi risultati.

1. Recupera la lista di tutti i sondaggi presenti
```bash
http --unsorted GET http://levidimartino.pythonanywhere.com/api/polls/  
```
2. Visualizza l'endpoint specifico dei risultati per il sondaggio scelto in base al ID (per scegliere un sondaggio modifica il campo id)
```bash
http GET http://levidimartino.pythonanywhere.com/api/polls/id/results/  
```

### Fase 2: Autenticazione e Creazione (Ottenimento Token JWT)
Per eseguire operazioni di scrittura, l'utente deve scambiare le proprie credenziali con un token di accesso.

3. Login dell' Utente 0 (Copia l' access token, dovrai sostituirlo nei comandi successivi) 
 (provare se si vuole a inserire prima credenziali errate da quelle specificate)

```bash
http -j POST http://levidimartino.pythonanywhere.com/api/token/ username="AuthenticatedUser0" password="SafePolls0" 
```

### Fase 3. Creazione di un nuovo sondaggio (da parte dell'Utente 1)

```bash
http --unsorted -j POST http://levidimartino.pythonanywhere.com/api/polls/ question="Quale framework preferisci per le API?" choices[0][choice_text]="Django" choices[1][choice_text]="FastAPI" choices[2][choice_text]="Flask" "Authorization: Bearer <INCOLLA_TOKEN_UTENTE_0>"
```
Prendi nota dell'ID del sondaggio restituito.  Se vuoi personalizza la domanda o le scelte tra le virgolette.
(se --unsorted da problemi rimuovilo o scrivi "--sorted=no" al suo posto)

### Fase 4: Voto e Restrizioni (Operazioni Protette, valide solo per autente Autenticato)
Utilizzando il token JWT all'interno dell'header Authorization, l'utente può ora interagire attivamente con l'applicazione.

#5. L'Utente 0 vota per un sondaggio (es. sostituisci al campo id l'ID del sondaggio che vuoi votare e dopo l'ID della tua scelta)
```bash
http POST http://levidimartino.pythonanywhere.com/api/polls/id/vote/ "Authorization: Bearer <INCOLLA_TOKEN_UTENTE_0>" choice=id 
```
#6. TEST UNICITÀ DEL VOTO: L'Utente 0 prova a votare di nuovo lo stesso sondaggio 

```bash
Riusa il comando precedente usando lo stesso ID del sondaggio (l'ID della scelta è indifferente).
```
Il sistema intercetta la violazione e risponde con: HTTP 400 Bad Request ("You have already voted in this poll.")

### Fase 5: Cancellazione di una singola opzione di risposta 
Un utente autorizzato ha il permesso di cancellare le opzioni dei sondaggi da lui creati.

Prova a sostituire il campo id con l'ID della scelta "FastAPI" di prima, per cancellarla.
```bash
http DELETE http://levidimartino.pythonanywhere.com/api/choices/id/ "Authorization: Bearer <INCOLLA_TOKEN_UTENTE_0>"
```
Se la risposta del server è: 204 No Content, significa che la cancellazione è avvenuta con successo.

### Fase 6: Test delle Restrizioni e Azioni Vietate (Security Check)
Il sistema è progettato per respingere i tentativi di violazione delle regole di business. Un utente autorizzato non può cancellare o modificare un sondaggio non suo. 

7. Fai il login dell' Utente 1 (Copia l' access token)
```bash
http -j POST http://levidimartino.pythonanywhere.com/api/token/ username="AuthenticatedUser1" password="SafePolls1" 
```
8. Prova a cancellare il sondaggio creato dall'Utente 0 (sostituisci l'ID del sondaggio nel campo <id> e inserisci il token del utente 1)
```bash
http DELETE http://levidimartino.pythonanywhere.com/api/polls/id/ "Authorization: Bearer <TOKEN_UTENTE_1>"
```
Il sistema blocca la richiesta rispondendo con: HTTP 403 Forbidden ("You do not have permission to perform this action.")

### Fase 7: Permessi Admin

Fai il login come admin
```bash
http -j POST http://levidimartino.pythonanywhere.com/api/token/ username="admin" password="admin1234"
```
Prova a cancellare il sondaggio appena creato dal Utente 0 (sostituisci il campo id con l'ID del sondaggio creato dall' Utente 0)
```bash
http DELETE http://levidimartino.pythonanywhere.com/api/polls/15/  "Authorization: Bearer <INCOLLA_TOKEN_ADMIN>"
```
Se la risposta del server è: 204 No Content, significa che la cancellazione è avvenuta con successo.

### Installazione e Avvio Locale (Opzionale)
Qualora si preferisse eseguire ed ispezionare il server in un ambiente di sviluppo locale:

```bash
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
```
