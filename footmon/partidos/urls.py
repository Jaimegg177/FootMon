from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import partidos_equipo_anyo_torneo, goles_por_jugador_y_anyo, goles_en_propia_reibidos_por_equipo, goles_por_equipo_en_torneo, maximo_goleador_equipo, primer_tiro_penaltis, media_goles_de_penalti_por_jugador, media_victorias_equipo, pagina_principal,maximo_goleador_equipo_aggregate, ciudades_con_mas_goles, ciudades_con_mas_goles_bucles

urlpatterns = [
    path('', pagina_principal, name='pagina_principal'),
    path('partidos_equipo_anyo_torneo/', partidos_equipo_anyo_torneo, name='partidos_equipo_anyoo_torneo'),
    path('goles_por_jugador_y_anyo', goles_por_jugador_y_anyo, name='goles_por_jugador_y_anyo'),
    path('goles_en_propia/', goles_en_propia_reibidos_por_equipo, name='goles_en_propia'),
    path('goles_por_equipo_en_torneo/', goles_por_equipo_en_torneo, name='goles_por_equipo_en_torneo'),
    path('maximo_goleador_equipo', maximo_goleador_equipo, name='maximo_goleador_equipo'),
    path('primer_tiro_penaltis/', primer_tiro_penaltis, name='primer_tiro_penaltis'),
    path('media_goles_de_penalti_por_jugador/', media_goles_de_penalti_por_jugador, name='media_goles_de_penalti_por_jugador'),
    path('media_victorias_equipo/', media_victorias_equipo, name='media_victorias_equipo'),
    path('maximo_goleador_equipo_aggregate/', maximo_goleador_equipo_aggregate, name='maximo_goleador_equipo_aggregate'),
    path('ciudades_con_mas_goles/', ciudades_con_mas_goles, name='ciudades_con_mas_goles'),
    path('ciudades_con_mas_goles_bucles/', ciudades_con_mas_goles_bucles, name='ciudades_con_mas_goles_bucles'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

