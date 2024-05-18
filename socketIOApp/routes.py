from socketIOApp import app, socketio
from flask import render_template,request,session,url_for,redirect
from flask_socketio import join_room, leave_room, emit
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/join", methods=["GET", "POST"])
def join():
    # check for post method
    if(request.method == "POST"):
        username: str = request.form["username"]
        room_name: str = request.form["roomName"]
        # store the username and room name in session
        session["username"] = username
        session["room_name"] = room_name
        return render_template("chatroom.html", session=session)
    else:
        # handle logged in user
        if(session.get("username") is not None):
            return render_template("chatroom.html", session=session)
        else:
            return redirect(url_for("index"))
        
@socketio.on("join",namespace="/join")
def join(message):
    roomName: str = session.get("room_name")
    username: str = session.get("username")
    join_room(roomName)
    emit("status",{
        "MSG": f"{username} has joined the room."
    }, room = roomName)

    @socketio.on("text", namespace="/join")
    def text(message):
        roomName: str = session.get("room_name")
        username: str = session.get("username")
        emit("message",{ "msg": f"{username}: {message['msg']}"}, room = roomName)
        
    
# handle user leaving    
@socketio.on("left", namespace="/join")
def left(message):
    roomName: str = session.get("room_name")
    username: str = session.get("username")
    leave_room(room = roomName)
    session.clear()
    emit("status",{
        "msg": f"{username} has left the room."
    }, room = roomName)
    