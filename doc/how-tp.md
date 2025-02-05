# Connection sequence

Quando il viewer si connette (via ws) al server, chiede di essere associato ad una room
Per farlo, passa ID e Secret del drawer (basic auth)

Il server, rimanda queste info al drawer, che conferma la connessione del viewer al drawer

Cose da fare:
    - Il viwer deve conosce qual è il suo drawer, per "lasciare la stanza" quando si chiude il browser
      - Questa info dovrebbe stare in sessione
    - Quindi la "login" dovrebbe essere indipendente dal ws
    - 
