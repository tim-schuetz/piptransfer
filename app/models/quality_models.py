from . import db

class Defectstableone(db.Model): #Folie 1 links
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String)
    origin = db.Column(db.String)
    amount = db.Column(db.Integer)
    issue = db.Column(db.Integer)
    supplier = db.Column(db.String)
    iscasting = db.Column(db.Boolean)
    month = db.Column(db.String)

class Defectstabletwo(db.Model): #die PowerPoint Folie 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    product = db.Column(db.String)
    material = db.Column(db.String)
    method = db.Column(db.String)
    issue = db.Column(db.String)
    cost = db.Column(db.Integer)
    month = db.Column(db.String)

