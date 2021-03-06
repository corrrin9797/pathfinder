import random
from pymongo import MongoClient

conn = MongoClient()

db = conn['1247']


def restart():
    db.idnum.drop()
    n = {"next" : 2}
    db.idnum.insert(n)
    
    db.usertable.drop()
    tdic = {'username': 'testing', 'password':'testing', 'IDs':''}
    db.usertable.insert(tdic)

def getNextID():
    cres = db.idnum.find()
    old  = [r for r in cres][0]["next"]
    new = old + 1
    db.idnum.update ({'next':old}, {"$set": {'next':new}})
    
    return old

def printData():
    cres = db.usertable.find()
    #{}, {'_id':False})
    #print cres
    #res = [r
    for r in cres:
        print r

def validate(usernamei, passwordi):
    cres = db.usertable.find({'username': usernamei,'password':passwordi})
    res = [r for r in cres]  
    if len(res)>0:
        return True
    return False

#def validate(usernamei, passwordi):
#    def decorate(func):
#        def inner(*args):
#            cres = db.usertable.find({'username': usernamei,'password': passwordi})
#            res = [r for r in cres]  
#            if len(res)>0:
#                return func(args, kwargs)
#            
#            error = "Invalid credentials"
#            return render_template ("login.html", error = error)
#        return inner

def addUser(usernamei, passwordi):
    cres = db.usertable.find({'username':usernamei})
    res = [r for r in cres]
    print res
    if len(res)>0:
        return False
    nu = {'username': usernamei, 'password':passwordi, 'IDs':''}
    db.usertable.save(nu)
    return True


def updateUser(usernamei, passwordi, passwordn):
    if validate (usernamei, passwordi):
        db.usertable.update ({'username':usernamei, 'password':passwordi}, {"$set": {'username': usernamei, 'password':passwordn}})
        return True
    return False
    
def addID (username, idnum):
    cres = db.usertable.find({'username':username})
    res = [r for r in cres]
    old = res[0]["IDs"]
    if old == "":
        new = str(idnum)
    else:
        new = old + "," + str(idnum)
    db.usertable.update ({'username':username}, {"$set": {'IDs':new}})


def getIDs (username):
    cres = db.usertable.find({'username':username})
    res = [r for r in cres][0]
    return res["IDs"].encode("ascii").split(",") 
