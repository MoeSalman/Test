import os
import json
import pandas as pd
import pyodbc
from pathlib import Path

def query_db(query,one=False):
    r = [dict(zip(cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    return (r[0] if r else None) if one else r

## Spécifier le chemin pour les deux documents

try:
    path_1 = 'C:\\Users\\User\\Desktop\\Files\\CapgeminiTest\\data'
    filename_L = os.path.join(path_1,'lieux.csv')
    path_2 = 'C:\\Users\\User\\Desktop\\Files\\CapgeminiTest\\data'
    filename_P = os.path.join(path_2,'People.csv')
    

except IOError:
    print('The file doesnt exist')

## Configuration de la connexion à la base de données SQL

else:
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-J8LJ1M3\WEBSITETESTING;'
                      'Database=test;'
                      'Trusted_Connection=yes;')
    df_1 = pd.read_csv(filename_L)
    cursor = conn.cursor()
    
##  Insertion du premier fichier Lieux dans la base de données SQL

    for row in df_1.itertuples():
        cursor.execute('''
                INSERT INTO Lieux (Commune,Departement,region)
                VALUES (?,?,?)
                ''',
                row.commune, 
                row.departement,
                row.region
                )
    print("done")    
    conn.commit()

##  Insertion du deuxieme fichier people dans la base de données SQL    

    cursor = conn.cursor()
    df_2 = pd.read_csv(filename_P)

    for row_2 in df_2.itertuples():
        cursor.execute('''
                INSERT INTO People (prenom,nom,DATE_DE_NAISSANCE,CommuneID)
                VALUES (?,?,?,?)
                ''',
                row_2.prenom, 
                row_2.nom,
                row_2.datenaissance,
                row_2.commune
                )
    print("done") 
    conn.commit()


##  Changement du nom de la commune par l'ID    

    Update_communeID= """ update p
    set p.CommuneID=l.ID
    from People p inner join Lieux l
    on p.CommuneID=l.Commune"""
    cursor.execute(Update_communeID)
    print("done") 
    conn.commit()
    

##  Requêtes SQL pour les personnes nées et les résultats sont sauvegardés dans deux documents différents avec un chemin précis
 
    select_par_departement = """SELECT  L.Departement,COUNT(P.ID) AS NOMBRE_DE_NEES FROM People P JOIN Lieux L ON P.CommuneID=L.ID GROUP BY L.Departement"""
    select_par_region = """SELECT  L.region,COUNT(P.ID) AS NOMBRE_DE_NEES FROM People P JOIN Lieux L ON P.CommuneID=L.ID GROUP BY L.region"""
    
    cursor.execute(select_par_departement)
    result_1 = cursor.fetchall()
    result_1= dict(result_1)
    print(result_1)

    base = Path('C:\\Users\\User\\Desktop\\Files\\CapgeminiTest\\Test')
    jsonpath = base / ("ParDepartement.json")
    base.mkdir(exist_ok=True)
    jsonpath.write_text(json.dumps(result_1))

    
   
    cursor.execute(select_par_region)
    result_2 = cursor.fetchall()
    result_2= dict(result_2)
    print(result_2)
    
    base = Path('C:\\Users\\User\\Desktop\\Files\\CapgeminiTest\\Test')
    jsonpath = base / ("ParRegion.json")
    base.mkdir(exist_ok=True)
    jsonpath.write_text(json.dumps(result_2))
    cursor.connection.close()
    
