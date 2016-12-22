import datetime
import os
import hashlib
import binascii
from flask import Flask, jsonify, request, json
from flask_cors import CORS, cross_origin

NOW = datetime.datetime.now()
APP = Flask(__name__)
CORS(APP)

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
    """Gets all the post ids"""
    pids = allpostids()
    posts = []
    for pid in pids:
        file = singlepost(pid)
        posts.append(file)
    return posts

def singlepost(id):
    """Gets the file of the post that is selected"""
    post = openfile("posts/"+ str(id) + ".json")
    return json.loads(post)

def editpost(id, content):
    """Edits the content of the post selected"""
    file_name = 'posts/' + str(id) + '.json'
    try:
        writefile(file_name, content)
    except IOError:
        print('Error editing the file')
        raise IOError

def updatepost(id):
    """Updates the total amount of posts made"""
    file_name = 'posts.json'
    posts = json.loads(openfile(file_name))
    posts['ids'].append(id)
    writefile(file_name, posts)

def deletepst(id):
    """Updates the total amount of posts made"""
    file_name = 'posts.json'
    posts = json.loads(openfile(file_name))
    posts['ids'].pop(id-1)
    writefile(file_name, posts)

def getposttable():
    """Gets the amount of posts made"""
    postsobj = json.loads(openfile("posts.json"))
    return postsobj
def allpostids():
    """Gets the post table"""
    ptable = getposttable()
    return ptable['ids']

def allusers():
    """Gets all the user ids"""
    uids = alluserids()
    users = []
    for uid in uids:
        file = singleuser(uid)
        users.append(file)
    return users

def singleuser(id):
    """Gets the file of the user that is selected"""
    usr = openfile("userdata/"+ str(id) + ".json")
    return json.loads(usr)

def edituser(id, content):
    """Edits the user that is selected"""
    file_name = 'userdata/' + str(id) + '.json'
    try:
        writefile(file_name, content)
    except IOError:
        print('Error editing the file')
        raise IOError

def updateusr(id):
    """Updates the total amount of users created"""
    file_name = 'users.json'
    users = json.loads(openfile(file_name))
    users['ids'].append(id)
    writefile(file_name, users)

def delusr(id):
    """Updates the total amount of users created"""
    file_name = 'users.json'
    users = json.loads(openfile(file_name))
    users['ids'].pop(id-1)
    writefile(file_name, users)

def getusertable():
    """Gets the amount of users made"""
    userobj = json.loads(openfile("users.json"))
    return userobj

def alluserids():
    """Gets the user table"""
    utable = getusertable()
    return utable['ids']

def hashpswd(password):
    """Hashes the users password"""
    salt = binascii.hexlify(os.urandom(20)).decode()
    hashpassword = hashlib.md5(salt.encode('UTF-8') + password.encode('UTF-8'))
    hashedpswd = hashpassword.hexdigest() + ':' + salt
    return hashedpswd

def checkpswd(hashedpswd, user_pswd):
    """Checks the users password"""
    password, salt = hashedpswd.split(':')
    hashpassword = hashlib.md5(salt.encode('UTF-8') + user_pswd.encode('UTF-8'))
    hashedpswd = hashpassword.hexdigest()
    return password

# Route definitions

#Posts

#Create
@APP.route("/post", methods=["PUT"])
def createpost():
    """Creates a post"""
    dtformat = NOW.strftime('%d/%m/%Y')
    timeformat = NOW.strftime('%H:%M')
    pids = allpostids()
    pids.sort(reverse=True)
    pid = pids[0] + 1
    newpost = json.loads(request.data)
    newpost['id'] = pid
    newpost['date'] = dtformat
    newpost['time'] = timeformat
    editpost(pid, newpost)
    updatepost(pid)
    return jsonify({"success": "true", "post_id": pid})

#Read
@APP.route("/post/<id>", methods=["GET"])
def getpost(id):
    """Gets the specified post"""
    post = singlepost(id)
    post_json = jsonify(**post)
    return post_json

@APP.route("/post", methods=["GET"])
def getallposts():
    """Gets all the posts"""
    posts = allposts()
    return jsonify(posts)

#Update
@APP.route("/post", methods=["POST"])
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
@APP.route("/post/<int:id>", methods=['DELETE'])
def deletepost(id):
    """Deletes a post"""
    file_name = 'posts/'+ str(id) + '.json'
    try:
        singlepost(id)
        deletepst(id)
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
    uids.sort(reverse=True)
    uid = uids[0] + 1
    try:
        newuser = json.loads(request.data)
        newuser['uid'] = uid
        newuser['password'] = hashpswd(newuser['password'])
        edituser(uid, newuser)
        updateusr(uid)
    except:
        return '{"success":"false"}'
    return jsonify({"success": "true", "user_id": uid})

#Read
@APP.route("/usr/<id>", methods=['GET'])
def getuser(id):
    """Gets the specified user"""
    user = singleuser(id)
    user_json = jsonify(**user)
    return user_json

@APP.route("/usr", methods=['GET'])
def getallusers():
    """Gets all the users"""
    users = allusers()
    return jsonify(users)
#Update
@APP.route("/usr", methods=["POST"])
def changeuser():
    """Changes a users data"""
    cuser = json.loads(request.data)
    cuser['password'] = hashpswd(cuser['password'])
    try:
        edituser(cuser['uid'], cuser)
        return '{"success":"true"}'
    except IOError:
        return '{"success":"false"}'

#Delete
@APP.route("/usr/<int:id>", methods=['DELETE'])
def deleteuser(id):
    """Deletes the selected user"""
    file_name = 'userdata/'+ str(id) + '.json'
    try:
        singleuser(id)
        delusr(id)
    except:
        return '{"success":"false"}'
    os.remove(file_name)
    return '{"success":"true"}'

if __name__ == "__main__":
    APP.run()
