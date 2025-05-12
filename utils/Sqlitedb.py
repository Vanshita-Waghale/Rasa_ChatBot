import sqlite3 as sql
import pandas as pd


def createUserDataIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS userdata (
                            name text not null,
                            username text not null,
                            password text not null,
                            contact text not null,
                            address text not null,
                            gender text not null,
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


def insertUserData(name, username, password, contact, address, gender, dob, email, profession, hobbies, family,
                   familyMembers, medicalCondition, pets):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO userdata (name, username, password, contact, address, gender, dob, email, profession, hobbies, family, familyMembers,  medicalCondition, pets) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (name, username, password, contact, address, gender, dob, email, profession, hobbies, family, familyMembers,
         medicalCondition, pets))
    con.commit()
    con.close()


def retrieveUserData():
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM userdata")
    loc = cur.fetchall()
    con.close()
    return loc


def get_existing_usernames_from_database():
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute("SELECT username FROM userdata")
    existing_usernames = [username[1] for username in cur.fetchall()] if cur.fetchall() else []
    con.close()
    return existing_usernames


def createMoodTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
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
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO mood (id, moodCategory, timeCategory, default) VALUES (?,?,?,?)",
        (id, moodCategory, timeCategory, default))
    con.commit()
    con.close()


def retrieveMoodData():
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM mood")
    loc = cur.fetchall()
    con.close()
    return loc


def createMusicTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS musicData (
                            id integer primary key autoincrement,
                            language text not null,
                            musicCategory text not null,
                            source text not null,
                            cluster int,
                            mood text not null
                        );
                    """)


def insertMusicData(language, musicCategory, source, cluster, mood):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO musicData (language, musicCategory, source, cluster, mood ) VALUES (?,?,?,?,?)",
        (language, musicCategory, source, cluster, mood))
    con.commit()
    con.close()


def retrieveMusicData(MusicCategory):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM musicData WHERE MusicCategory='{MusicCategory}'")
    loc = cur.fetchall()
    musicData_accumulator = []
    # Display result
    for row in loc:
        language = row[0]
        MusicCategory = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        cur.execute(f"SELECT * FROM musicData WHERE cluster_predicted ='{cluster}'")
        locWithCluster = cur.fetchall()

        musicDataDict = {"MusicCategory": MusicCategory, "Source": Source}
        musicData_accumulator.append(musicDataDict)
        # for item in locWithCluster:
        #     language = item[0]
        #     MusicCategory = item[1]
        #     Source = item[2]
        #     clustered = item[3]
        #     mood = row[4]
        #
        #     musicDataDict = {"MusicCategory": MusicCategory, "Source": Source}
        #     musicData_accumulator.append(musicDataDict)
    con.close()
    return musicData_accumulator


def retrieveMusicData(language, music_category):
    # Convert music category to match the format in the database
    print("Music data for language {} and category {}".format(language, music_category))
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM musicData WHERE Language='{language}' AND MusicCategory='{music_category}'")
    loc = cur.fetchall()
    musicData_accumulator = []

    # Display result
    for row in loc:
        language = row[0]
        music_category = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        cur.execute(f"SELECT * FROM musicData WHERE cluster_predicted ='{cluster}'")
        locWithCluster = cur.fetchall()

        musicDataDict = {"MusicCategory": music_category, "Source": Source}
        musicData_accumulator.append(musicDataDict)

        # for item in locWithCluster:
        #     language = item[0]
        #     music_category = item[1]
        #     Source = item[2]
        #     clustered = item[3]
        #     mood = row[4]
        #
        #     musicDataDict = {"MusicCategory": music_category, "Source": Source}
        #     musicData_accumulator.append(musicDataDict)
    con.close()
    return musicData_accumulator


def retrieveMusicData(mood, language, music_category):
    # Convert music category to match the format in the database
    #print("Music data for language {} and category {}".format(language, music_category))
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM musicData WHERE mood='{mood}' AND Language='{language}' AND MusicCategory='{music_category}'")
    loc = cur.fetchall()
    musicData_accumulator = []

    # Display result
    for row in loc:
        language = row[0]
        music_category = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        cur.execute(f"SELECT * FROM musicData WHERE cluster_predicted ='{cluster}'")
        locWithCluster = cur.fetchall()

        musicDataDict = {"MusicCategory": music_category, "Source": Source, "mood" : mood}
        musicData_accumulator.append(musicDataDict)

        # for item in locWithCluster:
        #     language = item[0]
        #     music_category = item[1]
        #     Source = item[2]
        #     clustered = item[3]
        #     mood = row[4]
        #
        #     musicDataDict = {"MusicCategory": music_category, "Source": Source}
        #     musicData_accumulator.append(musicDataDict)
    con.close()
    return musicData_accumulator


def createMovieTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Moviedata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS moviesData (
                            id integer primary key autoincrement,
                            name text not null,
                            movieCategory text not null,
                            source text not null,
                            cluster int,
                            mood text not null
                        );
                    """)


def insertMovieData(name, movieCategory, source, cluster, mood):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Moviedata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO moviesData (name, movieCategory,source, cluster, mood) VALUES (?,?,?,?,?)",
        (name, movieCategory, source, cluster, mood))
    con.commit()
    con.close()


def retrieveMovieData(MovieCategory):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Moviedata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM moviesData WHERE MovieCategory='{MovieCategory}'")
    loc = cur.fetchall()
    movieData_accumulator = []
    # Display result
    for row in loc:
        Name = row[0]
        MovieCategory = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        cur.execute(f"SELECT * FROM moviesData WHERE cluster_predicted ='{cluster}'")
        movieDataDict = {"MovieCategory": MovieCategory, "Source": Source}
        movieData_accumulator.append(movieDataDict)
        locWithCluster = cur.fetchall()
        # for item in locWithCluster:
        #     Name = item[0]
        #     MovieCategory = item[1]
        #     Source = item[2]
        #     cluster = item[3]
        #     mood = item[4]
        #
        #     movieDataDict = {"MovieCategory": MovieCategory, "Source": Source}
        #     movieData_accumulator.append(movieDataDict)
    con.close()
    return movieData_accumulator

def retrieveMovieData(mood, MovieCategory):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Moviedata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM moviesData WHERE mood='{mood}' AND MovieCategory='{MovieCategory}'")
    loc = cur.fetchall()
    moviesData_accumulator = []
    for row in loc:
        MovieTitle = row[0]
        MovieCategory = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        moviesDataDict = {"MovieCategory": MovieCategory, "Source": Source, "mood": mood}
        moviesData_accumulator.append(moviesDataDict)
    con.close()
    return moviesData_accumulator

def createGameTableIfNotExist():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Gamedata.db")
    # print(sqlConnection)

    sqlConnection.execute("""
                        CREATE TABLE IF NOT EXISTS gamesData (
                            id integer primary key autoincrement,
                            gameCategory text not null,
                            gameTitle text not null,
                            source text not null,
                            cluster int,
                            mood text not null
                        );
                    """)


def insertGameData(gameCategory, gameTitle, source, cluster, mood):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Gamedata.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO gamesData (gameCategory, gameTitle, source,cluster,mood) VALUES (?,?,?,?,?)",
        (gameCategory, gameTitle, source, cluster, mood))
    con.commit()
    con.close()

def retrieveGameData(GameCategory):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Gamedata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM gamesData WHERE GameCategory='{GameCategory}'")
    loc = cur.fetchall()
    gamesData_accumulator = []
    for row in loc:
        GameTitle = row[0]
        GameCategory = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        gamesDataDict = {"GameTitle": GameTitle, "GameCategory": GameCategory, "Source": Source, "mood": mood}
        gamesData_accumulator.append(gamesDataDict)
    con.close()
    return gamesData_accumulator

def retrieveGameData(mood, GameCategory):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Gamedata.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM gamesData WHERE mood='{mood}' AND GameCategory='{GameCategory}'")
    loc = cur.fetchall()
    gamesData_accumulator = []
    for row in loc:
        GameTitle = row[0]
        GameCategory = row[1]
        Source = row[2]
        cluster = row[3]
        mood = row[4]
        gamesDataDict = {"GameCategory": GameCategory, "Source": Source, "mood": mood}
        gamesData_accumulator.append(gamesDataDict)
    con.close()
    return gamesData_accumulator


def loadCsvFileToUserData():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\current_userdata.csv')

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
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Musicdata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\csv\musicData.csv')

    # Write the data to a sqlite db table
    location.to_sql('musicData', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from musicData')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()


def loadCsvFileToMovieTable():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Moviedata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\csv\moviesData.csv')

    # Write the data to a sqlite db table
    location.to_sql('moviesData', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from moviesData')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()


def loadCsvFileToGameTable():
    sqlConnection = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Gamedata.db")
    # Create a cursor object
    curs = sqlConnection.cursor()
    # # Run create table sql query
    # curs.execute("create table if not exists studentInfo" +
    #              " (name text, gender text, age integer,course text, branch text)")
    # Load CSV data into Pandas DataFrame
    location = pd.read_csv(r'C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\csv\gamesData.csv')

    # Write the data to a sqlite db table
    location.to_sql('gamesData', sqlConnection, if_exists='replace', index=False)

    # Run select sql query
    curs.execute('select * from gamesData')

    # Fetch all records
    # as list of tuples
    records = curs.fetchall()
    # Close connection to SQLite database
    sqlConnection.close()


def getUserDataStructure():
    conn = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    a = conn.execute("PRAGMA table_info('userdata')")
    for i in a:
        print(i)


def retrieveClusterUserData(username, password):
    con = sql.connect(r"C:\Users\wagha\PycharmProjects\Chat_bot_4 (1)\Chat_bot_4\utils\Dbs\Userdata.db")
    cur = con.cursor()
    cur.execute(
        f"SELECT username, password, family, medicalCondition, pets FROM userdata WHERE username='{username}' AND password='{password}'")
    data = cur.fetchall()
    con.close()
    return data


response = retrieveClusterUserData("123Dhawal", "@123Dhawal")
#print(response)
len(response) > 0
# createUserDataIfNotExist()
# loadCsvFileToUserData()
# insertUserData("name", "username","demo", 8177864759, "address", "gender", "dob", "email", "profession", "hobbies", "family", 5, "medicalCondition", "pets")
# print(retrieveUserData())
# createMovieTableIfNotExist()
# loadCsvFileToMovieTable()
# print(retrieveMovieData('Drama'))
# createMusicTableIfNotExist()
# loadCsvFileToMusicTable()
#print(retrieveMusicData('Hindi', 'Classical Music Old'))
#createGameTableIfNotExist()
#loadCsvFileToGameTable()
#print(retrieveGameData('happy', 'Adventure'))
#print(retrieveGameData('sad', 'Adventure'))
#print(retrieveGameData('bored', 'Adventure'))
#print(retrieveMovieData('happy', 'Drama'))
print(retrieveMusicData('sad','Hindi', 'Classical Music Old'))
# getUserDataStructure()
# insertUserData("name", "username","demo", 8177864759, "address", "gender", "dob", "email", "profession", "hobbies", "family", 5, "medicalCondition", "pets")
# print(retrieveUserData())
