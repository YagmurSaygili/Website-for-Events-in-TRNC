import sqlite3

# Creating Database and tables; user, event, city
def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE user("
              "username TEXT PRIMARY KEY,"
              "password TEXT,"
              "firstname TEXT,"
              "lastname TEXT,"
              "email)")

    c.execute("CREATE TABLE city("
              "cityid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "cityname TEXT)")

    c.execute("CREATE TABLE event("
              "eventid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "name TEXT,"
              "description TEXT,"
              "price INTEGER,"
              "date DATE,"
              "time TEXT,"  # Can Be Changed
              "isActive INTEGER,"
              "location TEXT,"
              "username TEXT,"
              "cityid INTEGER,"
              "FOREIGN KEY (cityid) REFERENCES city(cityid)"
              "FOREIGN KEY (username) REFERENCES user(username))")

def insertRecord(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (1, "event1",
               "This is event1",
               100,
               '2022-11-10',
               '11.40',
               1,
               "Girne", "test1", 1))
    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (2, "event2",
               "This is event2", 200, '2022-11-10', '11.40', 1, "Girne", "test1", 2))
    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (3, "event3",
               "This is event3", 300, '2022-11-10', '11.40', 1, "Girne", "test1", 1))
    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (4, "event4",
               "This is event4", 400, '2022-11-10', '11.40', 1, "Girne", "test1", 1))
    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (99, "event4",
               "This is event4", 400, '2022-11-10', '11.40', 1, "Girne", "test1", 1))
    c.execute("Insert INTO event(eventid,name,description,price,date,time,isactive,location,username,cityid)Values(?,?,?,?,?,?,?,?,?,?)",
              (5, "event5",
               "This is event5", 500, '2022-11-10', '11.40', 1, "Girne", "test1", 1))

    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(1,"Lefkosa"))
    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(2,"Girne"))
    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(3,"Guzelyurt"))
    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(4,"Gazi Magusa"))
    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(5,"Lefke"))
    c.execute("INSERT INTO city(cityid,cityname)Values(?,?)",(6,"Iskele"))


    conn.commit()

if __name__ == "__main__":
    createDatabase("postdb.db")
    insertRecord("postdb.db")
    conn = sqlite3.connect("postdb.db")
    c = conn.cursor()

    c.execute("Select * from event")
    rows = c.fetchall()

    for row in rows:
        print(row)
    c.close()
    conn.close()