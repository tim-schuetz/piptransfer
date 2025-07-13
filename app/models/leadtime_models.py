from . import db

class Leadtimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String)
    kanbanidnumber = db.Column(db.String)
    created = db.Column(db.String)
    creationmonthasint = db.Column(db.Integer)
    time = db.Column(db.String)
    number = db.Column(db.String)
    kanbanstatus = db.Column(db.String)
    order = db.Column(db.String)
    cntcycle = db.Column(db.String)
    leadtimeinh = db.Column(db.String)
    activationstatus = db.Column(db.String)

    # hourssincemonthbeginning = db.Column(db.Integer)


