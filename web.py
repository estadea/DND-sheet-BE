#----------------------# REQUISITI E FUNZIONI #----------------------#

# AGGIUNGI UTENTE è implementato da aggiungiUtente()

# RIMUOVI UTENTE è implementato da rimuoviUtente()

# AGGIORNA DATABASE è implementato da aggiornaDatabase()

# MODIFICA UTENTE è implementato da modificaUtente()


#----------------------# IMPLEMENTAZIONE ADMIN (WEB) #----------------------#

# ESEGUIRE UNA POST CON username e password
@app.route('/admin', methods=['POST', 'GET'])

def admin_login():

    if request.method == 'POST':
        id = valid_login(request.form['username'], request.form['password'])
        
        if not admin(id):
            return 'False'

        if id:
            if len(id) == 1:
                return {"id": id[0]}

    return 'False'


# ESEGUIRE UNA POST CON PARAMETRI ID dell'admin, username, email, password, ruolo
@app.route('/aggiungiUtente', methods=['POST', 'GET'])

def aggiungiUtente():
   
    if request.method == 'GET':
        return "Utilizzare una POST"
    
    if not admin(request.form['ID']):
        return 'Non autorizzato'

    if not check(request.form['username']) or not check(request.form['email']) or not check(request.form['ruolo']):
        return "Niente sql Injection qui"

    password = request.form['password']

    password = hashlib.sha256(password.encode()).hexdigest()

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Utenti (username, email, password, ruolo) VALUES ('{}','{}','{}','{}')".format(request.form['username'], request.form['email'], password, request.form['ruolo']))
    mydb.commit()
    return 'Utente aggiunto'

# ESEGUIRE UNA POST CON PARAMETRI username e ID dell'admin
@app.route('/rimuoviUtente', methods=['POST', 'GET'])

def rimuoviUtente():
    
    if request.method == 'GET':
        return "Utilizzare una POST"
    
    if not admin(request.form['ID']):
        return 'Non autorizzato'

    if not check(request.form['username']):
        return "Niente sql Injection qui"
    
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Utenti WHERE username = '{}'".format(request.form['username'])) 
    mydb.commit()
    return 'Eliminazione avvenuta'


# ESEGUIRE UNA POST CON PARAMETRI ID dell'admin, column  value e username (colonna da modificare,valore da inserire e utente da modificare) 
@app.route('/modificaUtente', methods=['POST', 'GET'])

def modificaUtente():

    value = request.form['value']
    column = request.form['column']
    username = request.form['username']
    
    if request.method == 'GET':
        return "Utilizzare una POST"
    

    if not admin(request.form['ID']):
        return 'Non autorizzato'

    if not check(column) or not check(value) or not check(username):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE  Utenti SET {} ='{}' WHERE username = '{}'".format(request.form['column'], request.form['value'], request.form['username']))
    mydb.commit()
    return 'Utente Modificato'


# ESEGUIRE UNA POST CON PARAMETRI Nome, Descrizione, CD, Livello, TS, Classe
@app.route('/aggiornaDatabase', methods=['POST', 'GET'])

def aggiornaDatabase():

    if request.method == 'GET':
        return "Utilizzare una POST"

    if not admin(request.form['ID']): 
        return 'Non autorizzato'
    
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Incantesimo VALUES ('{}','{}','{}','{}','{}','{}')".format(request.form['Nome'], request.form['Descrizione'], request.form['CD'], request.form['Livello'],request.form['TS'], request.form['Classe']))
    mydb.commit()
    return 'Incantesimo aggiunto'


