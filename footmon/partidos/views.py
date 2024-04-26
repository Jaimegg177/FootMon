from django.shortcuts import render
from pymongo import MongoClient

# Create your views here.

client = MongoClient('mongodb://localhost:27017/')
db = client['deportes_db']

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