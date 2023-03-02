from flask import *
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "it should be secret"


# Index for home page
@app.route("/")
@app.route("/index")
def index():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    else:
        return render_template("index.html")


# Route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST":
        username = escape(request.form["username"])
        password = escape(request.form["password"])
        conn = sqlite3.connect("postdb.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        row = c.fetchone()

        if row:
            session["username"] = username
            return redirect('/index')
        else:
            msg = "Invalid Credentials!"

        return render_template('index.html', msg=msg)

        conn.close()
    elif request.method == "GET":
        pass


# Route for register get inputs and save to database
@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = escape(request.form["username"])
        password = escape(request.form["password"])
        firstname = escape(request.form["firstname"])
        lastname = escape(request.form["lastname"])
        email = escape(request.form["email"])

        conn = sqlite3.connect("postdb.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username=? ", (username,))
        account = c.fetchone()

        if account:
            msg = 'Account already exists !'
        elif len(password) < 8:
            msg = 'Password length must be at least 8 !'
        elif not any(char.isupper() for char in password):
            msg = 'Password should include at least one upper case!'
        elif not any(char.islower() for char in password):
            msg = 'Password should include at least one lower case!'
        elif not any(char.isdigit() for char in password):
            msg = 'Password should include at least one digit!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            c.execute('INSERT INTO user VALUES (?,?,?,?,?)', (username, password, firstname, lastname, email,))
            c.connection.commit()
            msg = 'You have successfully registered !'
            conn.close()

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("register.html", msg=msg)


# Route for logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


# Route for adding new event to database
@app.route("/AddEvent")
def AddEvent():
    if "username" in session:
        conn = sqlite3.connect("postdb.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username=?", (session["username"],))
        records = c.fetchall()
        conn.close()
        return render_template("AddEvent.html", records=records)
    return redirect(url_for("index"))


# Route for displaying my events from database
@app.route("/myEvents")
def myEvents():
    if "username" in session:
        # retrieve the events from the database
        conn = sqlite3.connect("postdb.db")
        c = conn.cursor()
        c.execute(
            "SELECT event.name, event.description, event.location, city.cityname, event.price, event.date, event.time,event.eventid  "
            "FROM event,city,user "
            "WHERE city.cityid = event.cityid AND "
            "user.username = event.username AND event.isActive = 1")
        dataStorage = []
        events = c.fetchall()
        conn.close()
        return render_template("home.html", events=events)


# Route for deactivating events from database
@app.route('/deactivate-event', methods=['POST'])
def deactivate_event():
    # Get the event ID from the form
    event_id = request.form['eventId']
    print(event_id)
    conn = sqlite3.connect("postdb.db")
    cursor = conn.cursor()
    # Deactivate the event with the specified ID
    cursor.execute("UPDATE event SET isActive = 0 WHERE eventid = ?", (event_id,))
    # Commit the change
    conn.commit()
    # Close the connection
    conn.close()
    return redirect('/myEvents')


# Route for seeing more details about the event
@app.route('/seeMore', methods=['POST'])
def seeMore():
    # Get the event ID from the form
    event_name = request.form['eventName']
    conn = sqlite3.connect("postdb.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT event.name, event.description, event.location, city.cityname, event.price, event.date, event.time  "
        "FROM event,city "
        "WHERE event.name =? ", (event_name,))

    # Commit the change
    conn.commit()
    seeMoreDetails = cursor.fetchall()
    conn.close()
    return render_template("index.html", seeMoreDetails=seeMoreDetails)


# Route for creating a new event and adding to the add event page
@app.route('/create-event', methods=['POST'])
def create_event():
    msg = ''
    # get the form data from the request
    event_name = request.form['eventName']
    event_description = request.form['eventDescription']
    event_location = request.form['eventLocation']
    event_city = request.form['eventCity']
    event_price = request.form['eventPrice']
    event_date = request.form['eventDate']

    conn = sqlite3.connect("postdb.db")
    cursor = conn.cursor()

    cursor.execute("SELECT cityid FROM city WHERE cityname = ?", (event_city,))
    tmpresult = cursor.fetchone()
    cityID = tmpresult[0]

    username = session['username']

    print("Adsfasdhfasdfds")
    cursor.execute(
        "Insert INTO event (name, description, price, date, time, isActive, location, username, cityid) Values(?,?,?,?,?,?,?,?,?)",
        (event_name, event_description, event_price, '2022-11-10', '11.40', 1, event_location, username, cityID,))
    conn.commit()
    print("123213214213fds")
    # Close the connection
    conn.close()

    msg = 'You have successfully registered !'
    return render_template("AddEvent.html", msg=msg)


# Route for displaying top 5 events for each city
@app.route("/topEvents", methods=['POST'])
def topEvents():
    if "username" in session:
        # retrieve the events from the database
        conn = sqlite3.connect("postdb.db")
        c = conn.cursor()

        c.execute(
            "SELECT event.name, city.cityname, event.price, event.date, event.time  "
            "FROM event "
            "LEFT JOIN city ON event.cityid = city.cityid "
            "WHERE event.isActive = 1"
            "GROUP BY city.cityname ORDER BY event.date DESC, event.time DESC LIMIT 5;")
        events = c.fetchall()
        conn.close()
        return render_template("index.html", events=events)


# Route for searching for an event
@app.route('/search', methods=['POST'])
def search():
    # Get the search keywords from the form
    searchField = request.form['searchField']

    # Connect to the database
    conn = sqlite3.connect("postdb.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM event "
        "WHERE (name LIKE '%' || ? || '%' OR description LIKE '%' || ? || '%' OR location LIKE '%' || ? || '%') "
        "AND isActive = 1", (searchField, searchField, searchField))

    result = cursor.fetchall()

    # Close the connection
    conn.close()

    return render_template('search_results.html', searchField=searchField)


if __name__ == "__main__":
    app.run()
