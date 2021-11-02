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
@app.route('/controllaDati', methods=['POST', 'GET'])
def controllaDati():
    
    if request.method == 'GET':
        return "Utilizzare una POST"

    username = request.form['username']
    email = request.form['email']

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Utenti WHERE username = '{}'or email = '{}'".format(username, email))
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return 'True'
    else:
        return 'False'

@app.route('/controllaIncantesimo/<incantesimo>')
def controllaIncantesimo(incantesimo):
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Incantesimo WHERE Nome  = '{}'".format(incantesimo))
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return 'True'