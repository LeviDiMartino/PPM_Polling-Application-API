# PPM_Polling-Application-API

* **Studente:** Levi Di Martino Serafim
* **Matricola:** 7083297
* **Progetto:** REST API
* **Framework:** Django / Django REST Framework

---

## 1. Descrizione:
API REST per la gestione di sondaggi. Permette di consultare, creare ed eliminare quesiti e relative opzioni, garantendo l'unicità del voto per singolo utente.

---

## 2. Funzionalità e Ruoli:
*  **Anonimo:** Lettura lista sondaggi e visualizzazione risultati.
*  **Utente Autenticato (Standard):** Creazione sondaggi, espressione di un singolo voto, e modifica/cancellazione esclusivamente dei *propri* sondaggi [cite: 80].
*  **Amministratore (Superuser):** Permessi totali di moderazione, inclusa la cancellazione di *qualsiasi* sondaggio presente nel database e la gestione amministrativa globale .
  
---

## 3. Prerequisiti:
* Python 3.10 o superiore
* Git
---

## 4. Installazione e Avvio:
```bash
git clone <URL_REPO>
cd <PPM_Polling_Application_API>
python -m venv venv
source venv/Scripts/activate  # (venv/bin/activate su Mac/Linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
---

##5. Database Demo:
Il progetto include il file `db.sqlite3` con dati realistici e permessi già configurati[cite: 31, 50]. Account disponibili:
* `user_demo` / `user12345` (Ruolo: Utente Standard Autenticato - Gestisce solo i propri dati) 
* `admin_demo` / `admin12345` (Ruolo: Amministratore / Superuser - Controllo e moderazione globale)

---

##6. Deployment:
L'API è testabile online al seguente indirizzo: <URL_DEL_DEPLOY>

---

##7. Endpoints:

| Metodo | URL | Auth | Ruolo Consentito | JSON Body (Esempio) | Descrizione |
|---|---|---|---|---|---|
| POST | `/api/token/` | No | Tutti | `{"username":"", "password":""}` | [cite_start]Rilascio Token [cite: 42, 64] |
| GET | `/api/polls/` | No | Tutti | - | [cite_start]Lista sondaggi [cite: 42, 80] |
| GET | `/api/polls/<id>/` | No | Tutti | - | [cite_start]Dettaglio sondaggio [cite: 42, 80] |
| POST | `/api/polls/` | Sì | Utente Autenticato / Admin | `{"question": "..."}` | [cite_start]Crea sondaggio [cite: 42, 80] |
| DELETE | `/api/polls/<id>/` | Sì | Proprietario / Admin | - | [cite_start]Elimina sondaggio (Admin cancella tutto) [cite: 42, 80] |
| POST | `/api/polls/<id>/vote/` | Sì | Utente Autenticato / Admin | `{"choice": <id>}` | [cite_start]Invia voto (Max 1 per utente) [cite: 42, 80] |
2. Chiamata PubblicaBashhttp GET [http://127.0.0.1:8000/api/polls/](http://127.0.0.1:8000/api/polls/)
3. Chiamata Autenticata (Creazione)Bashhttp POST [http://127.0.0.1:8000/api/polls/](http://127.0.0.1:8000/api/polls/) "Authorization: Token <TOKEN>" question="Test API?"
4. Test Azione Negata (Prova di doppio voto)Bashhttp POST [http://127.0.0.1:8000/api/polls/1/vote/](http://127.0.0.1:8000/api/polls/1/vote/) "Authorization: Token <TOKEN>" choice=1
# Lanciando il comando due volte, la seconda restituirà 400 Bad Request
