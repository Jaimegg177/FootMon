import os
import django
import pandas as pd
from pymongo import MongoClient
from django.core.management import call_command

def populate_db():
    # Configurar las settings de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'footmon.settings')
    django.setup()

    # Conexión a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['deportes_db']

    # Borra la base de datos entera
    client.drop_database('deportes_db')
    print("Base de datos borrada")

    # Colecciones
    results = db['partidos_partido']
    goalscorers = db['partidos_goleadores']
    shootouts = db['partidos_penaltis']

    # Insertar resultados
    data_results = pd.read_csv('data/results.csv')
    data_goalscorers = pd.read_csv('data/goalscorers.csv')
    data_shootouts = pd.read_csv('data/shootouts.csv')

    # Convertir los datos a un formato compatible con MongoDB
    data_results_json = data_results.to_dict(orient='records')
    data_goalscorers_json = data_goalscorers.to_dict(orient='records')
    data_shootouts_json = data_shootouts.to_dict(orient='records')

    # Insertar los datos en la colección de MongoDB
    results.insert_many(data_results_json)
    goalscorers.insert_many(data_goalscorers_json)
    shootouts.insert_many(data_shootouts_json)

    print("Datos insertados en la base de datos")

    # Ejecutar migraciones de Django
    call_command('makemigrations')
    print("Migraciones hechas")

    call_command('migrate')
    print("Migraciones completadas")

# Ejecutar la función
populate_db()
