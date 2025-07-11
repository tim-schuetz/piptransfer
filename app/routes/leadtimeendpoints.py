from flask import Blueprint, request, jsonify
from app.models import *
from datetime import datetime
import pandas as pd
from sqlalchemy import desc
import statistics
from ..leadtimedatasource import updatekanbandatabase, extractmonthasnumberfromdate

leadtime_bp = Blueprint('leadtime', __name__)

@leadtime_bp.route('/getkanbandata', methods=['POST'])
def getkanbandata():

    uniquedates = [r[0] for r in db.session.query(Leadtimetable.created).distinct()]
    uniquedates_monthasint = [int(date[6:7]) if not str(date[6:7]).startswith("0") else int(date[7]) for date in uniquedates]
    uniquemonths_asint = list(set(uniquedates_monthasint))
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    uniquemonths_asstring = [months[monthint] for monthint in uniquemonths_asint]

    monthselectoptions = {'monthsasnumber': uniquemonths_asint, 'monthsasword': uniquemonths_asstring}

    uniquematerialslist = [r[0] for r in db.session.query(Leadtimetable.material).distinct()]

    uniqueloopslist = [r[0] for r in db.session.query(Leadtimetable.cntcycle).distinct()]


    data = request.get_json()
    material = data.get('material')
    loop = data.get('loop')
    sortfor = data.get('sortfor')

    print('material:', material, 'loop:', loop, 'sortfor:', sortfor)

    query = (
        db.session.query(
            Leadtimetable
        )
        .filter(
            Leadtimetable.kanbanstatus == 2,
        ) # Entweder nur Status 2 oder nur Status 5 damit nicht doppelt (am besten nur Status 2, damit die noch offenen sichtbar)
    )

    if material and material.lower() != 'all':
        query = query.filter(Leadtimetable.material == material)

    if loop and loop.lower() != 'all':
        query = query.filter(Leadtimetable.cntcycle == loop)

    if sortfor and sortfor == 'leadtime':
        query = query.order_by(desc(Leadtimetable.leadtimeinh))
    elif sortfor and sortfor == 'kanbanID':
        query = query.order_by(desc(Leadtimetable.kanbanidnumber))
    else:
        query =query.order_by(desc(Leadtimetable.created))

    results = query.all()

    kanbaninfos = [{'material': result.material, 'idnumber': result.id, 'creationdate': result.created, 'creationtime': result.time, 'status': result.kanbanstatus, 'ordernumber': result.order, 'cntcycle': result.cntcycle, 'leadtimeinh': result.leadtimeinh, 'activationstatus': result.activationstatus, 'month': extractmonthasnumberfromdate(result.created), 'hourssincemonthbeginning': result.hourssincemonthbeginning} for result in results]

    leadtimeinfos = [float(result.leadtimeinh) for result in results]

    avgleadtime = statistics.mean(leadtimeinfos) if len(leadtimeinfos) > 0 else None
    minleadtime = min(leadtimeinfos) if len(leadtimeinfos) > 0 else None
    maxleadtime = max(leadtimeinfos) if len(leadtimeinfos) > 0 else None

    totalvalues = len(kanbaninfos)

    return jsonify({'kanbaninfos':kanbaninfos, 'uniquematerialslist': uniquematerialslist, 'uniqueloopslist': uniqueloopslist, 'monthselectoptions':monthselectoptions, 'avgleadtime': avgleadtime, 'minleadtime': minleadtime, 'maxleadtime': maxleadtime, 'totalvalues': totalvalues})


@leadtime_bp.route('/updatekanbandatabase')
def redirect_updatekanbandatabase():
    updatekanbandatabase()
    return jsonify({'updated': 'successful'}), 200

@leadtime_bp.route('/exposekanbandatabase')
def exposekanbandatabase():

    results = Leadtimetable.query.all()
    
    response = [[r.material, r.kanbanidnumber, r.created, r.time, r.number, r.kanbanstatus, r.order, r.cntcycle, r.leadtimeinh, r.activationstatus] for r in results]
    responselength = len(response)

    return jsonify({'responselength': responselength, 'response': response})

