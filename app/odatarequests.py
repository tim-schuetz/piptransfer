import requests
import json
from datetime import datetime, timedelta
import isodate
from .models import *

api_key_cn = '138702f4-da0f-4404-8a52-5a76d6f78003'
endpoint_cn = 'https://ews-esz-emea.api.bosch.com/manufacturing/production-order/RB9S-PEX_PRORD_SRV/PRP/v2/'

plant_cn = 'CN50'
material_cn = 'R988114969'
workcenter_cn = '523246N'

api_key_cn_qrp = '240270ef-9b4f-473c-88f7-e56d13b8658b'
endpoint_cn_qrp = 'https://ews-esz-emea.api.bosch.com/manufacturing/production-order/RB9S-PEX_PRORD_SRV/QRP/v2/'

materialnummerinfos_url = f"{endpoint_cn}A_ProductionOrder?$filter=ProductionPlant eq '{plant_cn}' and Material eq '{material_cn}'&$top=3"
nachbausfc015_url = f"{endpoint_cn}A_ProductionOrderOperation?$filter=WorkCenter eq '{workcenter_cn}'&$top=3"

# for content in contents:
#     customers.append(content.get('CustomerName'))
#     materialsinformation.append({'material': content.get('Material'), 'customer': content.get('CustomerName'), 'quantity': content.get('MfgOrderConfirmedYieldQty')})

def getmatnrsformachine(workcenter):

    workcenter = '530133N'

    # 1) Prüfen, ob bereits Materialnummern auf der Maschine eingetragen sind

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

        return uniquemateriallist

    # 2.1) (Falls keine Einträge in der DB vorhanden, dann in SAP schauen) Die Auftragsnummern von den Maschinen ziehen:

    latestmatnrsURL = (
        f"{endpoint_cn}A_ProductionOrderOperation?"
        f"$filter=WorkCenter eq '{workcenter}' and OpActualExecutionStartDate ge datetime'2024-01-01T00:00:00'&"
        f"$top=50"
    )

    headers = {
        'KeyId': api_key_cn,
        'Accept': 'application/json',
        'SAP-language': 'EN' #DE
    }
    # print("URL, headers:", latestmatnrsURL, headers)
    response = requests.get(latestmatnrsURL, headers=headers, verify=False)

    if response.status_code != 200:
        print(f"Fehler bei SAP Abfrage: {response.status_code} - {response.text}")
        return []

    # print("\n\n\nresponse.status_code:", response.status_code, "\nresponse.text:", response.text, "\n\n\n")
    data_dict = response.json()
    # with open('output.json', 'w') as json_file:
    #     json.dump(data_dict, json_file, indent=4)

    if not 'd' in data_dict or not 'results' in data_dict['d'] or not data_dict['d']['results'] or not data_dict['d']['results'] or not len(data_dict['d']['results']) > 0:
        print("empty response")
        return []

    contents = data_dict['d']['results']

    orders = []

    for content in contents:
        mfgorder = content['ManufacturingOrder']
        orders.append(mfgorder)

    # 2.2) Die Materialnummern von den Auftragsnummern ziehen 

    materials = []

    for order in orders:

        ordernumberinfosurl = f"{endpoint_cn}A_ProductionOrderItem?$filter=ManufacturingOrder eq '{order}'&$top=1"

        headers = {
            'KeyId': api_key_cn,
            'Accept': 'application/json',
            'SAP-language': 'EN' #DE
        }

        response = requests.get(ordernumberinfosurl, headers=headers, verify=False)
        data_dict = response.json()
        
        material = data_dict['d']['results'][0]['Material']

        materials.append(material)

    uniquemateriallist = list(set(materials))

    #Das hier aktivieren, wenn die restliche Funktion debugged:

    # (2.3) Die Ergebnisse aus SAP in der DB speichern

    try:
        for materialnumber in uniquemateriallist:
            material = Machine_material(materialnumber=materialnumber, machineworkcenter=workcenter)
            db.session.add(material)
        db.session.commit()   
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Speichern in der Datenbank: {e}")

    return uniquemateriallist


def getcurrentorderinfo(workcenter):

    # workcenter = '530133N'

    today = datetime.now()
    today_asstring = today.strftime('%Y-%m-%d')

    latestmatnrsURL = (
        f"{endpoint_cn}A_ProductionOrderOperation?"
        f"$filter=WorkCenter eq '{workcenter}' and OpActualExecutionStartDate eq datetime'{today_asstring}T00:00:00'&"
        f"$orderby=OpErlstSchedldExecStrtTme&" #ist bei Odata standardmäßig aufsteigend, falls nicht desc angegeben 
        f"$top=1"
    )

    print('\n\n\nlatestmatnrsURL:', latestmatnrsURL)

    headers = {
        'KeyId': api_key_cn,
        'Accept': 'application/json',
        'SAP-language': 'EN' #DE
    }

    response = requests.get(latestmatnrsURL, headers=headers, verify=False)

    data_dict = response.json()

    if len(data_dict['d']['results']) > 0:
        mostrecentorderinfo = {'ordernumber': data_dict['d']['results'][0]['ManufacturingOrder'], 
                               'plannedduration': data_dict['d']['results'][0]['OpPlannedProcessingDurn']}

    else:
        mostrecentorderinfo = {'ordernumber': '-', 'plannedduration': '-'}

    return mostrecentorderinfo

def timestamptoreadable(stamp):
    duration = isodate.parse_duration(stamp)
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    return f'{hours}:{minutes}:{seconds}'

def getrecentordersoverview(workcenter):

    print(workcenter)

    workcenter = '530133N'

    today = datetime.now() - timedelta(days=1)
    today_asstring = today.strftime('%Y-%m-%d')

    latestmatnrsURL = (
        f"{endpoint_cn}A_ProductionOrderOperation?"
        f"$filter=WorkCenter eq '{workcenter}' and OpActualExecutionStartDate ge datetime'{today_asstring}T00:00:00'&"
        f"$orderby=OpActualExecutionStartDate&"
        f"$top=30"
    )

    headers = {
        'KeyId': api_key_cn,
        'Accept': 'application/json',
        'SAP-language': 'EN' #DE
    }

    # print("URL, headers:", latestmatnrsURL, headers)

    response = requests.get(latestmatnrsURL, headers=headers, verify=False)

    # print("\n\n\nresponse.status_code:", response.status_code, "\nresponse.text:", response.text, "\n\n\n")

    data_dict = response.json()

    # with open('output.json', 'w') as json_file:
    #     json.dump(data_dict, json_file, indent=4)

    mostrecentordersinfo = []

    contents = data_dict['d']['results']
    for content in contents:
        beginning_raw = content['OpActualExecutionStartTime'] #Bsp.: PT20H16M08S
        beginningdate = f"2000-01-01 {beginning_raw[2:4]}:{beginning_raw[5:7]}:{beginning_raw[8:10]}"
        beginningdate_datetime = datetime.strptime(beginningdate, "%Y-%m-%d %H:%M:%S")

        ending_raw = content['OpActualExecutionEndTime'] #Bsp.: PT20H16M08S
        endingdate = f"2000-01-01 {ending_raw[2:4]}:{ending_raw[5:7]}:{ending_raw[8:10]}"
        endingdate_datetime = datetime.strptime(endingdate, "%Y-%m-%d %H:%M:%S")

        actualduration = round(((endingdate_datetime - beginningdate_datetime).total_seconds())/3600, 2)
        starttime = timestamptoreadable(content['OpActualExecutionStartTime'])
        endtime = timestamptoreadable(content['OpActualExecutionEndTime'])
        mostrecentordersinfo.append({'ordernumber': content['ManufacturingOrder'], 'plannedprocesduration': content['OpPlannedProcessingDurn'], 'actualduration': actualduration, 'quantity': content['OpTotalConfirmedYieldQty'], 'starttime': starttime, 'endtime': endtime})

    print('mostrecentordersinfo:', mostrecentordersinfo)

    return mostrecentordersinfo


def gettodaysoutput(workcenter):

    # print(workcenter)

    todaysdate = datetime.now()
    todaysdate_asstring = todaysdate.strftime('%Y-%m-%d')

    todaysmatnrsURL = (
        f"{endpoint_cn}A_ProductionOrderOperation?"
        f"$filter=WorkCenter eq '{workcenter}' and OpActualExecutionStartDate ge datetime'{todaysdate_asstring}T00:00:00'" 
        # f"&$top=50" 
    )

    headers = {
        'KeyId': api_key_cn,
        'Accept': 'application/json',
        'SAP-language': 'EN' #DE
    }

    # print("URL, headers:", todaysmatnrsURL, headers)

    response = requests.get(todaysmatnrsURL, headers=headers, verify=False)

    # print("\n\n\nresponse.status_code:", response.status_code, "\nresponse.text:", response.text, "\n\n\n")

    data_dict = response.json()

    # with open('output.json', 'w') as json_file:
    #     json.dump(data_dict, json_file, indent=4)

    contents = data_dict['d']['results']
    amount = 0
    for content in contents:
        amount += int(content['OpTotalConfirmedYieldQty'])

    todaysoutput = amount
    return todaysoutput


