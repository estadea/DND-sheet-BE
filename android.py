#----------------------# REQUISITI E FUNZIONI #----------------------#

# LOGIN è implementato da login()

# REGISTRAZIONE è implementata da registrazione()

#----------------------# VISITATORE #----------------------#

# ESEGUIRE UNA POST CON PARAMETRI username, email, password
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        if not check(email) or not check(username) or not check(password):
            return "Niente sql Injection qui"

        mydb = connect_db()
        mycursor = mydb.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()
        mycursor.execute("INSERT into Utenti (username, email, password, ruolo) VALUES ('{}','{}', '{}', '0')".format(username, email, password))
        mydb.commit()
        return "Registrazione completata"

# ESEGUIRE UNA POST CON PARAMETRI username, password
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        id = valid_login(request.form['username'], request.form['password'])
        if id:
            if len(id) == 1:
                return {"id": id[0]}

    return 'False'




#----------------------# REQUISITI E FUNZIONI #----------------------#


# DETTAGLI INCANTESIMO, RICERA INCANTESIMO E RICERCA PER CLASSE vengono implementate da ricerca()

# VISUALIZZA LISTA PERSONAGGI è implementato da get_personaggi() 

# DETTAGLI PERSONAGGIO è implementato da get_personaggi() e get_lista_incantesimii(id)

# CREA PERSONAGGIO è implementato da crea_personaggio()

# ELIMINA PERSONAGGIO è implementato da elimina_personaggio()

# SALVA INCANTESIMO è implementato da salva_incantesimo()

# ELIMINA INCANTESIMO è implementato da elimina_incantesimo()


#----------------------# IMPLEMENTAZIONE UTENTE (ANDROID) #----------------------#

# ESEGUIRE UNA RICHIESTA con /personaggi/parametro

@app.route('/crea_personaggio', methods=['POST', 'GET'])

def crea_personaggio():
    if request.method == 'GET':
        return "Utilizzare una POST"
    
    if not check(request.form['Nome']) or not check(request.form['id_utente']) or not check(request.form['Classe']):
            return "Niente sql injection qui"
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Personaggio (Nome, Classe, id_Utente) VALUES ('{}','{}','{}')".format(request.form['Nome'], request.form['Classe'], request.form['id_utente']))
    mydb.commit()
    return 'Personaggio aggiunto'


# ESEGUIRE UNA POST Con parametro id_personaggio e id_utente
@app.route('/elimina_personaggio', methods=['POST', 'GET'])

def elimina_personaggio():

    if request.method == 'GET':
        return "Utilizzare una POST"


    if not check(request.form['id_personaggio']):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Personaggio WHERE id = '{}'".format(request.form['id_personaggio']))
    mycursor.execute ("DELETE FROM Lista_Incantesimo WHERE id_personaggio = {}".format(request.form['id_personaggio']))
    mydb.commit()
    return 'Eliminazione avvenuta'


# ESEGUIRE UNA POST CON PARAMETRO id_personaggio ed id_Incantesimo
# RITORNA ROBA INUTILE
@app.route('/salva_incantesimo', methods=['POST', 'GET'])

def salva_incantesimo():
    
    if request.method == 'GET':
        return "Utilizzare una POST"
    #if not admin(): return FALSE 

    if not check(request.form['id_personaggio']) or not check(request.form['id_incantesimo']):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Lista_Incantesimi VALUES ('{}','{}')".format(request.form['id_personaggio'], request.form['id_incantesimo']))
    mydb.commit()
    return 'Incantesimo salvato'


# ESEGUIRE UNA POST CON PARAMETRO id_incantesimo ed id_personaggio
# RITORNA ROBA INUTILE
@app.route('/elimina_incantesimo', methods=['POST', 'GET'])

def elimina_incantesimo():

    if request.method == 'GET':
        return "Utilizzare una POST"

    if not check(request.form['id_personaggio']) or not check(request.form['id_incantesimo']):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute ("DELETE FROM Lista_Incantesimo WHERE id_personaggio = {} and id_Incantesimo = '{}'".format(request.form['id_personaggio'], request.form['id_incantesimo']))
    mydb.commit()
    return "Eliminazione effettuata"

    



# ESEGUIRE UNA RICHIESTA A /personaggio/input con input id dell'Utente
# RITORNA LA LISTA DEI PERSONAGGI DI UN UTENTE
@app.route('/personaggi/<id>')

def get_personaggi(id):

    if not check(id):
        return "Niente Sql Injection qui"
    

    mydb = connect_db()
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM Personaggio WHERE id_Utente = '{}'".format(id))
    myresult = mycursor.fetchall()
    
    return str(myresult)


# ESEGUIRE UNA RICHIESTA A lista_incantesimo/id_personaggio
# RITORNA UNA LISTA DI TUPLE di id_incantesimo
@app.route('/lista_incantesimi/<id>')

def get_lista_incantesimi(id):
    if not check(id):
        return "Niente Sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id_Incantesimo FROM Lista_Incantesimi WHERE id_personaggio = '{}'".format(id))
    myresult = mycursor.fetchall()
    return str(myresult)



# ESEGUIRE UNA RICHIESTA CON /ricerca/parametro
# FUNZIONA SIA CON LA CLASSE, CHE CON l'ID CHE CON Il Nome
# RITORNA TUPLE di Incantesimi
@app.route('/ricerca/<nome>')

def ricerca(nome):
    if not check(nome):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("Select * FROM Incantesimo WHERE Nome = '{}' or Classe = {} or id = '{}'".format(nome, nome, nome))
    myresult = mycursor.fetchall()

    return str(myresult)
