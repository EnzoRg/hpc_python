#  Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes

# **Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento** 

## Objetivo 

Evaluar el desempeño de los filtros adaptativos Lee, Frost y Gamma-MAP en la reducción del ruido speckle en imágenes SAR, aplicándolos sobre un conjunto masivo de datos y optimizando el procesamiento mediante técnicas de multiprocesamiento.

## Introducción
Una forma de obtener una reconstrucción en 2D y 3D de una imágen aérea o de la superficie terrestre es mediante un radar de apertura sintética (SAR). Se basa en ondas electromagneticas para 

A diferencia de una cámara tradicional, que requiere la luz reflejada de la escena para formar una imagen, un SAR emite ondas electromagnéticas, las cuales rebotan en la superficie y son registradas como datos. El sensor SAR se encuentra montado en una plataforma móvil, y al desplazarse, combina las señales recibidas en distintos instantes lo que permite obtener una apertura sintetica y mejorar la resolución. A partir de estos datos se reconstruye la imagen.

Estas imágenes tienen la ventaja de no requerir una fuente de luz externa, y no se ven significativamente afectadas por la presencia de nubes o niebla. Además, brindan información sobre propiedades físicas de la escena, como la rugosidad del terreno, la humedad del suelo o la estructura de la vegetación.

Sin embargo, las imágenes SAR presentan un tipo de ruido multiplicativo denominado speckle. Este se origina porque las ondas reflejadas por distintos objetos dentro de un mismo píxel se suman o cancelan entre sí de manera coherente. El resultado es una textura granular que degrada la calidad visual de la imagen y dificulta su interpretación. Para mitigar este efecto se aplican diferentes técnicas de filtrado, entre las que se destacan los filtros Lee, Frost y Gamma-MAP.

Por otro lado, las imágenes SAR suelen ser de gran tamaño o generarse en grandes volúmenes, lo que dificulta su almacenamiento y procesamiento. 

## Experimento

Para evaluar el desempeño de un filtro para reducir el speckle, se requiere un conjunto de datos que contenga pares de imagenes SAR limpias y con ruido. Virtual SAR [1] es un dataset de imágenes aereas sobre la superficie terrestre. Contiene 31.500 pares de imagenes SAR sintéticas limpias y con ruido, lo cual resultan utiles para evaluar distintos métodos para reducir el speckle. 

<p align="center">
    <img src="/proyecto/imagenes/image_sar.png" alt="Imagen SAR" width="500"/>  
</p>

Mediante filtos adaptativos se puede reducir los efectos del speckle en imágenes SAR. El filtro Lee [2] suaviza el ruido en regiones homogéneas mientras preserva los bordes y detalles, ajustando la cantidad de filtrado según la variabilidad local de la imagen. El filtro Frost [3] utiliza un enfoque similar, pero pondera los píxeles cercanos al centro de la ventana de análisis y aquellos con valores más similares, lo que permite mantener estructuras importantes y contornos definidos. Por su parte, el filtro Gamma-MAP [4] se basa en un modelo estadístico del speckle, buscando estimar la señal subyacente de manera óptima; es especialmente efectivo en áreas homogéneas y contribuye a mejorar la calidad de la imagen sin comprometer demasiado la resolución.

<p align="center">
    <img src="/proyecto/imagenes/filtros.png" alt="Filtros" width="800"/>
</p>

Las métricas utilizadas para evaluar cada filtro son:
- **Structural Similarity Index Measure (SSIM):** mide la similitud estructural entre la imagen filtrada y la imagen de referencia. Evalúa aspectos como luminosidad, contraste y estructura, proporcionando un valor entre 0 y 1, donde valores más cercanos a 1 indican una mayor similitud.
- **Peak signal-to-noise ratio (PSNR):** cuantifica la relación entre la señal (imagen original de referencia) y el ruido introducido o no eliminado en la imagen filtrada. Se expresa en decibelios (dB) y valores más altos corresponden a una mejor calidad.

Las metricas utilizadas para evaluar el rendimiento al paralelizar el proceso son:

- Tiempo de ejecución: mide el tiempo total que tarda en completarse la tarea, tanto en la versión secuencial como en la paralela.

- Speedup: representa la ganancia obtenida al paralelizar. Se define como la relación entre el tiempo de ejecución secuencial y el tiempo de ejecución paralelo con *p* procesadores. Un valor mayor indica una aceleración más efectiva.

- Eficiencia: mide el grado de aprovechamiento de los recursos de cómputo. Se calcula como el speedup dividido por el número de procesadores *p*. Un valor de 1 representa el caso ideal, en el cual todos los procesadores se utilizan de forma óptima.
<p align="center">
    <img src="/proyecto/results/boxplot.png" alt="Boxplot SSIM PSNR" width="800"/>  
</p>

<p align="center">
    <img src="/proyecto/results/rendimiento.png" alt="Rendimiento" width="800"/>  
</p>

## Referencias
[1] Virtual SAR: A Synthetic Dataset for  Deep Learning based Speckle Noise Reduction  Algorithms

[2] Lee

[3] Frost

[4] Gamma-MAP
