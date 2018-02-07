Poster
====

### Requisiti
* python3
* pip

### Dipendenze

Le dipendenze sono specificate nel file _requirements.txt_.  
Per installarle esegui il comando
```
pip install -r requirements.txt
```

### Configurazione

È necessario definire una variabile contentente la chiave api del progetto firebase da utilizare:
```
export SNAKE_API_KEY="000000000000000000000000000000000000000"
```

### Utenti

È necessario l'utilizzo di un utente autorizzato. Gli utenti vanno creati dalla dashboard del
progetto firebase stesso.

### Utilizzo

Eseguire lo script tramite il comando

```
gunicorn main:app
```

In seguito, aprire l'indirizzo riportato nel browser (di default dovrebbe essere _localhost:8000_)

