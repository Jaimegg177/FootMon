from django.shortcuts import render
from pymongo import MongoClient

# Create your views here.

client = MongoClient('mongodb://localhost:27017/')
db = client['deportes_db']

# 1 Partidos jugados por cada equipo en cada año en una competición dada
def partidos_equipo_anyo_torneo(request):
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
    resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function, out='partidos_por_equipo_por_año_en_torneo')

    sorted_result = list(db.partidos_por_equipo_por_año_en_torneo.find().sort([('year', -1)]))

    return render(request, 'partidos_equipo_anyo_torneo.html', {'sorted_result': sorted_result})

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
        return Array.sum(values);
    }
    """
    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function, out='goles_por_jugador_y_anyo')

    sorted_result = list(db.goles_por_jugador_y_anyo.find().sort([('year', -1)]))

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
        return Array.sum(values);
    }
    """

    resultado = db.command('mapReduce', 'partidos_goleadores', map=map_function, reduce=reduce_function, out='goles_en_propia')

    sorted_result = list(db.goles_en_propia.find().sort([('value', -1)]))

    return render(request, 'goles_propia.html', {'sorted_result': sorted_result})

# 5 Maximo goleador de cada equipo (aggregation o procesado)

# 6 Top 10 ciudades con resultados más altos (procesando)

# 6 Top 10 ciudades con resultados más altos (bucles)

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
        return Array.sum(values);
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
        return Array.sum(values);
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
        value.media_victorias = value.ganados/value.jugados * 100;
        return value;
    }
    """

    resultado = db.command('mapReduce', 'partidos_partido', map=map_function, reduce=reduce_function,finalize=finalize_function, out='porcentaje_partidos_ganados_por_equipo')

    sorted_result = list(db.porcentaje_partidos_ganados_por_equipo.find().sort([('value.percentage_wins', -1)]))

    return render(request, 'media_victorias_equipo.html', {'sorted_result': sorted_result})


# MAIN

def pagina_principal(request):
    return render(request, 'main.html', {})
