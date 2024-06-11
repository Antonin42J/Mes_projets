# Machine Learning Big Data

Date : Novembre 2023

Language : Python (PySpark)

Ce projet consistait à répondre à différentes questions sur l'analyse de data sur les cas de COVID-19 dans le monde. Pour ce faire, l'utilisation de Spark et de son module Python était obligatoire. Durant ce projet, il a aussi fallu mettre en place une régression linéaire afin de déterminer les pays les plus fortement touchés. Pour faire un bilan, les réponses aux questions sont plutôt bonnes, mais l'utilisation de Spark est plutôt approximative.

Les questions étaient : 

1. For each country, calculate the mean number of confirmed cases daily for each month in the
dataset.

2. For each continent, calculate the mean, standard deviation, minimum and maximum of the
number of confirmed cases daily for each week. When calculating the statistics, consider only
the 100 states most affected by the pandemic. If the state is not indicated, consider the country.
To determine the most affected states in the entire dataset, consider the trend of the daily
increases of confirmed cases through the trendline coefficient. To estimate it, calculate the
slope of the regression line that approximates the trend of the daily increments.
Observe that the continent to which each state/country belongs is not explicitly indicated in
the dataset, but has to be identified. To this end, consider 6 continents: Africa, America,
Antarctica, Asia, Europe, Oceania.

3. Considering the 50 most affected states calculated on a monthly basis according to the
trendline coefficient, for each month in the dataset, apply the clustering algorithm K-means
[1, 2] with K= 4. Determine the states (or nations) that are part of each cluster. Each cluster
should group the states that have a similar pattern of daily increases in confirmed cases.
Optional: For the clustering algorithm K-means, compare the performance of a naive
implementation of the algorithm and the implementation provided by the Spark MLlib or
Apache Mahout [3] library.