from flask import Blueprint, request, jsonify
from app.models import *

machines_bp = Blueprint('machines', __name__)

@machines_bp.route('/addnewmachine', methods=['POST'])
def addmachine():
    print('\n\n\naddnewmachine wurde aufgerufen\n\n\n')  # DEBUG HINZUGEFÜGT
    data = request.get_json()
    workcenter = data.get('workcenter')
    name = data.get('name')
    materials = data.get('materials')
    newmachine = Machines(machinename=name, machineworkcenter=workcenter, active=True)
    db.session.add(newmachine)
    db.session.commit()

    for material in materials:
        newmaterial = Machine_material(materialnumber=material, machineworkcenter=workcenter)
        db.session.add(newmaterial)
    db.session.commit()

    return jsonify({'change': 'succesfull'}), 200

#addmachine: http://localhost:5000/addmachine?machinename=Kadia10&machineworkcenter=CP234

@machines_bp.route('/deletemachine', methods=['POST'])
def deletemachine():
    data = request.get_json()
    workcenter = data.get('workcenter')
    Machines.query.filter_by(machineworkcenter=workcenter).delete()
    db.session.commit()
    Machine_material.query.filter_by(machineworkcenter=workcenter).delete()
    return jsonify({'deletion': 'successful'}), 200

@machines_bp.route('/maschinenliste')
def maschinenliste():
    machines_unformatted = Machines.query.all()
    machines = []
    for machine in machines_unformatted:
        machines.append({'workcenter': machine.machineworkcenter,
            'name': machine.machinename,
            'active': machine.active
        })

    return jsonify({ 'verfuegbaremaschinen':machines })

@machines_bp.route('/changemachineactivationstatus', methods=['POST'])
def changemachineactivationstatus():
    data = request.get_json()
    machineworkcenter = data.get('machineworkcenter')
    newstatus = bool(data.get('newstatus'))

    if machineworkcenter is None or newstatus is None:
        return jsonify({'error': 'machineworkcenter or newstatus is not defined'}), 400

    machine = Machines.query.filter_by(machineworkcenter = machineworkcenter).first()
    if not machine:
        print('Workcenter in activationstatuschange nicht gefunden')
        return jsonify({'error': 'machine not found'}), 404
    machine.active = newstatus
    db.session.commit()

    return '', 204

@machines_bp.route('/fetchmateriallist')
def fetchmateriallist():
    materials_raw = Machine_material.query.all()
    materials = []
    for material in materials_raw:
        materials.append({'materialnumber': material.materialnumber, 'machineworkcenter': material.machineworkcenter})
    return jsonify({'materials': materials})

@machines_bp.route('/removematerial', methods=['POST'])
def removematerial():
    data = request.get_json()
    materialnumber = data.get('materialnumber')
    Machine_material.query.filter_by(materialnumber=materialnumber).delete()
    db.session.commit()
    return jsonify({'success': "true"})

@machines_bp.route('/getmaterialsformachine')
def getmatnrsformachine():

    data = request.get_json()
    workcenter = data.get('workcenternumber')    
    
    # workcenter = '530133N'

    try:

        results = (
            db.session.query(
                Machine_material.materialnumber
            )
            .filter(
                Machine_material.machineworkcenter == workcenter
            )
            .all()
        )

        materials = [material.materialnumber for material in results]

        if len(materials) > 0:

            uniquemateriallist = list(set(materials))

            return jsonify({'matnumbers': uniquemateriallist})
        
        return jsonify({'matnumbers': []})
    
    except Exception as e:
        
        print("Error:", e)

        return jsonify({'matnumbers': []})

