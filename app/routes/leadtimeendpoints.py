from flask import Blueprint, request, jsonify
from app.models import *
from datetime import datetime
import pandas as pd
from sqlalchemy import desc
import statistics
from ..leadtimedatasource import updatekanbandatabase, extractmonthasnumberfromdate
from sqlalchemy import func, cast, Float

leadtime_bp = Blueprint('leadtime', __name__)

#Testing:

@leadtime_bp.route('/exposekanbandatabase')
def exposekanbandatabase():

    results = Leadtimetable.query.all()
    
    response = [[r.material, r.kanbanidnumber, r.created, r.time, r.number, r.kanbanstatus, r.order, r.cntcycle, r.leadtimeinh, r.activationstatus] for r in results]
    responselength = len(response)

    return jsonify({'responselength': responselength, 'response': response})

#Production:

@leadtime_bp.route('/getkanbanfilteroptions')
def getfilteroptions():
    uniquematerialslist = [r[0] for r in db.session.query(Leadtimetable.material).distinct()]
    uniqueloopslist = [r[0] for r in db.session.query(Leadtimetable.cntcycle).distinct()]
    uniquemonths_as_int = [r[0] for r in db.session.query(Leadtimetable.creationmonthasint).distinct()]
    return jsonify({'uniquematerialslist': uniquematerialslist, 'uniqueloopslist': uniqueloopslist, 'uniquemonths_as_int': uniquemonths_as_int})

@leadtime_bp.route('/updatekanbandatabase')
def redirect_updatekanbandatabase():
    updatekanbandatabase()
    return jsonify({'updated': 'successful'}), 200

@leadtime_bp.route('/getkpivalues', methods=['POST'])
def getkpivalues():
    data = request.get_json()
    materials = data.get('material')
    loop = data.get('loop')
    monthasint = data.get('monthasint')

    query = db.session.query(
        func.min(Leadtimetable.leadtimeinh).label('leadtime_min'),
        func.max(Leadtimetable.leadtimeinh).label('leadtime_max'),
        func.avg(Leadtimetable.leadtimeinh).label('leadtime_avg')
    )

    if materials and len(materials) > 0:
        query = query.filter(Leadtimetable.material.in_(materials))

    if loop and loop != 'all':
        query = query.filter(Leadtimetable.cntcycle == loop)

    if monthasint and monthasint != 'all':
        query = query.filter(Leadtimetable.creationmonthasint == int(monthasint))

    # results = query.all()
    # result = results[0]

    result = query.one()

    return jsonify({
        'minleadtime': result.leadtime_min,
        'maxleadtime': result.leadtime_max,
        'avgleadtime': round(result.leadtime_avg, 2) if result.leadtime_avg is not None else None
    })

@leadtime_bp.route('/getleadtimebymatnrs', methods=['POST'])
def leadtimebymatnrs():

    #Am Ende noch nach der Dauer der Durchlaufzeit absteigend sortieren

    data = request.get_json()
    materials = data.get('materials')
    loop = data.get('loop')
    monthasint = data.get('monthasint')
    xaxisparameter = data.get('xaxisparameter')

    print("loop:", loop, "monthasint:", monthasint, "materials:", materials, "xaxisparameter:", xaxisparameter)

    query = db.session.query(
        Leadtimetable.material,
        Leadtimetable.kanbanidnumber,
        Leadtimetable.order,
        func.avg(cast(Leadtimetable.leadtimeinh, Float)).label('average_leadtime')
    )

    if materials and len(materials) > 0:
        query = query.filter(Leadtimetable.material.in_(materials))

    if loop and loop != 'all':
        query = query.filter(Leadtimetable.cntcycle == loop)

    if monthasint and monthasint != 'all':
        query = query.filter(Leadtimetable.creationmonthasint == int(monthasint))

    if xaxisparameter == 'material':
        query = query.group_by(Leadtimetable.material)
    elif xaxisparameter == 'kanbanid':
        query = query.group_by(Leadtimetable.kanbanidnumber)
    else:
        query = query.group_by(Leadtimetable.order)

    results = query.all()

    xaxisvalues = [r.material for r in results]
    leadtimes = [round(r.average_leadtime, 2) if r.average_leadtime is not None else None for r in results]

    for i in range(len(leadtimes) - 1, -1, -1):
        if leadtimes[i] is None:
            leadtimes.pop(i)
            xaxisvalues.pop(i)

    print ("xaxisvalues:", xaxisvalues, 'leadtimes:', leadtimes)

    return jsonify({
        'materials': xaxisvalues,
        'leadtimes': leadtimes
    })

