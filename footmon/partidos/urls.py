from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import shootouts_csv, results_csv, goalscorers_csv, consultas, datos, partidos_equipo_anyo_torneo, goles_por_jugador_y_anyo, goles_en_propia_reibidos_por_equipo, goles_por_equipo_en_torneo, maximo_goleador_equipo, maximo_goleador_equipo_aggregate, primer_tiro_penaltis, media_goles_de_penalti_por_jugador, media_victorias_equipo, pagina_principal, ciudades_con_mas_goles, ciudades_con_mas_goles_bucles


urlpatterns = [
    path('', pagina_principal, name='pagina_principal'),
    path('consultas/', consultas, name='consultas'),
    path('datos/', datos, name='datos'),
    path('consultas/partidos_equipo_anyo_torneo/', partidos_equipo_anyo_torneo, name='partidos_equipo_anyoo_torneo'),
    path('consultas/goles_por_jugador_y_anyo', goles_por_jugador_y_anyo, name='goles_por_jugador_y_anyo'),
    path('consultas/goles_en_propia/', goles_en_propia_reibidos_por_equipo, name='goles_en_propia'),
    path('consultas/goles_por_equipo_en_torneo/', goles_por_equipo_en_torneo, name='goles_por_equipo_en_torneo'),
    path('consultas/maximo_goleador_equipo', maximo_goleador_equipo, name='maximo_goleador_equipo'),
    path('consultas/primer_tiro_penaltis/', primer_tiro_penaltis, name='primer_tiro_penaltis'),
    path('consultas/media_goles_de_penalti_por_jugador/', media_goles_de_penalti_por_jugador, name='media_goles_de_penalti_por_jugador'),
    path('consultas/media_victorias_equipo/', media_victorias_equipo, name='media_victorias_equipo'),
    path('consultas/maximo_goleador_equipo_aggregate/', maximo_goleador_equipo_aggregate, name='maximo_goleador_equipo_aggregate'),
    path('consultas/ciudades_con_mas_goles/', ciudades_con_mas_goles, name='ciudades_con_mas_goles'),
    path('consultas/ciudades_con_mas_goles_bucles/', ciudades_con_mas_goles_bucles, name='ciudades_con_mas_goles_bucles'),
    path('results_csv/', results_csv, name='results_csv'),
    path('shootouts_csv/', shootouts_csv, name='shootouts_csv'),
    path('goalscorers_csv/', goalscorers_csv, name='goalscorers_csv'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

