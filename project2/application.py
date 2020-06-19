import os, sys, requests, datetime
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
socketio = SocketIO(app)

loggedin_users=[]
channelslist=[]
channelmessages=dict()


@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        uname=request.form.get("username")
        if uname in loggedin_users:
            return render_template("error.html",msg="User is loggedin already with that username")
        session["username"]=uname
        loggedin_users.append(uname)
        return redirect("/channels")

@app.route("/channels",methods=["GET","POST"])
def channels():
    if request.method == "GET":
        return render_template("main.html",cname="",channelslist=channelslist)
    else:
        channelname=request.form.get("channelname")
        if channelname in channelslist:
            return render_template("error.html",msg="Channel already exists.")
        else:
            channelslist.append(channelname)
            channelmessages[channelname]=[]
            return render_template("main.html",cname=channelname,channelslist=channelslist)

@app.route("/viewchannel/<string:channelname>",methods=["GET","POST"])
def viewchannel(channelname):
    if request.method == "GET":
        return render_template("channel.html",channelname=channelname,msglist=channelmessages[channelname],username=session["username"])

@socketio.on("add message")
def add_message(data):
    time=datetime.datetime.now().strftime("%I:%M:%S on %d/%m/%Y")
    msgcontent={"time": time, "user": session["username"], "msg": data["message"]}
    c=data['cname']
    if(len(channelmessages[c])==100):
        channelmessages.pop(0)
    channelmessages[c].append(msgcontent)
    emit("display message",{"time": time, "user": session["username"], "msg": data["message"]},broadcast=True)

@socketio.on("delete message")
def delete_message(data):
    print(channelmessages)
    print(data,file=sys.stdout)
    r={'user':data['username'],'msg':data['msg'],'time':data['time']}
    channelmessages[data['cname']].remove(r);
    print(channelmessages)
    emit("removed",data,broadcast=True)



@app.route("/logout",methods=["GET"])
def logout():
    loggedin_users.remove(session["username"])
    session.pop('username')
    return redirect("/")
