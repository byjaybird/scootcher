
#primary python document that controls the whole application.

import os
import sqlite3

#pyserial to talk to serial port
import serial
import flask

from time import sleep

from flask import Flask, render_template, jsonify, request

#404 type errors
from werkzeug.exceptions import abort

#create connection to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    #assigns row names to act like python libraries
    conn.row_factory = sqlite3.Row
    return conn

#Calls DB to get all data about a user by name
def get_user_data(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?',
                        (username,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user

#Calls DB to get points data about a user by userid
def get_points_data(userid):
    conn = get_db_connection()
    points = conn.execute('SELECT * FROM points WHERE userid = ?',
                          (userid,)).fetchone()
    conn.close()
    if points is None:
        abort(404)
    return points

def change_points(userid, pointchange):
    conn = get_db_connection()
    print(userid)
    print(pointchange)
    print("here in the point changer")
    points = conn.execute('SELECT * FROM points WHERE userid = ?',
                          (userid,)).fetchone()
    currentpoints = points['points']
    
    newpoints = currentpoints + pointchange

    cur = conn.cursor()
    cur.execute('UPDATE points SET points = ? WHERE userid = ?',
                ((newpoints), (userid)))
    conn.commit()
    conn.close()
    return

def change_tokens(userid, tokenchange):
    conn = get_db_connection()
    print(userid)
    print(tokenchange)
    print("here in the token changer")
    points = conn.execute('SELECT * FROM points WHERE userid = ?',
                          (userid,)).fetchone()
    currenttokens = points['tokens']
    
    newtokens = currenttokens + tokenchange

    cur = conn.cursor()
    cur.execute('UPDATE points SET tokens = ? WHERE userid = ?',
                ((newtokens), (userid)))
    conn.commit()
    conn.close()
    return
##
##
## Experimental Stuff
##
##
#function to initialize serial connection with a Scootchbot
def scootchbot():
    messageid = 0
    ser=serial.Serial()
    ser.port = '/dev/cu.usbmodemECDA3B60107C2'
    # cu.usbmodemECDA3B60107C2
    # tty.usbmodemECDA3B60107C2
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0
    try:
        ser.open()
    except serial.SerialException as e:
         yield 'event:error\n' + 'data:' + 'Serial port error({0}): {1}\n\n'.format(e.errno, e.strerror)
         messageid = messageid + 1
    str_list = []
    while True:
        sleep(0.01)
        nextchar = ser.read()
        if nextchar:
            str_list.append(nextchar)
        else:
            if len(str_list) > 0:
                yield 'id:' + str(messageid) + '\n' + 'data:' + ''.join(str_list) + '\n\n'
                messageid = messageid + 1
                str_list = []


app = Flask(__name__)

#Home Page
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    print("Home Page Success")
    return render_template('index.html', users=users )

# Game Page
@app.route('/<string:username>')
def fetchgamepage(username):
    user = get_user_data(username)
    userid = user['userid']
    points = get_points_data(userid)
    print("game Page load success")
    return render_template('game.html', user=user, points=points)


##
##
## Experimental Stuff
##
##
@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        activeplayer = request.form.get("player")

    print(activeplayer)

    ##Make The ScootchBot Play
    print("in the play function")
    activeplayer = 'jake'
    user = get_user_data(activeplayer)
    userid = user['userid']
    change_points(userid,25)
    change_tokens(userid,-25)
    points = get_points_data(userid)
    
    return render_template('index.html')

# Trying to control the scootchbot
@app.route('/scootchbot')
def scootcher():
    newresponse = flask.Response(scootchbot(), mimetype="text/event-stream")
    newresponse.headers.add('Access-Control-Allow-Origin', '*')
    newresponse.headers.add('Cache-Control', 'no-cache')
    return newresponse

