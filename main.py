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

def allposts():
    """Gets all the post ids"""
    pids = allids('post')
    posts = []
    for pid in pids:
        file = singleaccess(pid, 'posts/')
        posts.append(file)
    return posts

def singleaccess(id, name):
    """Gets the file that is selected"""
    post = openfile(name + str(id) + ".json")
    return json.loads(post)

def editpost(id, content):
    """Edits the content of the post selected"""
    file_name = 'posts/' + str(id) + '.json'
    try:
        writefile(file_name, content)
    except IOError:
        print('Error editing the file')
        raise IOError

def update(id, name):
    """Updates the total amount made"""
    file_name = name +'.json'
    idup = json.loads(openfile(file_name))
    idup['ids'].append(id)
    writefile(file_name, idup)

def delete(id, name):
    """Updates the total amount made"""
    file_name = name +'.json'
    idup = json.loads(openfile(file_name))
    idup['ids'].pop(id)
    writefile(file_name, idup)

def gettable(name):
    """Gets the amount of the selected item made"""
    table_data = json.loads(openfile(name + ".json"))
    return table_data

def allids(name):
    """Gets the selected table"""
    ptable = gettable(name)
    return ptable['ids']

def allusers():
    """Gets all the user ids"""
    uids = allids('users')
    users = []
    for uid in uids:
        file = singleaccess(uid, 'userdata/')
        users.append(file)
    return users

def edituser(id, content):
    """Edits the user that is selected"""
    file_name = 'userdata/' + str(id) + '.json'
    try:
        writefile(file_name, content)
    except IOError:
        print('Error editing the file')
        raise IOError

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
    pids = allids('post')
    pids.sort(reverse=True)
    pid = pids[0] + 1
    newpost = json.loads(request.data)
    newpost['id'] = pid
    newpost['date'] = dtformat
    newpost['time'] = timeformat
    editpost(pid, newpost)
    update(pid, 'post')
    return jsonify({"success": "true", "post_id": pid})

#Read
@APP.route("/post/<id>", methods=["GET"])
def getpost(id):
    """Gets the specified post"""
    post = singleaccess(id, 'posts/')
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
    post = singleaccess(pid, 'posts/')
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
        singleaccess(id, 'posts/')
        delete(id, 'posts')
    except:
        return '{"success":"false"}'
    os.remove(file_name)
    return '{"success":"true"}'

#Users

#Create
@APP.route("/usr", methods=['PUT'])
def createuser():
    """Creates a user"""
    uids = allids('users')
    uids.sort(reverse=True)
    uid = uids[0] + 1
    try:
        newuser = json.loads(request.data)
        newuser['uid'] = uid
        newuser['password'] = hashpswd(newuser['password'])
        edituser(uid, newuser)
        update(uid, 'users')
    except:
        return '{"success":"false"}'
    return jsonify({"success": "true", "user_id": uid})

#Read
@APP.route("/usr/<id>", methods=['GET'])
def getuser(id):
    """Gets the specified user"""
    user = singleaccess(id, 'userdata/')
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
        singleaccess(id, 'userdata/')
        delete(id, 'users')
    except:
        return '{"success":"false"}'
    os.remove(file_name)
    return '{"success":"true"}'

if __name__ == "__main__":
    APP.run()
