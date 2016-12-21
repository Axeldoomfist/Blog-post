import datetime
import os
import hashlib
from flask import Flask, jsonify, request, json
from flask_cors import CORS, cross_origin

NOW = datetime.datetime.now()
APP = Flask(__name__)

def openfile(file):
    """Gets a file and returns the output"""
    try:
        with open(file) as loading:
            loaded = loading.read()
            return loaded

    except IOError:
        print('File does not exist')

def writefile(file, contents):
    """Gets a file and writes the specified contents to it"""
    try:
        with open(file, 'w+') as filewri:
            contents_json = json.dumps(contents)
            filewri.write(contents_json)
    except IOError:
        print("Problem with writing to the file")
        raise IOError

def ask():
    """Gets a file from the user"""
    asks = "Post.json"
    return asks

def allposts():
    pids = allpostids()
    posts = []
    for pid in pids:
        file = singlepost(pid)
        posts.append(file)
    return posts

def singlepost(id):
    post = openfile("posts/"+ str(id) + ".json")
    return json.loads(post)

def editpost(id, content):
    file_name = 'posts/' + str(id) + '.json'
    try:
        writefile(file_name, content)
    except IOError:
        print('Error editing the file')
        raise IOError

def getposttable():
    postsobj = json.loads(openfile("posts.json"))
    return postsobj
def allpostids():
    """Gets the post table"""
    ptable = getposttable()
    return ptable['ids']

def allusers():
    uids = alluserids()
    users = []
    for uid in uids:
        file = singleuser(uid)
        users.append(file)
    return users

def singleuser(id):
    usr = openfile("userdata/"+ str(id) + ".json")
    return json.loads(usr)

def edituser(id, content):
    file_name = 'userdata/' + str(id) + '.json'
    try:
        writefile(file_name,content)
    except IOError:
        print('Error editing the file')
        raise IOError

def getusertable():
    userobj = json.loads(openfile("users.json"))
    return userobj

def alluserids():
    """Gets the user table"""
    utable = getusertable()
    return utable['ids']

def hashpswd(password):
    """Hashes the new users password"""
    hashpassword = hashlib.md5(password.encode('UTF-8'))
    hashedpswd = hashpassword.hexdigest()
    return hashedpswd

# Route definitions

#Posts

#Create
@APP.route("/", methods=["PUT"])
def createpost():
    """Creates a post"""
    dtformat = NOW.strftime('%d/%m/%Y')
    timeformat = NOW.strftime('%H:%M')
    pids = allpostids()
    pids.sort()
    pid = pids[0] + 1
    add = request.form['body']
    uid = request.form['uid']   # if request.form['uid'] != None:
                                #     uid = request.form['uid']
    post = {"id": pid, "Date": dtformat, "Time": timeformat, "Post": add, "Userid": uid}
    editpost(pid, post)
    return jsonify({"success": "true", "post_id": pid})

#Read
@APP.route("/<id>", methods=["GET"])
def getpost(id):
    """Main function"""
    post = singlepost(id)
    post_json = jsonify(**post)
    return post_json

@APP.route("/", methods=["GET"])
def getallposts():
    """Gets all the posts"""
    posts = allposts()
    return jsonify(posts)

#Update
@APP.route("/", methods=["POST"])
def changepost():
    """Changes a post"""
    pid = request.form['id']
    post = singlepost(pid)
    change = request.form["body"]
    post['Post'] = change
    try:
        editpost(pid, post)
        return '{"success":"true"}'
    except IOError:
        return '{"success":"false"}'

#Delete
@APP.route("/<int:id>", methods=['DELETE'])
def deletepost(id):
    """Deletes a post"""
    file_name = 'posts/'+ str(id) + '.json'
    try:
        singlepost(id)
    except:
        return '{"success":"false"}'
    os.remove(file_name)
    return '{"success":"true"}'

#Users

#Create
@APP.route("/usr", methods=['PUT'])
def createuser():
    """Creates a user"""
    uids = alluserids()
    uids.sort()
    uid = uids[0] + 1
    newuser = json.loads(request.data)
    newuser['uid'] = uid
    newuser['password'] = hashpswd(newuser['password'])
    edituser(uid, newuser)
    return jsonify({"success": "true", "post_id": uid})

#Read
@APP.route("/usr/<id>", methods=['GET'])
def getuser(id):
    user = singleuser(id)
    user_json = jsonify(**user)
    return user_json

@APP.route("/usr", methods=['GET'])
def getallusers():
    """Gets all the users"""
    users = allusers()
    return jsonify(users)
#Update
@APP.route("/", methods=["POST"])
def changeuser():
    """Changes a users data"""
    cuser = json.loads(request.data)
    try:
        edituser(cuser['id'], cuser)
        return '{"success":"true"}'
    except IOError:
        return '{"success":"false"}'
    
#Delete
@APP.route("/<int:id>", methods=['DELETE'])
def deleteuser(id):
    file_name = 'userdata/'+ str(id) + '.json'
    try:
        singleuser(id)
    except:
        return '{"success":"false"}'
    os.remove(file_name)
    return '{"success":"true"}'

if __name__ == "__main__":
    APP.run()
