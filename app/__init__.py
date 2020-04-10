from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import pymysql as sql

app = Flask(__name__)

@app.route('/register', methods=["POST"])
def create_user():
    if request.method == 'POST':
        if session['loggedin']:
            return render_template("register.html", error="You are already logged in if you want to register, please log out")
        try:
            connection = mysql.connector.connect(host='localhost',
                                        database='epytodo',
                                        user='root',
                                        password='axf64b')
            if connection.is_connected():
                req = request.form
                form = (req["username"], req["password"])
                cursor = connection.cursor()
                sql = "INSERT INTO user (username, password) VALUES (%s, %s);"
                cursor.execute(sql, form)
                connection.commit()

        except Error as e:
            print("error is :", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("connection closed")
    return render_template('index.html')

@app.route('/signin', methods=["POST"])
def signin():
    msg = ""
    if request.method == 'POST':
        if session['loggedin']:
            return render_template("register.html", error="You are already logged in if you want to register, please log out")
        req = request.form
        form = (req["username"], req["password"])

        try:
            connection = mysql.connector.connect(host='localhost',
                                        database='epytodo',
                                        user='root',
                                        password='axf64b')
            if connection.is_connected():
                cursor = connection.cursor()
                sql = "SELECT * FROM user WHERE username = %s AND password = %s;"
                cursor.execute(sql, form)
                account = cursor.fetchone()
                print(account)
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                value = "you are logged as " + account[1]
                return render_template("index.html", state=value)

        except Error as e:
            print("error is :", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("connection closed")
    return render_template('users.html')

@app.route('/logout')
def logout():
    if session['loggedin'] == False:
        return render_template("register.html", error="You are already logged out")
    session.pop('loggedin', False)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')

@app.route('/user')
def print_user():
    msg = ""
    if session['loggedin'] == False:
        return render_template("register.html", error="You have to log in before")
    form = (session['id'],)
    print(form)
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='epytodo',
                                    user='root',
                                    password='axf64b')
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "SELECT * FROM user WHERE user_id = %s;"
            cursor.execute(sql, form)
            account = cursor.fetchone()
            print(account)
        if account:
            password = account[2]
            username = account[1]
            return render_template("users.html", pswd=password, name=username)

    except Error as e:
        print("error is :", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")
    return render_template('index.html')

@app.route('/user/task/add', methods=['POST'])
def add_new_task():
    if session['loggedin'] == False:
        return render_template("register.html", error="You have to log in before")
    form = (request.form["task"],)
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='epytodo',
                                    user='root',
                                    password='axf64b')
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "INSERT INTO task (title) VALUES (%s);"
            cursor.execute(sql, form)
            connection.commit()
            task = cursor.lastrowid
            to_insert = (session['id'], task)
            sql = "INSERT INTO user_has_task VALUES (%s, %s);"
            cursor.execute(sql, to_insert)
            connection.commit()
            return render_template("tasks.html")

    except Error as e:
        print("error is :", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")
    return render_template('index.html')

@app.route('/user/task')
def print_user_tasks():
    number = 0
    msg = []
    if session['loggedin'] == False:
        return render_template("handler.html", error="You have to log in before")
    form = (session['id'],)
    print(form)
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='epytodo',
                                    user='root',
                                    password='axf64b')
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "SELECT * FROM user_has_task WHERE fk_user_id = %s;"
            cursor.execute(sql, form)
            account = cursor.fetchall()
            rows = cursor.rowcount
            print(rows)
            for row in account:
                sql = "SELECT * FROM task WHERE task_id = %s;"
                cursor.execute(sql, (row[1],))
                msg.append(cursor.fetchone())
            return render_template("tasks.html", message=msg)

    except Error as e:
        print("error is :", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")
    return render_template('index.html')

@app.route('/user/task/<int:task_id>', methods=["GET", "POST"])
def print_user_spectask(task_id):
    print("value = ", request.form['value'])
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='epytodo',
                                    user='root',
                                    password='axf64b')
        if connection.is_connected():
            print("connecté")
            cursor = connection.cursor()
            if request.method == 'GET':
                sql = "SELECT * FROM task WHERE task_id = %s;"
                cursor.execute(sql, (task_id,))
                account = cursor.fetchone()
            if request.method == 'POST':
                print("post")
                sql = "UPDATE task SET status = %s;"
                cursor.execute(sql, (request.form['value'],))
                return ("task updated")
            if account:
                return render_template("spec_task.html", msg=account)
            else:
                return render_template("index.html", error="task id does  not  exist")

    except Error as e:
        print("error is :", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")
    return render_template('index.html')

@app.route('/user/task/del/<int:task_id>', methods=['POST'])
def del_task(task_id):
    if session['loggedin'] == False:
        return render_template("register.html", error="You have to log in before")
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='epytodo',
                                    user='root',
                                    password='axf64b')
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "DELETE FROM task WHERE task_id = %s;"
            cursor.execute(sql, (task_id,))
            connection.commit()
            return ("task deleted")

    except Error as e:
        print("error is :", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")
    return render_template('index.html')