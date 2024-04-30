# FootMon
Repositorio proyecto CBD - MapReduce MongoDB

## Manual de instalación

Para poder instalar y ejecutar esta aplicación, primero se deben cumplir los siguientes requisitos:

- Tener instalado MongoDB.
- Tener instalado un editor de código.
- Tener clonado el repositorio de github. Lo encontramos en este enlace: [https://github.com/Jaimegg177/FootMon](https://github.com/Jaimegg177/FootMon)

Si cumplimos estos requisitos, podemos empezar con la instalación:

1. Abrir el proyecto en el editor de código.
2. Instalamos los paquetes/requisitos mediante `pip install -r requirements.txt` (recomendamos crear un entorno virtual previamente mediante `python -m venv env`).
3. Debemos haber ejecutado MongoDB para poder conectarnos a la base de datos.
4. Para poblar los datos ejecutamos el archivo `populate_db.py` mediante la instrucción `python populate_dd.py`.
5. Ejecutamos el proyecto mediante `python manage.py runserver`, lo que abrirá el proyecto en el puerto 8000.
6. A partir de aquí ya podemos usar la aplicación.

### Cosas a tener en cuenta y posibles errores que podemos encontrar:

- En caso de que al popular la base de datos se quede parado calculando sin avanzar, es posible que no se haya levantado la base de datos correctamente o no coincidan los puertos. Asegúrate de que el puerto en el que tienes la base de datos levantada es el mismo que está definido en el código. Concretamente en el archivo de población en la línea `client = MongoClient("mongodb://localhost:27017/")`. Esto también deberá coincidir en el archivo `views.py` en la carpeta `partidos` y en el `settings.py` en el campo `port` dentro del apartado `databases`.
- Si al ejecutar el proyecto mediante `runserver` da error de conflicto de puertos, significa que ya está el puerto 8000 en uso, por lo que habrá que liberarlo.
