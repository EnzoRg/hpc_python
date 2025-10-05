#  Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes

# **Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento** 

## Objetivo 

Evaluar el desempeño de los filtros adaptativos Lee, Frost y Gamma-MAP en la reducción de speckle en imágenes SAR, aplicándolos sobre diversas imágenes de la superficie terrestre mediante técnicas de multiprocesamiento.

## Introducción
Una forma de obtener una reconstrucción de la superficie terrestre es mediante un radar de apertura sintética (SAR). A diferencia de una cámara tradicional, que requiere la luz reflejada de la escena para formar una imágen, un SAR ilumina la escena mediante ondas electromagenticas. Estas rebotan sobre la superficie y son capturadas como datos para luego formar una imágen.

El sensor SAR se encuentra montado en una plataforma móvil, y al desplazarse combina las ondas recibidas en distintos momentos lo que permite obtener una apertura sintetica y mayor resolución. 

Estas imágenes tienen la ventaja de no necesitar una fuente de luz externa, y no se ven significativamente afectadas por la presencia de nubes. Además, brindan información sobre propiedades físicas de la escena, como la rugosidad del terreno, la humedad del suelo o el tipo de material.

Sin embargo, las imágenes SAR presentan un tipo de ruido multiplicativo denominado **speckle**. Este se origina porque las ondas reflejadas por distintos objetos dentro de un mismo píxel se suman o cancelan entre sí de manera coherente. El resultado es una textura granular que degrada la calidad visual de la imagen y dificulta su interpretación. Para mitigar este efecto se aplican diferentes técnicas de filtrado, entre las que se destacan los filtros Lee, Frost y Gamma-MAP.

Por otro lado, las imágenes SAR suelen ser de gran tamaño o generarse en grandes volúmenes, lo que dificulta su procesamiento. Cada imágen debe leerse, filtrarse y luego guardarse para su posterior análisis. Al paralelizar los datos se aprovecha mejor los recursos de computo y obtener imágenes listas para su uso más rápido. 

## Experimento

### Datasets
Para evaluar el desempeño de un filtro para reducir el speckle, se requiere un conjunto de datos que contenga pares de imagenes SAR limpias y con ruido. Virtual SAR [1] es un dataset de imágenes aéreas sobre la superficie terrestre. Contiene 31.500 pares de imagenes SAR sintéticas limpias y con ruido, lo cual resultan utiles para evaluar distintos métodos para reducir el speckle. 

<p align="center">
    <img src="/proyecto/imagenes/image_sar.png" alt="Imagen SAR" width="500"/>  
</p>

### Filtros
El filtro Lee [2] suaviza el ruido en regiones homogéneas mientras preserva los bordes y detalles, ajustando la cantidad de filtrado según la variabilidad local de la imagen. El filtro Frost [3] utiliza un enfoque similar, pero pondera los píxeles cercanos al centro de la ventana de análisis y aquellos con valores más similares, lo que permite mantener estructuras importantes y contornos definidos. Por su parte, el filtro Gamma-MAP [4] se basa en un modelo estadístico del speckle, buscando estimar la señal subyacente de manera óptima, es especialmente efectivo en áreas homogéneas y contribuye a mejorar la calidad de la imagen sin comprometer demasiado la resolución.

<p align="center">
    <img src="/proyecto/imagenes/filtros.png" alt="Filtros" width="800"/>
</p>

### Paralelización de Datos
Debido al gran conjunto de datos se opta por paralelizar los datos mediante multiprocesamiento. A través del objeto **Pool**:

1. Se crea un conjunto de procesos.
2. Se define un conjunto de datos que van a ser distribuidos a los procesos elemento a elemento.
3. Los procesos ejecutan una tarea que se aplica sobre cada elemento.
4. Los datos de distribuyen entre los procesos de forma automática y ordenada. 

### Métricas
Las métricas utilizadas para evaluar cada filtro son:
- **Structural Similarity Index Measure (SSIM):** mide la similitud estructural entre la imagen filtrada y la imagen de referencia. Evalúa aspectos como luminosidad, contraste y estructura, proporcionando un valor entre 0 y 1, donde valores más cercanos a 1 indican una mayor similitud.
- **Peak signal-to-noise ratio (PSNR):** cuantifica la relación entre la señal (imagen original de referencia) y el ruido introducido o no eliminado en la imagen filtrada. Se expresa en decibeles (dB) y valores más altos corresponden a una mejor calidad.

Las metricas utilizadas para evaluar el rendimiento al paralelizar el proceso son:

- **Tiempo de ejecución:** mide el tiempo total que tarda en completarse la tarea, tanto en la versión secuencial como en la paralela.

- **SpeedUp:** representa la ganancia obtenida al paralelizar. Se define como la relación entre el tiempo de ejecución secuencial y el tiempo de ejecución paralelo con *p* procesadores. Un valor mayor indica una aceleración más efectiva.

- **Eficiencia:** mide el grado de aprovechamiento de los recursos de cómputo. Se calcula como el SpeedUp dividido por el número de procesadores *p*. Un valor de 1 representa el caso ideal, en el cual todos los procesadores se utilizan de forma óptima.


## Resultados

### Ejecución
Para esta primer instancia se evaluaron tres batchs de 10, 100 y 1.000 imágenes respectivamente. Los boxplots fueron creados a partir de los resultados de las 1.000 imágenes.

```bash
# Crear el entorno
conda env create -f environment.yaml

# Activar el entorno
conda activate hpc_python

# Script principal
python main.py

# Generar gráficos para evaluar filtros
python plot_img_stats.py

# Generar gráficos para evaluar rendimiento
python plot_all.py
```
### PSNR y SSIM

<p align="center">
    <img src="/proyecto/results/boxplot.png" alt="Boxplot SSIM PSNR" width="800"/>  
</p>

Mediante los gráficos de boxplot se ve que para PSNR, Gamma-MAP presenta la mayor mediana y menor dispersión, indicando mejor preservación de la señal. Frost se ubica en segundo lugar, con valores consistentes pero algo más bajos. Lee muestra alta variabilidad y mediana más baja, con riesgo de degradar la calidad en ciertas imágenes pero alcanzando en algunos casos los valores más altos de PSNR.

Al analizar SSIM, Gamma-MAP vuelve a destacar con medianas más altas. Frost mantiene resultados aceptables, aunque con mayor dispersión. Lee tiende a valores más bajos y con más dispersión, indicando menor preservación de estructuras.

### Rendimiento

<p align="center">
    <img src="/proyecto/results/rendimiento.png" alt="Rendimiento" width="800"/>  
</p>

El aumento en el número de procesos reduce significativamente el tiempo, sobre todo para el batch de 1.000 imágenes. A partir de 6 procesos, la reducción de tiempo se estabiliza, indicando saturación de recursos.

En el batch de 1.000 imágenes se alcanza un SpeedUp de x5, cercano al ideal para 6 procesos. El batch de 10 imágenes muestra un SpeedUp limitado (x3), debido a la sobrecarga de comunicación en comparación con el trabajo útil.

El batch 1.000 mantiene eficiencias relativamente altas (>0.8 hasta 6 procesos). Batch 10 y 100 caen más rápido, llegando a <0.5 con más de 8 procesos. Esto confirma que mayor cantidad de imágenes son más adecuadas para el paralelismo, aprovechando mejor la distribución del trabajo.

## Conclusiones
El experimento muestra que el escalado de prceosos paralelizados resulta eficiente hasta cierto punto (aproximadamente 6–8 procesos), alcanzando altos niveles de rendimiento para cargas grandes, aunque con una eficiencia decreciente cuando son menos imágenes, lo que evidencia que la granularidad del batch es un factor crítico. En cuanto a la calidad de los resultados, el filtro Gamma-MAP se destaca por ofrecer el mejor equilibrio entre reducción de ruido y preservación estructural (reflejado en valores altos de PSNR y SSIM), mientras que el Frost ocupa una posición intermedia y el Lee se presenta como el menos robusto dentro del conjunto de datos evaluado.

## Trabajos Futuros
Para mejorar este trabajo, se propone:
- Utilizar batchs de imágenes más grandes, hasta 31.500.
- Evaluar versiones más modernas de los filtros utilizados. 
- Utilizar multihilo para la lectura y escritura de imágenes.
- Mediante GPU utilizar PyCUDA y CUPy para procesar imágenes.

## Referencias
[1] S. Dabhi, K. Soni, U. Patel, P. Sharma, and M. Parmar, "Virtual SAR: A Synthetic Dataset for Deep Learning based Speckle Noise Reduction Algorithms," in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2021, pp. 1968–1977. doi: 10.1109/CVPRW53098.2021.00209.

[2] J.-S. Lee, "Digital Image Enhancement and Noise Filtering by Use of Local Statistics," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. PAMI-2, no. 2, pp. 165–168, Mar. 1980, doi: 10.1109/TPAMI.1980.4766994.

[3] V. S. Frost, J. A. Stiles, K. S. Shanmugan and J. C. Holtzman, "A Model for Radar Images and Its Application to Adaptive Digital Filtering of Multiplicative Noise," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. PAMI-4, no. 2, pp. 157–165, Mar. 1982, doi: 10.1109/TPAMI.1982.4767223.

[4] A. Lopes, R. Touzi and E. Nezry, "Adaptive Speckle Filters and Scene Heterogeneity," IEEE Transactions on Geoscience and Remote Sensing, vol. 28, no. 6, pp. 992–1000, Nov. 1990, doi: 10.1109/36.61764.
