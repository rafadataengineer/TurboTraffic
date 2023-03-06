# TurboTraffic

En este repositorio se encuentra el proyecto clasificador de productos para TurboTraffic

**Contenido**   
1. [¿Cómo funciona?](#id1)
2. [¿Cómo se utiliza?](#id2)
3. [Pruebas unitarias](#id3)
4. [Descripción modelo de clasificación](#id4)

## Clasificador de productos

Este es un proyecto de ejemplo que demuestra cómo utilizar un modelo de clasificación para clasificar productos basados en una palabra clave.

### ¿Cómo funciona?<a name="id1"></a>
El clasificador de productos utiliza un modelo de clasificación que toma una lista de productos y una palabra clave como entrada y devuelve una lista de resultados con una propiedad "score" en cada uno. El "score" indica el grado de coincidencia entre el producto y la palabra clave, siendo 0 el valor más bajo y 10 el valor más alto.

El modelo se entrena con una lista de productos de ejemplo que se obtienen de dos APIs diferentes. El modelo extrae información relevante de cada producto, como su nombre y descripción, y utiliza esta información para calcular el score.


### ¿Cómo se utiliza?<a name="id2"></a>
Para utilizar el clasificador de productos, se necesita tener Python y Docker instalados.

1. Clonar este repositorio.
2. Navegar al directorio del repositorio.
3. Construir la imagen de Docker ejecutando el siguiente comando:
```bash
docker build -t aplicacion .
```
4. Ejecutar el contenedor de Docker desde la imagen del punto anterior:
```bash
docker run -p 5000:5000 aplicacion
```

### Pruebas unitarias<a name="id3"></a>
El proyecto incluye pruebas unitarias para el modelo de clasificación. Estas pruebas se pueden ejecutar utilizando el módulo unittest de Python. Para ejecutar las pruebas, navegue al directorio del repositorio y ejecute el siguiente comando:
```bash
python test_app.py
```

### Descripción modelo de clasificación<a name="id4"></a>
Para realizar el modelo de clasificación de productos necesitamos seguir los siguientes pasos:

#### 1. Importar las librerias necesarias:
Para este proyecto, necesitamos importar las siguientes librerias:

* requests: para realizar solicitudes HTTP
* pandas: para trabajar con datos estructurados
* scikit-learn: para crear el modelo de clasificación
    
```python
import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
```

#### 2. Consultar las API
Podemos consultar las API utilizando la función requests.get(). En este caso, necesitamos especificar el rango de productos que deseamos obtener utilizando los parámetros _from y _to.

```python
url1 = "https://master--chevignon.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"
url2 = "https://master--pepeganga.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"

response1 = requests.get(url1)
response2 = requests.get(url2)

data1 = response1.json()
data2 = response2.json()
```

#### 3. Extraer la información relevante
Para crear nuestro modelo de clasificación, necesitamos extraer la información relevante de las API. En este caso, podemos extraer el nombre y la descripción del producto.

```python
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
```

#### 4. Crear el modelo de clasificación
Para crear el modelo de clasificación, utilizaremos la técnica de vectorización de texto y similitud coseno. Primero, necesitamos vectorizar los datos de entrenamiento (los nombres y las descripciones de los productos). Luego, podemos calcular la similitud coseno entre los vectores de búsqueda y los vectores de entrenamiento para determinar qué productos son los más relevantes.

```python
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
```

#### 5. Ejecutar el clasificador y devolver los resultados con una propiedad de score
Finalmente, utilizamos el clasificador para obtener los resultados y devolverlos al usuario en formato JSON con una propiedad de score para cada producto.

```python
# Función para ejecutar el clasificador y devolver los resultados
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
```

#### 6. Ahora podemos llamar a la función classify_products() con nuestro ejemplo de entrada y obtener los resultados en formato JSON.

```python
# Ejemplo de entrada JSON
input_json = '{"products": [{"name": "chaqueta de mujer en cuero", "description": "Description 1"}, {"name": "chaqueta para hombre", "description": "Description 2"}], "keyword": "chaqueta"}'


# Llamar a la función classify_products() y obtener los resultados en formato JSON
output_json = classify_products(input_json)


# Imprimir los resultados en formato JSON
print(output_json)
```


**¡Gracias por usar el clasificador de productos! Si tiene algún problema o pregunta, no dude en crear un issue en este repositorio.**
