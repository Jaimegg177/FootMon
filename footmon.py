'''
Created on 11 oct 2023

@author: anton
'''

from tkinter import Tk, Button

from pymongo import MongoClient

def bd():
    # Conexión a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['deportes_db']
    partidos = db['partidos']

    # Función de map
    map_function = """
    function() {
        var resultado;
        if (this.goles_local > this.goles_visitante) {
            resultado = {ganados: 1, empatados: 0, perdidos: 0};
        } else if (this.goles_local < this.goles_visitante) {
            resultado = {ganados: 0, empatados: 0, perdidos: 1};
        } else {
            resultado = {ganados: 0, empatados: 1, perdidos: 0};
        }
        emit(this.equipo_local, {
            goles_local: this.goles_local,
            goles_visitante: this.goles_visitante,
            partidos_jugados: 1,
            resultado: resultado,
            faltas_local: this.faltas_local,
            faltas_visitante: this.faltas_visitante,
            tarjetas_amarillas_local: this.tarjetas_amarillas_local,
            tarjetas_amarillas_visitante: this.tarjetas_amarillas_visitante,
            tarjetas_rojas_local: this.tarjetas_rojas_local,
            tarjetas_rojas_visitante: this.tarjetas_rojas_visitante,
            corners_local: this.corners_local,
            corners_visitante: this.corners_visitante,
            minutos_local: this.minutos_local,
            minutos_visitante: this.minutos_visitante
        });
        emit(this.equipo_visitante, {
            goles_local: this.goles_local,
            goles_visitante: this.goles_visitante,
            partidos_jugados: 1,
            resultado: {ganados: resultado.perdidos, empatados: resultado.empatados, perdidos: resultado.ganados},
            faltas_local: this.faltas_local,
            faltas_visitante: this.faltas_visitante,
            tarjetas_amarillas_local: this.tarjetas_amarillas_local,
            tarjetas_amarillas_visitante: this.tarjetas_amarillas_visitante,
            tarjetas_rojas_local: this.tarjetas_rojas_local,
            tarjetas_rojas_visitante: this.tarjetas_rojas_visitante,
            corners_local: this.corners_local,
            corners_visitante: this.corners_visitante,
            minutos_local: this.minutos_local,
            minutos_visitante: this.minutos_visitante
        });
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        var result = {
            goles_local: 0,
            goles_visitante: 0,
            partidos_jugados: 0,
            ganados: 0,
            empatados: 0,
            perdidos: 0,
            faltas_local: 0,
            faltas_visitante: 0,
            tarjetas_amarillas_local: 0,
            tarjetas_amarillas_visitante: 0,
            tarjetas_rojas_local: 0,
            tarjetas_rojas_visitante: 0,
            corners_local: 0,
            corners_visitante: 0,
            minutos_local: 0,
            minutos_visitante: 0
        };
        values.forEach(function(value) {
            result.goles_local += value.goles_local;
            result.goles_visitante += value.goles_visitante;
            result.partidos_jugados += value.partidos_jugados;
            result.ganados += value.resultado.ganados;
            result.empatados += value.resultado.empatados;
            result.perdidos += value.resultado.perdidos;
            result.faltas_local += value.faltas_local;
            result.faltas_visitante += value.faltas_visitante;
            result.tarjetas_amarillas_local += value.tarjetas_amarillas_local;
            result.tarjetas_amarillas_visitante += value.tarjetas_amarillas_visitante;
            result.tarjetas_rojas_local += value.tarjetas_rojas_local;
            result.tarjetas_rojas_visitante += value.tarjetas_rojas_visitante;
            result.corners_local += value.corners_local;
            result.corners_visitante += value.corners_visitante;
            result.minutos_local += value.minutos_local;
            result.minutos_visitante += value.minutos_visitante;
        });
        return result;
    }
    """

    # Ejecutar MapReduce
    result = db.command('mapReduce', 'partidos', map=map_function, reduce=reduce_function, out='estadisticas_goles')

    print('MapReduce completado:', result)

    # Consultar los resultados del MapReduce
    print("Estadísticas de fútbol por equipo:")
    for doc in db.estadisticas_goles.find():
        total_goles = doc['value']['goles_local'] + doc['value']['goles_visitante']
        partidos_jugados = doc['value']['partidos_jugados']
        promedio_goles_por_partido = total_goles / partidos_jugados if partidos_jugados > 0 else 0
        diferencia_goles = doc['value']['goles_local'] - doc['value']['goles_visitante']
        print(f"Equipo: {doc['_id']}, Goles: {total_goles}, Partidos jugados: {partidos_jugados}, Promedio de goles por partido: {promedio_goles_por_partido}, Ganados: {doc['value']['ganados']}, Empatados: {doc['value']['empatados']}, Perdidos: {doc['value']['perdidos']}, Diferencia de goles: {diferencia_goles}")
        print(f"Faltas cometidas: Local {doc['value']['faltas_local']}, Visitante: {doc['value']['faltas_visitante']}")
        print(f"Tarjetas amarillas: Local {doc['value']['tarjetas_amarillas_local']}, Visitante: {doc['value']['tarjetas_amarillas_visitante']}")
        print(f"Tarjetas rojas: Local {doc['value']['tarjetas_rojas_local']}, Visitante: {doc['value']['tarjetas_rojas_visitante']}")
        print(f"Corners: Local {doc['value']['corners_local']}, Visitante: {doc['value']['corners_visitante']}")
        print(f"Minutos jugados: Local {doc['value']['minutos_local']}, Visitante: {doc['value']['minutos_visitante']}")



def start():
    top=Tk()
    B = Button(top, text ="Almacenar Resultados")
    B.pack()
    
    B2 = Button(top, text ="Listar Jornadas")
    B2.pack()
    
    B3 = Button(top, text ="Buscar Jornadas")
    B3.pack()
    
    B4 = Button(top, text ="Estadisticas Jornadas")
    B4.pack()
    
    B5 = Button(top, text ="Buscar Goles")
    B5.pack()
    
    top.mainloop()


if __name__ == '__main__':
    bd()
    start()