from PIL import Image
import numpy as np
import pandas as pd 
import sys
np.set_printoptions(threshold=sys.maxsize)

# Abrir imagen a color y convertirla a niveles de gris
image = Image.open('D:/Documentos/ING.Conocimiento/Taller_IA/Aprendizaje Profundo/Datos/dato_1_800x800.jpg').convert("L")

# Tamaño de la imagen
print(image.size)

# Rescalar la imagen a 32 x 32
image = image.resize((32,32))
image.save("D:/Documentos/ING.Conocimiento/Taller_IA/Aprendizaje Profundo/Datos/imagen_pequeña_1.jpg", "JPEG", optimize=True)

# tamaño de la imagen
print(image.size)

# Crear un arreglo con la imágen
arr = np.asarray(image).reshape(1024)

# Imprimir la forma del arreglo 
print(arr.shape)
# Imprimir el arreglo 
print(arr)

# convert array into dataframe 
df = pd.DataFrame(arr) 
  
# save the dataframe as a csv file 
df.to_csv("D:/Documentos/ING.Conocimiento/Taller_IA/Aprendizaje Profundo/Datos/datos_2.csv")

