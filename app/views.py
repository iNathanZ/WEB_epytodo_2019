from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import pymysql as sql
from app import *

@app.route('/register/page')
def home_reg():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('log.html')

@app.route('/user/handler')
def handler_user():
    return render_template("handler.html")

@app.route('/task/handler')
def handler_task():
    return render_template("task_handler.html")

@app.route('/', methods=["GET"])
def index():
    session['loggedin'] = False
    return render_template('index.html')