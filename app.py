# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS as cors
import smtplib


app = Flask(__name__)
cors(app)

countries = [   # list
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120}, # map
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]
# this defines a path on the server (localhost:5000) to access the data
@app.get("/countries")
def get_countries():
    return jsonify(countries)

@app.post("/sendmail")
def send_mail():
    
    sender = "soft-dev-2022@hotmail.com"
    password = "LetMeIn@2022"

    receivers = ["eamole@gmail.com"]
    message = 'Hello world'
    subject = 'Test Email from Python'
    body = 'Subject: {}\n\n{}'.format(subject, message)
    # smtp.gmail.com
    conn = smtplib.SMTP('smtp.office365.com',587)
    # type(conn)
    # conn.ehlo()
    conn.starttls()
    conn.login(sender,password)
    conn.sendmail(sender, receivers, body)
    conn.quit()  

    return "ok"

@app.get("/get-pub-data")
def get_pub_data():
    import sqlite3 as sql

    conn = sql.connect("./cork-tourism.sqlite")
    
    conn.row_factory = sql.Row

    cur = conn.cursor() # this is like a file handle

    sql = "SELECT * FROM pubs;"

    cur.execute(sql)
    
    pubs = cur.fetchall()
    results = [dict(row) for row in pubs]
    print(results)

    return jsonify(results)
    # return 'ok'

@app.get("/add-pub-data")
def add_pub_data():

    pubs = [
    {"name": "Bodega", "address": "Cornmarket St", "email": "orders@bodega.ie", 
        "phone": "021 96969696", "img": "./images/bodega.jpg"},
    {"name": "Rossinis", "address": "Princes St", "email": "orders@rossinis.ie",
        "phone": "021 454545454", "img": "./images/rossinis.jpg"},
    {"name": "Macdonalds", "address": "Winthrop St", "email": "orders@macdonalds.ie",
        "phone": "021 454545454", "img": "./images/macdonalds.jpg"}
    ]

    import sqlite3 as sql

    conn = sql.connect("./cork-tourism.sqlite")

    cur = conn.cursor() # this is like a file handle
    sql = "INSERT INTO pubs ('name','address','email','phone','img') VALUES "
    i = 0
    for pub in pubs:
        if i > 0:
            sql += ","
        sql += "('{}','{}','{}','{}','{}')".format(pub["name"], pub["address"], pub["email"], pub["phone"], pub["img"])
        i += 1

    print(sql)

    cur.execute(sql)

    conn.commit()

    return "ok"


    