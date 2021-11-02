from flask import Flask
from flask import request
from flask import jsonify
import mysql.connector
import hashlib
import string
import json
import urllib.parse

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

#----------------------# README #----------------------#


# I controlli per la registrazione, aggiunta e modifica di utenti non vengono effettuati lato backend

# SOno perà disponibili delle funzioni in Controller per eseguire i controlli necessari

# Per il login da web è stata implementata una funzione differente presente nella parte relativa all'admin



#----------------------# REQUISITI E FUNZIONI #----------------------#

# LOGIN è implementato da login()

# REGISTRAZIONE è implementata da registrazione()

#----------------------# VISITATORE #----------------------#

# ESEGUIRE UNA POST CON PARAMETRI username, email, password
@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    username = request.form['username']

    if not check(email) or not check(username) or not check(password):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()

    mycursor.execute("INSERT into Utenti (username, email, password, ruolo) VALUES ('{}','{}', '{}', '0')".format(username, email, password))
    mydb.commit()
    
    return "Registrazione completata"

# ESEGUIRE UNA POST CON PARAMETRI username, password
@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()

    mydb = connect_db()
    mycursor = mydb.cursor()

    if check(username):
        mycursor.execute("SELECT * FROM Utenti WHERE username = '{}' and password = '{}'".format(username, password))
        r = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
        return jsonify(r)

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

@app.route('/crea_personaggio', methods=["POST"])
def crea_personaggio():
    if not check(request.form['Nome']) or not check(request.form['id_utente']) or not check(request.form['Classe']):
            return "Niente sql injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Personaggio (Nome, Classe, id_Utente) VALUES ('{}','{}','{}')".format(request.form['Nome'], request.form['Classe'], request.form['id_utente']))
    mydb.commit()
    
    return 'Personaggio aggiunto'


# ESEGUIRE UNA POST Con parametro id_personaggio e id_utente
@app.route('/elimina_personaggio', methods=["POST"])
def elimina_personaggio():
    if not check(request.form['id_personaggio']):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Personaggio WHERE id = '{}'".format(request.form['id_personaggio']))
    mycursor.execute ("DELETE FROM Lista_Incantesimi WHERE id_personaggio = {}".format(request.form['id_personaggio']))
    mydb.commit()
    return 'Eliminazione avvenuta'


# ESEGUIRE UNA POST CON PARAMETRO id_personaggio ed id_Incantesimo
# RITORNA ROBA INUTILE
@app.route('/salva_incantesimo', methods=["POST"])
def salva_incantesimo(): 
    id_personaggio = request.form['id_personaggio']
    id_incantesimo = request.form['id_incantesimo']

    if not check(id_personaggio) or not check(id_incantesimo):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT into Lista_Incantesimi VALUES ('{}','{}')".format(id_incantesimo, id_personaggio))
    mydb.commit()

    return 'Incantesimo salvato'


# ESEGUIRE UNA POST CON PARAMETRO id_incantesimo ed id_personaggio
# RITORNA ROBA INUTILE
@app.route('/elimina_incantesimo', methods=["POST"])
def elimina_incantesimo():
    id_personaggio = request.form['id_personaggio']
    id_incantesimo = request.form['id_incantesimo']

    if not check(id_personaggio) or not check(id_incantesimo):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute ("DELETE FROM Lista_Incantesimi WHERE id_personaggio = {} and id_Incantesimo = '{}'".format(id_personaggio, id_incantesimo))
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
    r = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
    return jsonify(r)

# ESEGUIRE UNA RICHIESTA A lista_incantesimo/id_personaggio
# RITORNA UNA LISTA DI TUPLE di id_incantesimo
@app.route('/lista_incantesimi/<id>')

def get_lista_incantesimi(id):
    if not check(id):
        return "Niente Sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id_Incantesimo FROM Lista_Incantesimi WHERE id_personaggio = '{}'".format(id))
    
    r = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]

    return jsonify(r)

# ESEGUIRE UNA RICHIESTA CON /ricerca/parametro
# FUNZIONA SIA CON LA CLASSE, CHE CON l'ID CHE CON Il Nome
# RITORNA TUPLE di Incantesimi
@app.route('/ricerca/<nome>')
def ricerca(nome):
    spell_name = urllib.parse.unquote(nome)

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Incantesimo WHERE Nome LIKE '{}%' or Classe LIKE '{}%' or id = '{}'".format(spell_name, spell_name, spell_name))
    
    r = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
    return jsonify(r)


#----------------------# REQUISITI E FUNZIONI #----------------------#

# AGGIUNGI UTENTE è implementato da aggiungiUtente()

# RIMUOVI UTENTE è implementato da rimuoviUtente()

# AGGIORNA DATABASE è implementato da aggiornaDatabase()

# MODIFICA UTENTE è implementato da modificaUtente()


#----------------------# IMPLEMENTAZIONE ADMIN (WEB) #----------------------#

# ESEGUIRE UNA POST CON username e password
@app.route('/admin', methods=['POST', 'GET'])

def admin_login():

    if request.method == 'GET':
        return 'False'

        
    if not admin(str(id)):
        return 'False'

    username = request.form["username"]
    password = hashlib.sha256(request.form["password"].encode()).hexdigest()

    mydb = connect_db()
    mycursor = mydb.cursor()

    if check(str(username)):
        mycursor.execute("SELECT * FROM Utenti WHERE username = '{}' and password = '{}'".format(username, password))
        r = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
        return jsonify(r)



# ESEGUIRE UNA POST CON PARAMETRI ID = 1, username, email, password, ruolo
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

# ESEGUIRE UNA POST CON PARAMETRI username e ID = 1
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


# ESEGUIRE UNA POST CON PARAMETRI ID dell'admin, old_username (utente da modificare),  username, email, password e ruolo nuovi valori per le colonne.
# Se password = NULL allora non cambia la password
@app.route('/modificaUtente', methods=['POST', 'GET'])

def modificaUtente():
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    ruolo = request.form['ruolo']
    old_username = request.form['old_username']
    if request.method == 'GET':
        return "Utilizzare una POST"
    

    if not admin(request.form['ID']):
        return 'Non autorizzato'

    if not check(old_username) or not check(email) or not check(username) or not check(ruolo):
        return "Niente sql Injection qui"

    mydb = connect_db()
    mycursor = mydb.cursor()

    if password == "NULL":
        mycursor.execute("UPDATE Utenti SET username  = '{}', email ='{}',  ruolo='{}'  WHERE username = '{}'".format(request.form['username'], request.form['email'], request.form['ruolo'], request.form['old_username']))

    else:
        password = hashlib.sha256(password.encode()).hexdigest()
        mycursor.execute("UPDATE Utenti SET username  = '{}', email ='{}', password='{}', ruolo='{}'  WHERE username = '{}'".format(request.form['username'], request.form['email'], request.form['password'], request.form['ruolo'], request.form['old_username']))
    
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
    mycursor.execute("INSERT into Incantesimo (Nome, Descrizione, CD, Livello, TS, Classe) VALUES ('{}','{}','{}','{}','{}','{}')".format(request.form['Nome'], request.form['Descrizione'], request.form['CD'], request.form['Livello'],request.form['TS'], request.form['Classe']))
    mydb.commit()
    return 'Incantesimo aggiunto'

# id è l'id dell'admin
@app.route('/all_user/<id>')
def all_user(id):
    if not admin(id):
        return 'False'
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Utenti")
    result = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
    return jsonify(result)


@app.route('/all_incantesimi/<id>')
def all_incantesimi(id):
    if not admin(id):
        return 'False'
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Incantesimo")
    result = [dict((mycursor.description[i][0], value) for i, value in enumerate(row)) for row in mycursor.fetchall()]
    return jsonify(result)
#----------------------# SICUREZZA E CONNESSIONE DB #----------------------#

#----------------------# PARTE RELATIVA SOLAMENTE AL BACKEND #----------------------#

def connect_db():
        mydb = mysql.connector.connect(
                host="localhost",
                user="dandb",
                password="Salsa.Doom21.21",
                database="dndproject"
        )

        return mydb


def check(parameter):
    whitelist = string.ascii_letters + string.digits + "!$£/()=?^*+><.,:_+@"

    for char in parameter:
        if char not in whitelist:
            return False

    return True


def valid_login(username, password):
        mydb = connect_db()
        mycursor = mydb.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()
        if check(username):
            mycursor.execute("SELECT id FROM Utenti WHERE password = '{}' and username = '{}'".format(password, username))
            myresult = mycursor.fetchone()
            
            return myresult

def admin(id):
    mydb = connect_db()
    mycursor = mydb.cursor()
    if check(id):
        mycursor.execute("SELECT ruolo FROM Utenti WHERE id = '{}'".format(id))
        myresult = mycursor.fetchone()
        if str(myresult[0]) == "1":
            return True
        else:
            return False

    else:
        return 'False'

#----------------------# CONTROLLER PER VERIFICARE GLI INPUT #----------------------#

@app.route('/controlloSicurezzaPassword/<password>')
def controlloSicurezzaPassword(password):
    whitelist = "!$£/()=?^*+><.,:_+@&|;]["
    
    if len(password) > 7:
        for char in password:
            if char in whitelist:
                return 'True'
    return 'False'

# ESEGUIRE UNA POST CON PARAMETRI username ed email
@app.route('/controllaDati', methods=["POST"])
def controllaDati():
    username = request.form['username']
    email = request.form['email']

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Utenti WHERE username = '{}' OR email = '{}'".format(username, email))
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        return 'True'
    return 'False'

@app.route('/controllaIncantesimo/<incantesimo>')
def controllaIncantesimo(incantesimo):
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Incantesimo WHERE Nome  = '{}'".format(incantesimo))
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return 'True'
    else:
        return 'False'

#----------------------# MAIN #----------------------#

if __name__ == '__main__': app.run(host = '0.0.0.0', port = 10081)