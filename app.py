from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/name', methods=['POST', 'GET'])
def name():
    error = None
    if request.method == 'POST':
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('input.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('input.html', error=error)


def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(Pid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT);')
    connection.commit()
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()


@app.route('/deletename', methods=['POST', 'GET'])
def delete_name():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM users;')
    result = cursor.fetchall()
    connection.commit()

    error = None
    if request.method == 'POST':
        connection = sql.connect('database.db')
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        connection.execute('DELETE from users WHERE firstname=? and lastname=?',(first_name, last_name))
        connection.commit()
        cursor = connection.execute('SELECT * FROM users;')
        result = cursor.fetchall()
        print(result)
        if result:
            return render_template('deletename.html', error=error, result=result)
        else:
            error = 'invalid input name'

    return render_template('deletename.html', error=error, result=result)


if __name__ == "__main__":
    app.run()


