import csv
import os
from django.shortcuts import render
from pymongo import MongoClient
from .models import Partido

# Create your views here.

client = MongoClient('mongodb://localhost:27017/')
db = client['deportes_db']

# 1 Partidos jugados por cada equipo en cada año en una competición dada
def partidos_equipo_anyo_torneo(request):

    torneos = db.partidos_partido.distinct("tournament")
    if request.method == 'POST':
        selected_tournament = str(request.POST.get("tournament"))
        # Función de map
        map_function = f"""
        function() {{
            if (this.tournament == '{selected_tournament}') {{
                var year = this.date.split('-')[0];
                emit({{year: year, tournament: this.tournament, team: this.home_team}}, 1);
                emit({{year: year, tournament: this.tournament, team: this.away_team}}, 1);
            }}
        }}
        """
        # Función de reduce
        reduce_function = """
        function(key, values) {
            return {matches: Array.sum(values), tournament: key.tournament, team: key.team, year: key.year};
        }
        """
        resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function, out='partidos_por_equipo_por_año_en_torneo')

        sorted_result = list(db.partidos_por_equipo_por_año_en_torneo.find().sort([('year', -1)]))
        return render(request, 'partidos_equipo_anyo_torneo.html', {'sorted_result': sorted_result, 'torneos': torneos, 'selected_tournament': selected_tournament})

    return render(request, 'partidos_equipo_anyo_torneo.html', {'torneos': torneos})

# 2 Goles marcadados por cada jugador en cada año
def goles_por_jugador_y_anyo(request):
    # Función de map
    map_function = """
    function() {
        var year = this.date.split('-')[0];
        emit({year: year, scorer: this.scorer}, 1);
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return {goals: Array.sum(values), scorer: key.scorer, year: key.year};
    }
    """
    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function, out='goles_por_jugador_y_anyo')

    sorted_result = list(db.goles_por_jugador_y_anyo.find().sort([('value.scorer', -1)]))

    return render(request, 'goles_por_jugador_y_anyo.html', {'sorted_result': sorted_result})

# 3 Media de goles de penalti de cada jugador.
def media_goles_de_penalti_por_jugador(request):
    # Función de map
    map_function = """
    function() {
        emit({scorer: this.scorer}, this.penalty);
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        penalty = 0;
        for (var i = 0; i < values.length; i++) {
            if(values[i] == true) {
                penalty += 1;
            }
        }
        return {goles: values.length, penaltis: penalty};
    }
    """
    finalize_function="""
    function (key, value) {
        value.key = key;
        value.avg = value.penaltis/value.goles *100;
        return value;
    }
    """

    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function,finalize=finalize_function, out='goles_de_penalti_por_jugador')

    sorted_result = list(db.goles_de_penalti_por_jugador.find().sort([('value', -1)]))

    return render(request, 'media_goles_de_penalti_por_jugador.html', {'sorted_result': sorted_result})
    
# 4 Goles en propia recibidos por cada equipo 
def goles_en_propia_reibidos_por_equipo(request):
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
        return {goals:Array.sum(values), team: key.team};
    }
    """

    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function, out='goles_en_propia')

    sorted_result = list(db.goles_en_propia.find().sort([('value', -1)]))

    return render(request, 'goles_propia.html', {'sorted_result': sorted_result})

# 5 Maximos goleadores de cada equipo (aggregation o procesado)
def maximo_goleador_equipo(request):
    # Función de map
    map_function = """
    function() {
        emit({team: this.team, scorer: this.scorer}, 1);
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return Array.sum(values);
    }
    """

    # Ejecutar MapReduce
    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function, out='maximo_goleador_equipo')

    # Obtener los resultados ordenados por el número de goles en orden descendente
    sorted_result = list(db.maximo_goleador_equipo.find().sort([('value', -1)]))

    # Crear un diccionario para almacenar los máximos goleadores de cada equipo
    max_goleadores_por_equipo = {}

    # Iterar sobre los resultados y almacenar solo los tres máximos goleadores de cada equipo
    for result in sorted_result:
        equipo = result['_id']['team']
        goleador = result['_id']['scorer']
        goles = result['value']
        
        if equipo not in max_goleadores_por_equipo:
            max_goleadores_por_equipo[equipo] = []

        if len(max_goleadores_por_equipo[equipo]) < 3:
            max_goleadores_por_equipo[equipo].append({'scorer': goleador, 'goals': goles})


    return render(request, 'maximo_goleador_equipo.html', {'max_goleadores_por_equipo': max_goleadores_por_equipo})

def maximo_goleador_equipo_aggregate(request):
    pipeline = [
        {
            "$group": {
                "_id": {"team": "$team", "scorer": "$scorer"},
                "goals": {"$sum": 1}
            }
        },
        {
            "$sort": {"goals": -1, "_id.team": 1}
        },
        {
            "$group": {
                "_id": "$_id.team",
                "max_scorers": {
                    "$push": {
                        "scorer": "$_id.scorer",
                        "goals": "$goals"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "team": "$_id",
                "max_scorers": {"$slice": ["$max_scorers", 3]}
            }
        },
        {
            "$sort": {"max_scorers.goals": -1}
        }
    ]

    max_goleadores_por_equipo = list(db.partidos_goleadores.aggregate(pipeline))

    return render(request, 'maximo_goleador_equipo_aggregate.html', {'max_goleadores_por_equipo': max_goleadores_por_equipo})

# 6 Top 10 ciudades con resultados más altos (procesando)

def ciudades_con_mas_goles(request):
    # Función de map
    map_function = """
    function() {
        emit(this.city, this.home_score + this.away_score);
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        return {value: Array.sum(values), city: key};
    }
    """

    # Ejecutar MapReduce
    resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function, out='ciudades_con_mas_goles')

    # Obtener los resultados ordenados por la suma de goles en orden descendente y limitar a 10 resultados
    sorted_result = list(db.ciudades_con_mas_goles.find().sort([('value', -1)]).limit(10))

    return render(request, 'ciudades_con_mas_goles.html', {'sorted_result': sorted_result})
# 6 Top 10 ciudades con resultados más altos (bucles)
def ciudades_con_mas_goles_bucles(request):
    # Obtener todos los partidos de la base de datos
    partidos = Partido.objects.all()

    # Diccionario para almacenar la suma de goles por ciudad
    goles_por_ciudad = {}

    # Calcular la suma de goles por ciudad
    for partido in partidos:
        ciudad = partido.city
        goles_totales = partido.home_score + partido.away_score
        if ciudad in goles_por_ciudad:
            goles_por_ciudad[ciudad] += goles_totales
        else:
            goles_por_ciudad[ciudad] = goles_totales

    # Ordenar el diccionario por la suma de goles en orden descendente
    sorted_result = sorted(goles_por_ciudad.items(), key=lambda x: x[1], reverse=True)[:10]

    return render(request, 'ciudades_con_mas_goles_bucles.html', {'sorted_result': sorted_result})

# 7 Número de goles metidos por cada equipo en cada torneo
def goles_por_equipo_en_torneo(request):
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
        return {goals:Array.sum(values), team: key.team, tournament: key.tournament};
    }
    """

    # Ejecutar MapReduce
    resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function, out='goles_por_equipo_torneo')

    sorted_result = list(db.goles_por_equipo_torneo.find().sort([('value', -1)]))

    return render(request, 'goles_por_equipo_en_torneo.html', {'sorted_result': sorted_result})

# 8 Cuántas veces cada equipo ha chutado primero en una tanda de penaltis
def primer_tiro_penaltis(request):

    map_function = """
    function() {
        emit({team: this.first_shooter}, 1);
    }
    """

    # Función de reduce para calcular número de veces que cada equipo ha chutado primero en tanda de penaltis
    reduce_function = """
    function(key, values) {
        return {times: Array.sum(values), team: key.team};
    }
    """

    # Ejecutar MapReduce para calcular número de veces que cada equipo ha chutado primero en tanda de penaltis
    resultado = db.command('mapReduce', 'partidos_penaltis', map=map_function, reduce=reduce_function, out='chutes_primero_en_penaltis')
    sorted_result = list(db.chutes_primero_en_penaltis.find().sort([('value', -1)]))

    return render(request, 'primer_tiro_penaltis.html', {'sorted_result': sorted_result})

# 9 Promedio de partidos ganados por equipo
def media_victorias_equipo(request):
    # Función de map
    map_function = """
    function() {
        emit({team: this.home_team}, {jugados: 1, ganados: this.home_score > this.away_score ? 1 : 0});
        emit({team: this.away_team}, {jugados: 1, ganados: this.home_score < this.away_score ? 1 : 0});
    }
    """

    # Función de reduce
    reduce_function = """
    function(key, values) {
        var total_matches = 0;
        var total_wins = 0;
        for (var i = 0; i < values.length; i++) {
            total_matches += values[i].jugados;
            total_wins += values[i].ganados;
        }
        return {jugados: total_matches, ganados: total_wins};
    }
    """
    finalize_function="""
    function (key, value) {
        value.team = key.team;
        value.media_victorias = value.ganados/value.jugados * 100;
        return value;
    }
    """

    resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function,finalize=finalize_function, out='porcentaje_partidos_ganados_por_equipo')

    sorted_result = list(db.porcentaje_partidos_ganados_por_equipo.find().sort([('value.media_victorias', -1)]))

    return render(request, 'media_victorias_equipo.html', {'sorted_result': sorted_result})


# NavBar
def pagina_principal(request):
    return render(request, 'main.html', {})

def datos(request):
    return render(request, 'datos.html', {})

def consultas(request):
    return render(request, 'consultas.html', {})

# CSVs
def results_csv(request):
     # Ruta del archivo CSV
    csv_path = os.path.join('data','results.csv')

    # Leer el archivo CSV y procesar los datos
    csv_data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    # Renderizar una plantilla HTML para mostrar los datos
    return render(request, 'resultsCSV.html', {'csv_data': csv_data})

def goalscorers_csv(request):
    # Ruta del archivo CSV
    csv_path = os.path.join('data', 'goalscorers.csv')

    # Leer el archivo CSV y procesar los datos
    csv_data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    # Renderizar una plantilla HTML para mostrar los datos
    return render(request, 'goalscorersCSV.html', {'csv_data': csv_data})

def shootouts_csv(request):
     # Ruta del archivo CSV
    csv_path = os.path.join('data','shootouts.csv')

    # Leer el archivo CSV y procesar los datos
    csv_data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_data.append(row)

    # Renderizar una plantilla HTML para mostrar los datos
    return render(request, 'shootoutsCSV.html', {'csv_data': csv_data})

