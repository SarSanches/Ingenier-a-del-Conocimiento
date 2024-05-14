import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns # type: ignore

from sklearn import preprocessing # type: ignore

#### EXPLORACION Y VISUALIZACIÓN DE LOS DATOS ####

# Cargar datos de clientes en un DataFrame de pandas
df = pd.read_csv('D:/Documentos/ING.Conocimiento/Taller_IA/Hierarchical Clustering/Datos/Mall_Customers.csv')

# Regresar los primeros n renglones (default n=5)
print('\n')
print(df.head())
print('\n')

# El numero de datos nulos por columna
print(df.isnull().sum())
print('\n')

# Regresa algunas estadisticas por columna
print(df.describe())
print('\n')

# Graficar histograma junto con gráfica de densidad
plt.figure(1 , figsize = (15 , 6))
n = 0
for x in ['Age' , 'Annual Income (k$)' , 'Spending Score (1-100)']:
    n += 1
    plt.subplot(1 , 3 , n)
    plt.subplots_adjust(hspace = 0.5 , wspace = 0.5)
    sns.histplot(df[x] , bins = 15, kde=True, stat="density", kde_kws=dict(cut=3), alpha=.4, edgecolor=(1, 1, 1, .4))
    plt.title('Histogram of {}'.format(x))
plt.show()

# Codificación de etiquetas
label_encoder = preprocessing.LabelEncoder() 
df['Gender'] = label_encoder.fit_transform(df['Gender'])
print('\n')
print(df.head())

# Mapa de calor
plt.figure(1, figsize = (16 ,8))
sns.heatmap(df)
plt.show()