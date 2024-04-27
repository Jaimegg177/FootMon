from tkinter import Tk, Button
import pandas as pd
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['deportes_db']

def populate_db():
    
    results = db['partidos_partido']
    goalscorers = db['partidos_goleadores']
    shootouts = db['partidos_penaltis']

    # Insertar resultados
    data_results = pd.read_csv('data/results.csv')
    data_goalscorers = pd.read_csv('data/goalscorers.csv')
    data_shootouts = pd.read_csv('data/shootouts.csv')

    # Convierte los datos a un formato compatible con MongoDB
    data_results_json = data_results.to_dict(orient='records')
    data_goalscorers_json = data_goalscorers.to_dict(orient='records')
    data_shootouts_json = data_shootouts.to_dict(orient='records')

    # Inserta los datos en la colección de MongoDB
    results.insert_many(data_results_json)
    goalscorers.insert_many(data_goalscorers_json)
    shootouts.insert_many(data_shootouts_json)

    print("Datos insertados en la base de datos")

def drop_db():
    client.drop_database('deportes_db')

    print("Base de datos eliminada")
    
def partidos_equipo_año_torneo():
    # Función de map
    map_function = """
    function() {
        if (this.tournament == 'FIFA World Cup') {
            var year = this.date.split('-')[0];
            emit({year: year, tournament: this.tournament, team: this.home_team}, 1);
            emit({year: year, tournament: this.tournament, team: this.away_team}, 1);
        }
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return Array.sum(values);
    }
    """
    resultado = db.command('mapReduce', 'results', map=map_function, reduce=reduce_function, out='partidos_por_equipo_por_año_en_torneo')

    sorted_result = list(db.partidos_por_equipo_por_año_en_torneo.find().sort([('year', -1)]))

    print("\nResultados de partidos por equipo por año en torneo: ")
    for doc in sorted_result:
        print(doc)


def goles_en_propia_reibidos_por_equipo():
    # Función de map
    map_function = """
    function() {
        if (this.own_goal == true) {
            emit({team: this.team}, 1);
        }
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return Array.sum(values);
    }
    """

    resultado = db.command('mapReduce', 'goalscorers', map=map_function, reduce=reduce_function, out='goles_en_propia')

    sorted_result = list(db.goles_en_propia.find().sort([('value', -1)]))

    print("\n Goles en propia meta por equipo: ")
    for doc in sorted_result:
        print(doc)

def goles_por_equipo_en_torneo():
     # Función de map
    map_function = """
    function() {
        emit({tournament: this.tournament, team: this.home_team}, this.home_score);
        emit({tournament: this.tournament, team: this.away_team}, this.away_score);
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return Array.sum(values);
    }
    """

    # Ejecutar MapReduce
    resultado = db.command('mapReduce', 'results', map=map_function, reduce=reduce_function, out='goles_por_equipo_torneo')

    sorted_result = list(db.goles_por_equipo_torneo.find().sort([('value', -1)]))

    print("\nGoles por equipo y torneo:")
    for doc in sorted_result:
        print(doc)

def primer_tiro_penaltis():
    map_function = """
    function() {
        emit({team: this.first_shooter}, 1);
    }
    """

    # Función de reduce para calcular número de veces que cada equipo ha chutado primero en tanda de penaltis
    reduce_function = """
    function(key, values) {
        return Array.sum(values);
    }
    """

    # Ejecutar MapReduce para calcular número de veces que cada equipo ha chutado primero en tanda de penaltis
    resultado = db.command('mapReduce', 'shootouts', map=map_function, reduce=reduce_function, out='chutes_primero_en_penaltis')
    sorted_result = list(db.chutes_primero_en_penaltis.find().sort([('value', -1)]))

    print("\nChutes primero en tanda de penaltis:")
    for doc in sorted_result:
        print(doc)

def start():
    top=Tk()
    B = Button(top, text ="Popular BD", command=populate_db)
    B.pack()
    
    B2 = Button(top, text ="Eliminar BD", command=drop_db)
    B2.pack()

    B3 = Button(top, text ="Partidos de cada equipo en un año en competicion", command=partidos_equipo_año_torneo)
    B3.pack()

    B4 = Button(top, text ="Goles en propia recibidos por cada equipo", command=goles_en_propia_reibidos_por_equipo)
    B4.pack()

    B5 = Button(top, text ="Goles por equipo y torneo", command=goles_por_equipo_en_torneo)
    B5.pack()

    B6 = Button(top, text ="Primer tiro en penaltis", command=primer_tiro_penaltis)
    B6.pack()
       
    top.mainloop()


if __name__ == '__main__':
    start()