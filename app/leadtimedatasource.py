import pandas as pd
from datetime import datetime, time
from app.models import *
import math
import mysql.connector

def updatekanbandatabase():

    Leadtimetable.query.delete()
    db.session.commit()

    # kanban_df = pd.read_excel("kanban_sample.xlsx")

    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="WujP_mockup"
    )

    query = "SELECT * FROM SAP_ICO_KANBAN_Data LIMIT 100"

    kanban_df = pd.read_sql(query, conn)

    conn.close()

    for i in range(len(kanban_df)):
        if kanban_df.at[i, 'Status'] == 2:
            order = kanban_df.at[i, 'Order_']
            endtag = str(kanban_df.at[i, 'Created']).split(' ')[0]
            endzeit = str(kanban_df.at[i, 'Time'])            
            enddatum = endtag + '-' + endzeit
            enddatum = datetime.strptime(enddatum, '%Y-%m-%d-%H:%M:%S')

            indexoffoundrow = None
            valuefound = False
            for j in range(i, min(i+200, len(kanban_df))): #Startet bei der aktuellen Zeile wo die Auftragsnummer gefunden und geht dann bis zu 100 weiter runter, um die gleiche Auftragsnummer erneut zu finden. Aber nicht weiter runter als die Gesamtlänge des df (denn min() wählt immer den kleineren Wert)
                orderfound = kanban_df.at[j, 'Order']
                # print('order:', order, 'orderfound:', orderfound)
                durchlaufzeit_in_stunden = None #Damit es nicht zu einem Fehler kommt, falls die Auftragsnummer kein zweites mal gefunden wird
                if order == orderfound and kanban_df.at[j, 'Kanban status'] == 5:
                    anfangstag = str(kanban_df.at[j, 'Date']).split(' ')[0]
                    anfangszeit = str(kanban_df.at[j, 'Time'])            
                    anfangsdatum = anfangstag + '-' + anfangszeit
                    anfangsdatum = datetime.strptime(anfangsdatum, '%Y-%m-%d-%H:%M:%S')
                    durchlaufzeit = enddatum - anfangsdatum
                    durchlaufzeit_in_stunden = durchlaufzeit.total_seconds()/3600
                    indexoffoundrow = j
                    # print(f'Orderfound ({orderfound}) matches order ({order})')
                    valuefound = True
                    break
            if valuefound == False: #Falls nach unten hin nicht gefunden, dann noch die darüberliegenden Zeilen überprüfen
                for j in range(i, max(i-200, -1), -1): #Startet bei der aktuellen Zeile wo die Auftragsnummer gefunden und geht dann bis zu 100 weiter runter, um die gleiche Auftragsnummer erneut zu finden. Aber nicht weiter runter als die Gesamtlänge des df (denn min() wählt immer den kleineren Wert)
                    orderfound = kanban_df.at[j, 'Order']
                    # print('order:', order, 'orderfound:', orderfound)
                    durchlaufzeit_in_stunden = None #Damit es nicht zu einem Fehler kommt, falls die Auftragsnummer kein zweites mal gefunden wird
                    if order == orderfound and kanban_df.at[j, 'Kanban status'] == 5:
                        anfangstag = str(kanban_df.at[j, 'Date']).split(' ')[0]
                        anfangszeit = str(kanban_df.at[j, 'Time'])            
                        anfangsdatum = anfangstag + '-' + anfangszeit
                        anfangsdatum = datetime.strptime(anfangsdatum, '%Y-%m-%d-%H:%M:%S')
                        durchlaufzeit = enddatum - anfangsdatum
                        durchlaufzeit_in_stunden = durchlaufzeit.total_seconds()/3600
                        indexoffoundrow = j
                        # print(f'Orderfound ({orderfound}) matches order ({order})')
                        valuefound = True
                        break

                #Problem mit den Daten aus SAP: ist zwar nach Datum aufsteigend sortiert, aber nicht nach Uherzeit. Die sind bunt durcheinander.
                #Deshalb als Lösung: In beide Richtungen nach der Ordernumber (also foundorder) suchen und von der Differenzzeit immer den Betrag nehmen.
                # Am Ende nochmal gut prüfen! 
                
            if durchlaufzeit_in_stunden is not None:
                kanban_df.at[i, 'leadtime [in h]'] = abs(durchlaufzeit_in_stunden) #abs macht Zahl zu absoluter Zahl, also immer nur positive Zahlen
                if indexoffoundrow:
                    kanban_df.at[indexoffoundrow, 'leadtime [in h]'] = abs(durchlaufzeit_in_stunden)

    for i in reversed(range(len(kanban_df))):
        if pd.isna(kanban_df.at[i, 'leadtime [in h]']) and kanban_df.at[i, 'Kanban status'] == 2:
            kanban_df.drop(i, inplace=True)
        elif pd.isna(kanban_df.at[i, 'leadtime [in h]']) and kanban_df.at[i, 'Kanban status'] == 5:
            kanban_df.at[i, 'activationstatus'] = 'active'
        else:
            kanban_df.at[i, 'activationstatus'] = 'closed'

    cleaned_df = pd.DataFrame({
        'Material': kanban_df['Material'],
        'Kanbanidnumber': kanban_df['ID number'],
        'Created': kanban_df['Created'],
        'Time': kanban_df['Time'],
        'Number': kanban_df['No.'],
        'Kanbanstatus': kanban_df['Kanban status'],
        'Order': kanban_df['Order'],
        'Cntcycle': kanban_df['CntCycle'],
        'Leadtimeinh': kanban_df['leadtime [in h]'],
        'Activationstatus': kanban_df['activationstatus']
    })

    for index, row in cleaned_df.iterrows():
    
        created = row['Created']
        if isinstance(created, pd.Timestamp):
            created = created.to_pydatetime()

        time_val = row['Time']
        if isinstance(time_val, time):
            time_val = time_val.strftime('%H:%M:%S')

        leadtime = row['Leadtimeinh']
        if isinstance(leadtime, float) and math.isnan(leadtime):
            leadtime = None

        creationmonthasint = extractmonthasnumberfromdate(row['Created'])

        entry = Leadtimetable(
            material=row['Material'],
            kanbanidnumber=row['Kanbanidnumber'],
            created=created,
            creationmonthasint = creationmonthasint,
            time=time_val,
            number=row['Number'],
            kanbanstatus=row['Kanbanstatus'],
            order=row['Order'],
            cntcycle=row['Cntcycle'],
            leadtimeinh=leadtime,
            activationstatus=row['Activationstatus']
        )
        db.session.add(entry)

        if index % 500 == 0:
            db.session.commit()

    db.session.commit()

    #Nachträglich noch die Zeiten von Beginn des Monats an bestimmen: 

    results = (
        db.session.query(
            Leadtimetable.created,
            Leadtimetable.time
        ).all()
    )

    dates = [result.created for result in results]
    times = [result.time for result in results]

    hourssincemonthbeginning = []

    for i in range(len(dates)):
        date = dates[i]
        monthasint = int(date[6:7])
        time_ = times[i]
        timestamp = pd.to_datetime(str(date).split(' ')[0] + ' ' + str(time_))
        firstdayofmonthtimestamp = pd.to_datetime('2025-' + str(monthasint) + '-01')
        timedifference = timestamp - firstdayofmonthtimestamp
        timedifferenceinhours = int(timedifference.total_seconds() / 3600)
        hourssincemonthbeginning.append(timedifferenceinhours)

    entries = Leadtimetable.query.all()

    for index, entry in enumerate(entries):
        entry.hourssincemonthbeginning = hourssincemonthbeginning[index]

    db.session.commit()

    # Nachträglich noch den Monat als Integer in die Datenbank einfügen




def extractmonthasnumberfromdate(created):
    monthasnumber_raw = str(created).split('-')[1]
    if monthasnumber_raw.startswith('0'):
        monthasint = int(monthasnumber_raw[1])
    else:
        monthasint = int(monthasnumber_raw)
    return monthasint


