import os
import requests
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import users

app=Flask(__name__)
app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")
socketio=SocketIO(app)
db_users={}
db_channels={}

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
  if request.method=='POST':
    ok, message=users.signup(db_users, request.form.get('name'), request.form.get('password'), request.form.get('retype'))
    if ok:
      return render_template('list_channels.html', curr_username=request.form.get('name'), channels=db_channels.keys())
    else:
      return render_template('signup.html', message=message, name=request.form.get('name'), password=request.form.get('password'), retype=request.form.get('retype'))
  else:
    return render_template('signup.html', message='', name='', password='', retype='')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
  if request.method=='POST':
    ok, message=users.signin(db_users, request.form.get('name'), request.form.get('password'))
    if ok:
      return render_template('list_channels.html', curr_username=request.form.get('name'), channels=db_channels.keys())
    else:
      return render_template('signin.html', message=message, name=request.form.get('name'), password=request.form.get('password'))
  else:
    return render_template('signin.html', message='', name='', password='')

@app.route("/signin_auto", methods=['GET'])
def signin_auto():
  curr_username=request.args.get('curr_username')
  curr_channel=request.args.get('curr_channel')
  if curr_username in db_users.keys():
    if curr_channel in db_channels.keys():
      return render_template('channel.html', curr_channel=curr_channel, edits=db_channels[curr_channel])
    else:
      return render_template('list_channels.html', curr_username=curr_username, channels=db_channels.keys())
  else:
    return render_template('signin.html', message='', name='', password='')

@app.route("/signout")
def signout():
  return render_template('signout.html')

@app.route("/list_usernames", methods=['GET'])
def list_usernames():
  return render_template('list_usernames.html', usernames=db_users.keys())

@app.route("/list_channels", methods=['GET'])
def list_channels():
  return render_template('list_channels.html', channels=db_channels.keys())

@app.route("/channel", methods=['GET', 'POST'])
def channel():
  if request.method=='POST':
    curr_channel=request.form.get('channel')
  else:
    curr_channel=request.args.get('curr_channel')

  if not curr_channel:
    return list_channels()
  elif curr_channel not in db_channels.keys():
    db_channels[curr_channel]=[]
  return render_template('channel.html', curr_channel=curr_channel, edits=db_channels[curr_channel])

@socketio.on('submit edit')
def edit(data):
  curr_channel=data['channel']
  del data['channel']
  db_channels[curr_channel].append(data)
  _=len(db_channels[curr_channel])
  if _>100:
      db_channels[curr_channel]=db_channels[curr_channel][_-100:-1]
  emit("announce edit "+curr_channel, data, broadcast=True)

if __name__=='__main__':
  app.run(debug=True)
