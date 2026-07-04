# PPM_Polling-Application-API

**Studente:** Levi Di Martino Serafim 
**Matricola**: 7083297  
[cite_start]**Tipologia Progetto:** REST API   
[cite_start]**Framework utilizzato:** Django / Django REST Framework   

---

## 1. Descrizione del Progetto
[cite_start]L'applicazione fornisce un set completo di API REST per la gestione di sondaggi online. [cite_start]Il sistema permette la creazione di quesiti, la gestione delle opzioni di risposta e la registrazione dei voti da parte degli utenti, garantendo l'integrità dei dati e impedendo votazioni multiple dallo stesso account attraverso controlli lato server.

---

## 2. Funzionalità e Ruoli Utente

### Utente Anonimo (Non Autenticato)
* [cite_start]Consultazione della lista dei sondaggi disponibili.
* [cite_start]Visualizzazione dei dettagli di un singolo sondaggio e dei relativi risultati in tempo reale.

### Utente Autenticato (Standard / Admin)
* [cite_start]Tutte le operazioni consentite all'utente anonimo.
* [cite_start]Creazione di nuovi sondaggi completi di opzioni di risposta.
* [cite_start]Modifica e cancellazione dei propri sondaggi.
* [cite_start]Espressione di un singolo voto per ciascun sondaggio (il sistema impedisce il doppio voto).

---

## 3. Installazione e Avvio Locale

### Prerequisiti
* Python 3.10 o superiore
* Git

### Procedura di avvio
1. Clonare il repository GitHub:
   ```bash
   git clone <URL_DEL_TUO_REPOSITORY>
   cd <PPM_Polling_Application_API>
