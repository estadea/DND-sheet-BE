#----------------------# SICUREZZA E CONNESSIONE DB #----------------------#

#----------------------# PARTE RELATIVA SOLAMENTE AL BACKEND #----------------------#

def connect_db():
        mydb = mysql.connector.connect(
                host="localhost",
                user="dandb",
                password="*****",
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
    password = hashlib.sha256(password.encode()).hexdigest()
    if check(id):
        mycursor.execute("SELECT ruolo FROM Utenti WHERE id = '{}'".format(id))
        myresult = mycursor.fetchone()
        if myresult[0] == 1:
            return True
        else:
            return False

    else:
        return 'False'