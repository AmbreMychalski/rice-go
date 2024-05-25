# GO-RICE

**Exploración de modelos de aprendizaje automático como medio para la predicción de funcionalidades de genes**

Duvan Bonilla - Marine Buliard - Ambre Mychalski - Theo Llopis

## Objetivo general:
El objetivo de este proyecto es crear una herramienta capaz de predecir la función de un gen (su ontología) del reino vegetal basado en su secuencia y su traducción a proteína.


## Comó utilizar el proyecto:
### Librerías
Por favor, asegúrense de tener instaladas las librerías Python:
  - Numpy
  - Pandas
  - Joblib
  - Flask and Flask-CORS

LLas versiones se encuentran en Back_Python/requirements.txt. Para instalar todas las librerías y las versiones correctas, vayan a la carpeta Back_Python y ejecuten:
> pip install -r .\requirements.txt

### Lanzar el proyecto
Para lanzar el proyecto, vayan a la carpeta Back_Python y ejecuten:
> python app.py

Vayan al navegador y abran:
> http://127.0.0.1:3001

### Predecir la función de un gen desde una cadena de DNA
Para utilizar el proyecto, ingresen en la barra de búsqueda la cadena de ADN codificante de una proteína de la cual quieren predecir una función genómica. Den clic en "search" o presionen "Enter".

Por ejemplo, ingresen la cadena:

> ATGGCGCTCAAGGTCGTCTCTTTCCCCGGGGACTTGGCCGCGGTCTCATTCCTCGACTCCAACAGAGGAGGAGCTTTCAACCAGCTCAAAG

## Especificaciones del proyecto:
El backend es en Python, utilizando el framework Flask.

Los modelos de machine learning utilizados están ubicados en la carpeta Back_Python/models y son de tipo joblib.

Utilizamos una API y archivos JSON para comunicarnos con el frontend en React.
