from django.urls import path
from .views import partidos_equipo_anyo_torneo, goles_en_propia_reibidos_por_equipo, goles_por_equipo_en_torneo, primer_tiro_penaltis

urlpatterns = [
    path('partidos_equipo_anyo_torneo/', partidos_equipo_anyo_torneo, name='partidos_equipo_anyoo_torneo'),
    path('goles_en_propia/', goles_en_propia_reibidos_por_equipo, name='goles_en_propia'),
    path('goles_por_equipo_en_torneo/', goles_por_equipo_en_torneo, name='goles_por_equipo_en_torneo'),
    path('primer_tiro_penaltis/', primer_tiro_penaltis, name='primer_tiro_penaltis'),
]