from flask import Blueprint, request, jsonify
from ..odatarequests import *

odata_bp = Blueprint('odata', __name__)

@odata_bp.route('/getmaterialsformachine', methods=['POST'])
def forward_getmaterialsformachine():
    data = request.get_json()
    workcenternumber = data.get('workcenternumber')
    matnumbers = getmatnrsformachine(workcenternumber)
    return jsonify({'matnumbers': matnumbers})

@odata_bp.route('/getcurrentorder', methods=['POST'])
def forward_getcurrentorder():
    data = request.get_json()
    workcenternumber = data.get('workcenternumber')
    currentorderinfo = getcurrentorderinfo(workcenternumber)
    return jsonify({'currentorderinfo': currentorderinfo})

@odata_bp.route('/getrecentordersoverview', methods=['POST'])
def forward_getrecentordersoverview():
    data = request.get_json()
    workcenternumber = data.get('workcenternumber')
    mostrecentordersinfo = getrecentordersoverview(workcenternumber)
    return jsonify({'mostrecentordersinfo': mostrecentordersinfo})

@odata_bp.route('/gettodaysoutput', methods=['POST'])
def forward_gettodaysoutput():
    data = request.get_json()
    workcenternumber = data.get('workcenternumber')
    todaysoutput = gettodaysoutput(workcenternumber)
    return jsonify({'todaysoutput': todaysoutput})




