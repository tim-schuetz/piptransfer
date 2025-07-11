import pandas as pd
from .models import *

def updatedefectstableone(month):

    Defectstableone.query.filter(Defectstableone.month == month).delete()
    db.session.commit()

    pathforsanyuencr = r"C:\Users\CUI1LO\Documents\A_neu_moeicoperformanceanalysis\inputfilespace\NCR.xlsx"
    try:
        df_raw = pd.read_excel(pathforsanyuencr)
    except Exception as e:
        print(f"Fehler beim Einlesen der Excel: {e}")
        return

    df = pd.DataFrame({
        'notificationtype': df_raw['Notification type'],
        'vendorname': df_raw['Vendor name'],
        'amount': df_raw['Ref. quantity'],
        'description': df_raw['Description'],
        'matnr': df_raw['Material']
    })

    for index, row in df.iterrows():

        material = row['matnr']

        if str(row['notificationtype']) == 'YM':
            origin = 'Internal scrap'
        elif row['notificationtype'] == 'Y2' and str(row['vendorname']).startswith('Bosch'):
            origin = 'P2P'
        elif row['notificationtype'] == 'Y2' and not str(row['vendorname']).startswith('Bosch'):
            origin = 'PP'
        else:
            origin = 'others'

        amount = row['amount']

        issue = row['description']

        if str(row['vendorname']).startswith('Bosch') and str(row['description']).startswith('CAST'):
            supplier = 'LoP3'
        elif str(row['vendorname']).startswith('Bosch') and not str(row['description']).startswith('CAST'):
            supplier = 'LoP1'
        else:
            supplier = str(row['vendorname']) if str(row['vendorname']) != "nan" else "not defined"
        print("row['vendorname']:", row['vendorname'], "   supplier:", supplier)

        casting = True if str(row['description']).startswith('CAST') else False

        entry = Defectstableone(material=material, origin=origin, amount=amount, issue=issue, supplier=supplier, iscasting=casting, month=month)
        db.session.add(entry)
    
    db.session.commit()


def updatedefectstabletwo(month):

    Defectstabletwo.query.filter(Defectstabletwo.month == month).delete()
    db.session.commit()

    try:
        pathforinternalfailurecost = r"C:\Users\CUI1LO\Documents\A_neu_moeicoperformanceanalysis\inputfilespace\IFC.xlsx"
        df2_raw = pd.read_excel(pathforinternalfailurecost)
    except Exception as e:
        print(f'Fehler beim Einlsen der Excel: {e}')
        return

    df2 = pd.DataFrame({
        'date': df2_raw['日期'],
        'product': df2_raw['产品'],
        'method_reason': df2_raw['失效模式'],
        'cost': df2_raw['物料总价\n(RMB)'],
        'material': df2_raw['物料号']
    })

    print("df2:", df2)

    for index, row in df2.iterrows():

        if pd.notna(row['date']):
            try:
                date = row['date'].date().isoformat()
            except:
                date = None
        else:
            date = None

        product = str(row['product']) if pd.notna(row['product']) else None
        material = str(row['material']) if pd.notna(row['material']) else None

        method_reason = str(row['method_reason']) if pd.notna(row['method_reason']) else ''
        method = method_reason.split('-')[0].strip()
        issue = method_reason.split('-')[1].strip() if '-' in method_reason else 'not defined'

        cost = float(row['cost']) if pd.notna(row['cost']) else 0.0

        # date = str(row['date'].date()) if not pd.notna(row['date']) else None
        # product = row['product']
        # material = row['material']
        # method = str(row['method_reason']).split('-')[0]
        # issue = str(row['method_reason']).split('-')[1] if len(str(row['method_reason']).split('-')) > 1 else 'not defined'
        # cost = row['cost']

        entry = Defectstabletwo(date=date, product=product, material=material, method=method, issue=issue, cost=cost, month=month)
        db.session.add(entry)
    
    db.session.commit()


# def updatehistoric_mostfrequentscrapissuecauses(month):

#     df = pd.DataFrame()
#     results = Defectstabletwo.query.all()
#     for index, result in enumerate(results):
#         df.at[index, 'date'] = result.date
#         df.at[index, 'product'] = result.product
#         df.at[index, 'material'] = result.material
#         df.at[index, 'method'] = result.method
#         df.at[index, 'issue'] = result.issue
#         df.at[index, 'cost'] = result.cost

#     df = df.groupby(['issue']).agg({
#         'cost': 'sum'
#     }).sort_values(by='cost', ascending=False)

#     df.reset_index(inplace=True)

#     month = month
#     mostfrequenttissue = df.at[0, 'issue']
#     mostfrequenttissue_cost = df.at[0, 'cost']
#     secondmostfrequenttissue = df.at[1, 'issue']
#     secondmostfrequenttissue_cost = df.at[1, 'cost']
#     thirdmostfrequenttissue = df.at[2, 'issue']
#     thirdmostfrequenttissue_cost = df.at[2, 'cost']

#     newEntry = Mostfrequentscrapissuecauses(mostfrequenttissue=mostfrequenttissue, mostfrequenttissue_cost=mostfrequenttissue_cost, secondmostfrequenttissue=secondmostfrequenttissue, secondmostfrequenttissue_cost=secondmostfrequenttissue_cost, thirdmostfrequenttissue=thirdmostfrequenttissue, thirdmostfrequenttissue_cost=thirdmostfrequenttissue_cost)
#     db.session.add(newEntry)
#     db.session.commit()


# def updatehistoric_worstmethodsforspoolscrap():

#     df = pd.DataFrame()
#     results = Defectstabletwo.query.all()
#     for index, result in enumerate(results):
#         df.at[index, 'date'] = result.date
#         df.at[index, 'product'] = result.product
#         df.at[index, 'material'] = result.material
#         df.at[index, 'method'] = result.method
#         df.at[index, 'issue'] = result.issue
#         df.at[index, 'cost'] = result.cost

#     df = df[df['product'].str.lower().str.contains('spool', na=False)]

#     df = df.groupby(['method']).agg({
#         'cost': 'sum'
#     })

#     df.reset_index(inplace=True)

#     month = month
#     try:
#         costofassembly = df[df['method'].str.lower() == 'assembly']['cost'].values[0]
#     except:
#         costofassembly = 0
#     try:
#         costofgrinding = df[df['method'].str.lower() == 'grinding']['cost'].values[0]
#     except:
#         costofgrinding = 0
#     try:
#         costofturning = df[df['method'].str.lower() == 'turning']['cost'].values[0]
#     except:
#         costofturning = 0

#     newEntry = Worstmethodsforspoolscrap(month=month, costofassembly=costofassembly, costofgrinding=costofgrinding, costofturning=costofturning)

