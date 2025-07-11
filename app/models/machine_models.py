from . import db

class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machineworkcenter = db.Column(db.String)
    machinename = db.Column(db.String)
    active = db.Column(db.Boolean)

# class Materials(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     materialnumber = db.Column(db.String)

class Machine_material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materialnumber = db.Column(db.String)
    machineworkcenter = db.Column(db.String)

