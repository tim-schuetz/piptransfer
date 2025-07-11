from . import db

class Mostfrequentscrapissuecauses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String)
    mostfrequenttissue = db.Column(db.String)
    mostfrequenttissue_cost = db.Column(db.Integer)
    secondmostfrequenttissue = db.Column(db.String)
    secondmostfrequenttissue_cost = db.Column(db.Integer)
    thirdmostfrequenttissue = db.Column(db.String)
    thirdmostfrequenttissue_cost = db.Column(db.Integer)

class Worstmethodsforspoolscrap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String)
    costofassembly = db.Column(db.Integer)
    costofgrinding = db.Column(db.Integer)
    costofturning = db.Column(db.Integer)