**Il codice è diviso in:**

1. Parte Android su android.py 
2. Parte Web su web.py
3. Parte backend su backend.py
4. Parte del controller su controller.py


Il codice completo è disponibile su server.py.

**Per provare in locale:**

1. Creare un database così strutturato:

```
mysql> show tables

+----------------------+
| Tables_in_dndproject |
+----------------------+
| Incantesimo          |
| Lista_Incantesimi    |
| Personaggio          |
| Utenti               |
+----------------------+
4 rows in set (0.00 sec)

mysql> show columns FROM Utenti;
+----------+------+------+-----+---------+----------------+
| Field    | Type | Null | Key | Default | Extra          |
+----------+------+------+-----+---------+----------------+
| id       | int  | NO   | PRI | NULL    | auto_increment |
| username | text | YES  |     | NULL    |                |
| email    | text | YES  |     | NULL    |                |
| password | text | YES  |     | NULL    |                |
| ruolo    | int  | YES  |     | NULL    |                |
+----------+------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

mysql> show columns FROM Personaggio;
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| ID        | bigint       | NO   | PRI | NULL    | auto_increment |
| Nome      | varchar(255) | YES  |     | NULL    |                |
| Classe    | varchar(255) | YES  |     | NULL    |                |
| id_utente | int          | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)

mysql> show columns FROM Incantesimo;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| ID          | bigint       | NO   | PRI | NULL    | auto_increment |
| Nome        | varchar(255) | YES  |     | NULL    |                |
| Descrizione | varchar(255) | YES  |     | NULL    |                |
| CD          | varchar(255) | YES  |     | NULL    |                |
| Livello     | varchar(255) | YES  |     | NULL    |                |
| TS          | varchar(255) | YES  |     | NULL    |                |
| Classe      | varchar(255) | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)

mysql> show columns FROM Lista_Incantesimi;
+----------------+------+------+-----+---------+-------+
| Field          | Type | Null | Key | Default | Extra |
+----------------+------+------+-----+---------+-------+
| id_Incantesimo | int  | YES  |     | NULL    |       |
| Id_personaggio | int  | YES  |     | NULL    |       |
+----------------+------+------+-----+---------+-------+
2 rows in set (0.01 sec)
```



2. Usare il comando: `python3 server.py` per lanciare il programma


3. Eseguire richieste ad http://localhost:10081/nomeFunzione per utilizzare le varie funzioni.

