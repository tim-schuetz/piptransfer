from flask import Blueprint, request, jsonify
from app.models import *
from ..qualitydatasource import *
from datetime import datetime
from sqlalchemy import func, desc

quality_bp = Blueprint('quality', __name__)

# testingendpoints:

@quality_bp.route("/clearalldatabaseentries")
def clearalldatabaseentries():
    Defectstableone.query.delete()
    Defectstabletwo.query.delete()
    db.session.commit()
    return "Alle Einträge gelöscht"

@quality_bp.route("/updatedefectstableone")
def reroute_updatedefectstableone():
    updatedefectstableone('jan')
    return "successfully updated NCR table"

@quality_bp.route("/exposedatabase")
def exposedatabase():
    allentries_Defectstableone = Defectstableone.query.all()
    allentries_Defectstabletwo = Defectstabletwo.query.all()

    entriestableone = []
    for entry in allentries_Defectstableone:
            entriestableone.append({"entry:": entry.id, "material:": entry.material, "origin:": entry.origin, "amount:": entry.amount, "issue:": entry.issue, "supplier:": entry.supplier, "iscasting:": entry.iscasting, "month:": entry.month})

    entriestabletwo = []
    for entry in allentries_Defectstabletwo:
        entriestabletwo.append({
            "id": entry.id,
            "date": entry.date,
            "product": entry.product,
            "material": entry.material,
            "method": entry.method,
            "issue": entry.issue,
            "cost": entry.cost,
            "month": entry.month
        })

    return jsonify({"entriestableone": entriestableone, "entriestabletwo": entriestabletwo})


#Production endpoints:

@quality_bp.route('/removedataformonth', methods=['POST'])
def removedataformonth():
    data = request.json 
    month = data.get('month')

    try:
        Defectstableone.query.filter(Defectstableone.month == month).delete()
        Defectstabletwo.query.filter(Defectstabletwo.month == month).delete()
        db.session.commit()
        return jsonify({"answer": "successful"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@quality_bp.route('/readnewdatafromsource', methods=['POST'])
def readnewdatafromsource():
    data = request.get_json()
    month = data.get('month')
    updatedefectstableone(month)
    updatedefectstabletwo(month)
    return jsonify({'status': 'successful'})

@quality_bp.route('/getncrorigins', methods=['POST']) #1
def getncrorigins():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter')

    query = (
        db.session.query(
            func.sum(Defectstableone.amount).label('amountperorigin'),
            Defectstableone.origin
        )
        .filter(Defectstableone.month.ilike('%'+month+'%'))
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstableone.material.in_(matnrstofilter))

    query = query.group_by(Defectstableone.origin)

    results = query.all()

    response = [{'origin': result.origin, 'amount': result.amountperorigin} for result in results]

    return jsonify({'elements': response})


@quality_bp.route('/getsupplierofcastings', methods=['POST']) # 5
def getsupplierofcastings():
    
    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter')

    query = (
        db.session.query(
            func.sum(Defectstableone.amount).label('amountpersupplier'),
            Defectstableone.supplier
        )
        .filter(
            Defectstableone.iscasting == True,
            Defectstableone.origin.in_(['PP']),
            Defectstableone.month.ilike('%'+month+'%')
        )
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstableone.material.in_(matnrstofilter))

    query = query.group_by(Defectstableone.supplier)

    results = query.all()

    response = [{ 'supplier': result.supplier, 'amount': result.amountpersupplier } for result in results]

    # df = pd.DataFrame()
    # results = Defectstableone.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'amount'] = result.amount
    #     df.at[index, 'issue'] = result.issue
    #     df.at[index, 'supplier'] = result.supplier
    #     df.at[index, 'iscasting'] = result.iscasting

    # df = df[df['iscasting'] == True] 

    # df = df[~df['supplier'].fillna('').str.lower().isin(['lop1', 'lop3'])] 

    # if len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]

    # df = df.groupby('supplier').agg({
    #     'amount': 'sum'
    # })

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'supplier': row['supplier'], 'amount':row['amount']})

    return jsonify({'elements': response})


@quality_bp.route('/getsupplierofnonecastings', methods=['POST']) # 6
def getsupplierofnonecastings():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter')

    query = (
        db.session.query(
            func.sum(Defectstableone.amount).label('amountpersupplier'),
            Defectstableone.supplier,
            Defectstableone.month
        )
        .filter(Defectstableone.month.ilike('%' + month + '%'))
        .filter(Defectstableone.iscasting == False)
        .filter(Defectstableone.origin.in_(['PP']))
    ) 

    # query2 = (
    #     db.session.query(
    #         Defectstableone.material,
    #         Defectstableone.origin,
    #         Defectstableone.amount,
    #         Defectstableone.issue,
    #         Defectstableone.supplier,
    #         Defectstableone.iscasting
    #     )
    #     .filter(Defectstableone.iscasting == False)
    #     .filter(Defectstableone.origin.in_(['PP']))
    # )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstableone.material.in_(matnrstofilter))

    query = query.group_by(Defectstableone.supplier)

    results = query.all()

    response = [{'supplier': result.supplier, 'amount': result.amountpersupplier, 'month': result.month} for result in results]

    # printresult = query2.all()
    # printresponse = [{"material:": pr.material, "origin:": pr.origin, "amount:": pr.amount, "issue:": pr.issue, "supplier:": pr.supplier, "iscasting": pr.iscasting} for pr in printresult]
    # for row in printresponse:


    # df = pd.DataFrame()
    # results = Defectstableone.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'amount'] = result.amount
    #     df.at[index, 'issue'] = result.issue
    #     df.at[index, 'supplier'] = result.supplier
    #     df.at[index, 'iscasting'] = result.iscasting

    # df = df[df['iscasting'] == False] 
    # df = df[~df['supplier'].fillna('').str.lower().isin(['lop1', 'lop3'])] 

    # if len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]

    # df = df.groupby('supplier').agg({
    #     'amount': 'sum'
    # })

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'supplier': row['supplier'], 'amount':row['amount']})

    return jsonify({'elements': response})


@quality_bp.route('/getsuppliersinternal', methods=['POST']) # 7
def getsuppliersinternal():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter')

    query = (
        db.session.query(
            Defectstableone.material,
            func.sum(Defectstableone.amount).label('amountpersupplier'),
            Defectstableone.supplier,
        )
        .filter(
            Defectstableone.month.ilike('%' + month + '%'),
            # Defectstableone.supplier.in_(['lop1', 'lop3'])
            func.lower(Defectstableone.supplier).in_(['lop1', 'lop3'])
        )
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstableone.material.in_(matnrstofilter))

    query = query.group_by(Defectstableone.supplier)

    results = query.all()

    response = [{'supplier': result.supplier, 'amount': result.amountpersupplier} for result in results]

    # df = pd.DataFrame()
    # results = Defectstableone.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'amount'] = result.amount
    #     df.at[index, 'supplier'] = result.supplier

    # df = df[df['supplier'].str.lower().fillna('').isin(['lop1', 'lop3'])] 

    # if matnrstofilter and len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]

    # df = df.groupby('supplier').agg({
    #     'amount': 'sum'
    # })

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'supplier': row['supplier'], 'amount':row['amount']})

    return jsonify({'elements': response})

@quality_bp.route('/getscrapissueorigins', methods=['POST']) # 2
def getscrapissueorigins():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter', [])

    query = (
        db.session.query(
            Defectstabletwo.product.label('product'),
            Defectstabletwo.issue.label('issue'),
            func.sum(Defectstabletwo.cost).label('amount')
        )
        .filter(Defectstabletwo.month.ilike('%' + month + '%'))
    )

    if matnrstofilter:
        query = query.filter(Defectstabletwo.material.in_(matnrstofilter))

    query = query.group_by(Defectstabletwo.product, Defectstabletwo.issue)

    results = query.all()

    # 4. Direkt ins gewünschte JSON-Format bringen
    response = [{'material': result.product, 'issue': result.issue, 'amount': result.amount} for result in results]

    #Den Teil hier beibehalten um die Zeit zu stoppen für die T2000

    # df = pd.DataFrame()
    # results = Defectstabletwo.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'date'] = result.date
    #     df.at[index, 'product'] = result.product
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'method'] = result.method
    #     df.at[index, 'issue'] = result.issue
    #     df.at[index, 'cost'] = result.cost

    # if len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]

    # df = df.groupby(['product', 'issue']).agg({
    #     'cost': 'sum'
    # })

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'material': row['product'], 'issue':row['issue'], 'amount':row['cost']})

    return jsonify({'elements': response})


@quality_bp.route('/getspoolscrapmethods', methods=['POST']) # 3
def getspoolscrapmethods():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter')
    prodcuttofilter = data.get('prodcutstofilter') 

    if 'ng10' in (str(prodcuttofilter).lower()):
        prodcuttofilter = 'ng10'
    elif 'ng6' in (str(prodcuttofilter).lower()):
        prodcuttofilter = 'ng6'

    query = (
        db.session.query(
            Defectstabletwo.date,
            Defectstabletwo.product,
            Defectstabletwo.material,
            Defectstabletwo.method,
            func.sum(Defectstabletwo.cost).label('totalcostpermethod'),
        )
        .filter(
            Defectstabletwo.product.ilike('%spool%'),
            Defectstabletwo.month.ilike('%'+ month +'%')
        )
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstabletwo.material.in_(matnrstofilter))

    if prodcuttofilter and prodcuttofilter != 'all':
        query = query.filter(Defectstabletwo.product.ilike('%' + prodcuttofilter + '%'))


    query = query.group_by(Defectstabletwo.method)

    results = query.all()

    response = [{'method': result.method, 'cost': result.totalcostpermethod} for result in results]


    # df = pd.DataFrame()
    # results = Defectstabletwo.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'date'] = result.date
    #     df.at[index, 'product'] = result.product
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'method'] = result.method
    #     df.at[index, 'issue'] = result.issue
    #     df.at[index, 'cost'] = result.cost

    # print(1)

    # df = df[df['product'].str.lower().str.contains('spool', na=False)]

    # if len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]

    # if prodcuttofilter and prodcuttofilter != 'all':
    #     df = df[df['product'].str.lower().str.contains((prodcuttofilter), na=False)]

    # print(2)

    # if mindate:
    #     #Hier rumprobieren, dass nur die Daten größer mindate rauskriegen 
    #     ...
    # if maxdate:
    #     #Hier rumprobieren, dass nur die Daten kleiner maxdate rauskriegen 
    #     ...

    # df = df.groupby(['method']).agg({
    #     'cost': 'sum'
    # })

    # print(3)

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'method': row['method'], 'cost': row['cost']})

    # print('elements:', data)

    return jsonify({'elements': response})


@quality_bp.route('/getspoolscrapreason', methods=['POST'])
def getspoolscrapreason():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter', [])
    prodcuttofilter = data.get('prodcutstofilter', []) 

    print("month:", month, "prodcuttofilter:", prodcuttofilter, "matnrstofilter", matnrstofilter)

    if 'ng10' in (str(prodcuttofilter).lower()):
        prodcuttofilter = 'NG10 Spool'
    elif 'ng6' in (str(prodcuttofilter).lower()):
        prodcuttofilter = 'NG6 Spool'


    #Debugging:
    # querysimplified = (
    #     db.session.query(
    #         func.sum(Defectstabletwo.cost).label('totalcostperissue'),
    #         Defectstabletwo.product,
    #         Defectstabletwo.issue
    #     )
    # )

    # querysimplified = querysimplified.group_by(Defectstabletwo.issue)

    # results_simplified = querysimplified.all()

    # response_simplified = [{'totalcostperissue': r.totalcostperissue, 'product:': r.product, 'issue:': r.issue} for r in results_simplified]

    # print("response_simplified:", response_simplified)


    query = (
        db.session.query(
            Defectstabletwo.date,
            Defectstabletwo.product,
            Defectstabletwo.material,
            Defectstabletwo.issue,
            func.sum(Defectstabletwo.cost).label('totalcostperissue'),
        )
        .filter(
            Defectstabletwo.product.ilike('%spool%'), #like ist Vergleich, ob mit spool übereinstimmt. ilike ist case-insensitive, also Spool, SPOOL etc. funktionieren alle. Durch die % wildcards wird nicht auf genaue Übereinstimmung geprüft, sondern nur, ob spool enthalten ist
            Defectstabletwo.month.ilike('%'+ month +'%')
        )
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstabletwo.material.in_(matnrstofilter))

    if prodcuttofilter and len(prodcuttofilter) > 0 and prodcuttofilter != 'all' :
        query = query.filter(Defectstabletwo.product.in_([prodcuttofilter]))

    query = query.group_by(Defectstabletwo.issue)

    results = query.all()

    response = [{'issue': result.issue, 'cost': result.totalcostperissue} for result in results]

    # df = pd.DataFrame()
    # results = Defectstabletwo.query.all()
    # for index, result in enumerate(results):
    #     df.at[index, 'date'] = result.date
    #     df.at[index, 'product'] = result.product
    #     df.at[index, 'material'] = result.material
    #     df.at[index, 'issue'] = result.issue
    #     df.at[index, 'cost'] = result.cost

    # df = df[df['product'].str.lower().str.contains('spool', na=False)]

    # if matnrstofilter and len(matnrstofilter) > 0:
    #     df = df[df['material'].isin(matnrstofilter)]
    
    # if prodcuttofilter and len(prodcuttofilter) > 0:
    #     df = df[df['product'].str.lower().str.contains((prodcuttofilter), na=False)]

    # df = df.groupby(['issue']).agg({
    #     'cost': 'sum'
    # })

    # df.reset_index(inplace=True)

    # data = []

    # for index, row in df.iterrows():
    #     data.append({'issue': row['issue'], 'cost': row['cost']})


    return jsonify({'elements': response})


@quality_bp.route('/getproductlistforspoolscrap')
def getproductlistforspoolscrap():

    df = pd.DataFrame()
    results = Defectstabletwo.query.all()
    for index, result in enumerate(results):
        df.at[index, 'date'] = result.date
        df.at[index, 'product'] = result.product

    df = df[df['product'].str.lower().str.contains('spool', na=False)]

    products = df['product'].tolist()
    uniqueproductlist = list(set(products))

    return jsonify({'uniqueproductlist': uniqueproductlist})


@quality_bp.route('/showdatabank')
def showdatabank():

    results = Defectstabletwo.query.all()

    response = [{'method': result.method, 'cost': result.cost} for result in results]

    return jsonify({'response': response})



@quality_bp.route('/gethistoric_Worstmethodsforspoolscrap', methods=['POST'])
def gethistoric_Worstmethodsforspoolscrap():
    data = request.get_json()
    month = data.get('month')

    monthsoftheyear = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    index_month = monthsoftheyear.index(month)
    index_previousmonth = index_month - 1 if index_month > 0 else 11
    previousmonth = monthsoftheyear[index_previousmonth]

    query = (
        db.session.query(
            Defectstabletwo.method,
            func.sum(Defectstabletwo.cost).label('costbymethod')
        )
        .filter(
            Defectstabletwo.product.ilike('%spool%'),
            Defectstabletwo.month.ilike('%'+month+'%')
        )
        .group_by(Defectstabletwo.method)
        .order_by(func.sum(Defectstabletwo.cost))
    )

    results = query.all()

    response_thismonth = [{'method': result.method, 'cost': result.costbymethod} for result in results]
    response_thismonth_dict = [{'method': response['method'], 'cost': response['cost']} for response in response_thismonth]

    query = (
        db.session.query(
            Defectstabletwo.method,
            func.sum(Defectstabletwo.cost).label('costbymethod')
        )
        .filter(
            Defectstabletwo.product.ilike('%spool%'),
            Defectstabletwo.month.ilike('%'+previousmonth+'%')
        )
        .group_by(Defectstabletwo.method)
        .order_by(func.sum(Defectstabletwo.cost))
    )

    results = query.all()

    response_previousmonth = [{'method': result.method, 'cost': result.costbymethod} for result in results]
    response_previousmonth_dict = {entry['method']: entry['cost'] for entry in response_previousmonth}

    methodcostmonhtlycomparison = []

    for element in response_thismonth_dict:
        method = element['method']
        cost = element['cost']
        costpreviousmonth = response_previousmonth_dict.get(method)

        if costpreviousmonth is not None and costpreviousmonth != 0:
            costchange = (cost - costpreviousmonth) / costpreviousmonth
        else:
            costchange = None

        methodcostmonhtlycomparison.append({'method': method, 'costchange': costchange})

    return jsonify({'methodcostmonhtlycomparison': methodcostmonhtlycomparison})


@quality_bp.route('/getmostfrequentscrapissuecauses', methods=['POST'])
def getmostfrequentscrapissuecauses():

    data = request.get_json()
    month = data.get('month')
    matnrstofilter = data.get('matnrstofilter', [])
    
    monthsoftheyear = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    index_month = monthsoftheyear.index(month)
    index_previousmonth = index_month - 1 if index_month > 0 else 11
    previousmonth = monthsoftheyear[index_previousmonth]

    query = (
        db.session.query(
            func.sum(Defectstabletwo.cost).label('costperissue'),
            Defectstabletwo.issue
        )
        .filter(Defectstabletwo.month.ilike('%'+month+'%'))
        .group_by(Defectstabletwo.issue)
        .order_by(desc('costperissue'))
    )

    if matnrstofilter and len(matnrstofilter) > 0:
        query = query.filter(Defectstabletwo.material.in_(matnrstofilter))

    results = query.all()

    costperissue_currentmonth = [{'issue': result.issue, 'cost': result.costperissue } for result in results]

    query = (
        db.session.query(
            func.sum(Defectstabletwo.cost).label('costperissue'),
            Defectstabletwo.issue
        )
        .filter(Defectstabletwo.month.ilike('%'+previousmonth+'%'))
        .group_by(Defectstabletwo.issue)
        .order_by(desc('costperissue'))
    )

    results = query.all()

    costperissue_previousmonth = [{'issue': result.issue, 'cost': result.costperissue } for result in results]

    previous_cost_dict = {entry['issue']: entry['cost'] for entry in costperissue_previousmonth}

    costchangetopreviousmonthperissue = []

    for current in costperissue_currentmonth:
        issue = current['issue']
        current_cost = current['cost']
        previous_cost = previous_cost_dict.get(issue)

        if previous_cost is not None and previous_cost != 0:
            cost_change = (current_cost - previous_cost) / previous_cost
        else:
            # Wenn kein Vergleichswert vorhanden oder 0, setze auf None oder 100% (je nach Wunsch)
            cost_change = None

        costchangetopreviousmonthperissue.append({
            'issue': issue,
            'costchange': cost_change
        })

    return jsonify({'constchangetopreviousmonthperissue': costchangetopreviousmonthperissue})



