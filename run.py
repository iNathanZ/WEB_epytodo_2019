from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import pymysql as sql
from app import app
from app import views

app.secret_key = '\xc8`\xa6\xa3\xf5\xc2\x81\xe2\x83\xfb2\x14\xa18\xf8\x19\x80j\xb8\xa0\x17\x9e\x08#'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'axf64b'
app.config['MYSQL_DB'] = 'epytodo'

app.run(debug=True)