import sqlite3 as sql
import pandas as pd

def createUserDataIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS userdata (
                            id integer primary key autoincrement,
                            name text not null,
                            username text not null,
                            contact text not null,
                            address text not null,
                            gender text not null,
                            age text not null,
                            dob text not null,
                            email text not null,
                            profession text not null,
                            hobbies text not null,
                            family text not null,
                            familyMembers text not null,
                            medicalCondition text not null,
                            pets text not null
                        );
                    """)


def insertUserData(name, username, contact, address, gender, age, dob, email, profession, hobbies, family, familyMembers, medicalCondition, pets):
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO userdata (name, username, contact, address, gender, age, dob, email, profession, hobbies, family, familyMembers,  medicalCondition, pets) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (name, username, contact, address, gender, age,  dob, email, profession, hobbies, family, familyMembers,  medicalCondition, pets))
    con.commit()
    con.close()


def retrieveUserData():
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM userdata")
    loc = cur.fetchall()
    con.close()
    return loc


def createMoodTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS mood (
                            id integer primary key autoincrement,
                            moodCategory text not null,
                            timeCategory text not null,
                            default text not null,
                            
                        );
                    """)
def insertMoodData(id, moodCategory, timeCategory, default):
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO mood (id, moodCategory, timeCategory, default) VALUES (?,?,?,?)",
        (id, moodCategory, timeCategory, default))
    con.commit()
    con.close()

def retrieveMoodData():
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM mood")
    loc = cur.fetchall()
    con.close()
    return loc


def createMusicTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Musicdata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS music (
                            id integer primary key autoincrement,
                            language text not null,
                            musicCategory text not null,
                            source text not null
                        );
                    """)

def insertMusicData( language, musicCategory , source):
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO music (language, musicCategory, source ) VALUES (?,?,?)",
        (language, musicCategory, source))
    con.commit()
    con.close()


def retrieveMusicData():
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM music")
    loc = cur.fetchall()
    con.close()
    return loc

def createMovieTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Moviedata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS movie (
                            id integer primary key autoincrement,
                            name text not null,
                            movieCategory text not null,
                            source text not null
                        );
                    """)

def insertMovieData(name, movieCategory, source):
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Moviedata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO movie (name, movieCategory,source) VALUES (?,?,?)",
        (name, movieCategory, source))
    con.commit()
    con.close()


def retrieveMovieData():
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Moviedata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM movie")
    loc = cur.fetchall()
    con.close()
    return loc

def createGameTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Gamedata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS game (
                            id integer primary key autoincrement,
                            gameCategory text not null,
                            gameTitle text not null,
                            source text not null
                        );
                    """)

def insertGameData(gameCategory, gameTitle, source):
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Gamedata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO game (gameCategory, gameTitle, source) VALUES (?,?,?)",
        (gameCategory, gameTitle, source))
    con.commit()
    con.close()


def retrieveGameData():
    con = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Gamedata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM game")
    loc = cur.fetchall()
    con.close()
    return loc

def loadCsvFileToUserData():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\ASUS\PycharmProjects\Chat_bot\utils\csv\userdata.csv')

    # Write the data to a sqlite db table
    location.to_sql('userdata', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from userdata')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()

def loadCsvFileToMusicTable():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Musicdata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\ASUS\PycharmProjects\Chat_bot\utils\csv\music.csv')

    # Write the data to a sqlite db table
    location.to_sql('music', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from music')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()

def loadCsvFileToMovieTable():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Moviedata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\ASUS\PycharmProjects\Chat_bot\utils\csv\movie.csv')

    # Write the data to a sqlite db table
    location.to_sql('movie', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from movie')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()

def loadCsvFileToGameTable():
    sqlConnection = sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Gamedata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\ASUS\PycharmProjects\Chat_bot\utils\csv\game.csv')

    # Write the data to a sqlite db table
    location.to_sql('game', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from game')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()
#createUserDataIfNotExist()
#loadCsvFileToUserData()
#print(retrieveUserData())
#loadCsvFileToMovieTable()
#print(retrieveMovieData())
#loadCsvFileToMusicTable()
#print(retrieveMusicData())
#print(retrieveGameData())
#loadCsvFileToGameTable()
def getUserDataStructure():
    conn= sql.connect(r"C:\Users\ASUS\PycharmProjects\Chat_bot\utils\Dbs\Userdata.db")
    a= conn.execute("PRAGMA table_info('userdata')")
    for i in a:
        print(i)

getUserDataStructure()
insertUserData("name", "username", "67", "address", "gender", 66, "dob", "email", "profession", "hobbies", "family", 34, "medicalCondition", "pets")
print(retrieveUserData())