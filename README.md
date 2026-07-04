# PPM_Polling-Application-API

* **Studente:** <Levi Di Martino Serafim>
* **Matricola:** 7083297
* **Progetto:** REST API
* **Framework:** Django / Django REST Framework

---

## 1. Descrizione
API REST per la gestione di sondaggi. Permette di consultare, creare ed eliminare quesiti e relative opzioni, garantendo l'unicità del voto per singolo utente.

---

## 2. Funzionalità e Ruoli
* **Anonimo:** Lettura lista sondaggi, dettaglio e risultati.
* **Utente Autenticato / Admin:** Creazione, modifica e cancellazione dei propri sondaggi, e registrazione di un singolo voto per sondaggio.
  
---

## 3. Prerequisiti
* Python 3.10 o superiore
* Git
---

## 4. Installazione e Avvio
```bash
git clone <URL_REPO>
cd <PPM_Polling_Application_API>
python -m venv venv
source venv/Scripts/activate  # (venv/bin/activate su Mac/Linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
4. Database DemoIl progetto include il file db.sqlite3 pre-popolato con record di test. Account disponibili:admin_demo / admin12345 (Ruolo: Admin/Superuser)user_demo / user12345 (Ruolo: Utente Standard)5. DeploymentL'API è testabile online al seguente indirizzo: <URL_DEL_DEPLOY>6. EndpointsMetodoURLAuthRuoloJSON Body (Esempio)DescrizionePOST/api/token/NoTutti{"username":"", "password":""}Rilascio TokenGET/api/polls/NoTutti-Lista sondaggiGET/api/polls/<id>/NoTutti-Dettaglio sondaggioPOST/api/polls/SìAutenticato{"question": "..."}Crea sondaggioDELETE/api/polls/<id>/SìProprietario-Elimina sondaggioPOST/api/polls/<id>/vote/SìAutenticato{"choice": <id>}Invia voto7. Test Flow (HTTPie)1. Login (Ottieni Token)Bashhttp POST [http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/) username="user_demo" password="user12345"
2. Chiamata PubblicaBashhttp GET [http://127.0.0.1:8000/api/polls/](http://127.0.0.1:8000/api/polls/)
3. Chiamata Autenticata (Creazione)Bashhttp POST [http://127.0.0.1:8000/api/polls/](http://127.0.0.1:8000/api/polls/) "Authorization: Token <TOKEN>" question="Test API?"
4. Test Azione Negata (Prova di doppio voto)Bashhttp POST [http://127.0.0.1:8000/api/polls/1/vote/](http://127.0.0.1:8000/api/polls/1/vote/) "Authorization: Token <TOKEN>" choice=1
# Lanciando il comando due volte, la seconda restituirà 400 Bad Request
