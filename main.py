#Importamos las librerias necesarias:
#request: para realizar las solicitudes HTTP
#pandas: para trabajar con los datos
#sklearn: para crear el modelo de clasificacion

import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


#Consultar las API
url1 = "https://master--chevignon.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"
url2 = "https://master--pepeganga.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"

response1 = requests.get(url1)
response2 = requests.get(url2)

data1 = response1.json()
data2 = response2.json()


#Extraer la informacion
products1 = []
for product in data1:
    name = product['productName']
    description = product['description']
    products1.append({'name': name, 'description': description})

products2 = []
for product in data2:
    name = product['productName']
    description = product['description']
    products2.append({'name': name, 'description': description})


#Crear el modelo de clasificacion
# Vectorización de texto
vectorizer = CountVectorizer()
product_names = [product['name'] for product in products1 + products2]
product_descriptions = [product['description'] for product in products1 + products2]
X = vectorizer.fit_transform(product_names + product_descriptions)

# Cálculo de similitud coseno
def get_score(query):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, X).flatten()
    return scores

def classify(query, products):
    scores = get_score(query)
    results = []
    for i in range(len(products)):
        result = {'name': products[i]['name'], 'description': products[i]['description'], 'score': scores[i]}
        results.append(result)
    return results


# Función para ejecutar el clasificador y devolver los resultados con una propiedad de score
def classify_products(input_json):
    # Convertir el JSON a un diccionario de Python
    input_data = json.loads(input_json)

    # Extraer la keyword
    keyword = input_data['keyword']

    # Utilizar el clasificador para obtener los resultados
    results = classify(keyword, input_data['products'])

    # Agregar la propiedad score a cada producto
    for i in range(len(results)):
        results[i]['score'] = round(results[i]['score'] * 10, 2)

    # Convertir los resultados a formato JSON y devolverlos
    output_data = {'results': results}
    output_json = json.dumps(output_data)
    return output_json


# Ejemplo de entrada JSON
input_json = '{"products": [{"name": "chaqueta de mujer en cuero", "description": "Description 1"}, {"name": "chaqueta para hombre", "description": "Description 2"}], "keyword": "chaqueta"}'


# Llamar a la función classify_products() y obtener los resultados en formato JSON
output_json = classify_products(input_json)


# Imprimir los resultados en formato JSON
print(output_json)