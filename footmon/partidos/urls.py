from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import shootouts_csv, results_csv, goalscorers_csv, consultas, datos, partidos_equipo_anyo_torneo, goles_por_jugador_y_anyo, goles_en_propia_reibidos_por_equipo, goles_por_equipo_en_torneo, maximo_goleador_equipo, primer_tiro_penaltis, media_goles_de_penalti_por_jugador, media_victorias_equipo, pagina_principal

urlpatterns = [
    path('', pagina_principal, name='pagina_principal'),
    path('consultas/', consultas, name='consultas'),
    path('datos/', datos, name='datos'),
    path('partidos_equipo_anyo_torneo/', partidos_equipo_anyo_torneo, name='partidos_equipo_anyoo_torneo'),
    path('goles_por_jugador_y_anyo', goles_por_jugador_y_anyo, name='goles_por_jugador_y_anyo'),
    path('goles_en_propia/', goles_en_propia_reibidos_por_equipo, name='goles_en_propia'),
    path('goles_por_equipo_en_torneo/', goles_por_equipo_en_torneo, name='goles_por_equipo_en_torneo'),
    path('maximo_goleador_equipo', maximo_goleador_equipo, name='maximo_goleador_equipo'),
    path('primer_tiro_penaltis/', primer_tiro_penaltis, name='primer_tiro_penaltis'),
    path('media_goles_de_penalti_por_jugador/', media_goles_de_penalti_por_jugador, name='media_goles_de_penalti_por_jugador'),
    path('media_victorias_equipo/', media_victorias_equipo, name='media_victorias_equipo'),
    path('results_csv/', results_csv, name='results_csv'),
    path('shootouts_csv/', shootouts_csv, name='shootouts_csv'),
    path('goalscorers_csv/', goalscorers_csv, name='goalscorers_csv'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

