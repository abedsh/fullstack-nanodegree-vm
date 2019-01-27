'''
Created on Aug 30, 2018

@author: abedch
'''
# a util module for generic CRUD functions
from app import db_session


# update will accept any object declared to the SQLalchamy engine
def update(object):
    try:
        objToUpdate = db_session.query(type(object)).filter_by(id=object.id)
        objToUpdate.update(object.toMappedValues())
        db_session.commit()
    except:
        db_session.rollback()
    finally:
        closeDbSession()

# update will accept any object declared to the SQLalchamy engine
def getById(type,id):
    try:
        o = db_session.query(type).filter_by(id=object.id)
    except:
        db_session.rollback()
    finally:
        closeDbSession()



# update will accept any object declared to the SQLalchamy engine
def add(object):
    try:
        db_session.add(object)
        db_session.commit()
    except:
        db_session.rollback()
    finally:
        closeDbSession()


# delete requires an the object type to be deleted and its id
def deleteById(object, item_id):
    try:
        db_session.query(type(object)).filter_by(id=item_id).delete()
        db_session.commit()
    except:
        db_session.rollback()
    finally:
        closeDbSession()


# returns db session
def getDbSession():
    return db_session


# closes db session
def closeDbSession():
    db_session.close_all()
