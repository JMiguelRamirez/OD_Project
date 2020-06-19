# OD_Project: Movie Recommender

## Pre-requisites

The following software is necessary:

<table> <tr><th>Software</th><th>Version</th></tr><tr><td>python</td><td>3.6.5</td></tr></tr><tr><td>Neo4j</td><td>3.5.14</td></tr></tr></table>

The input data has been obtained from two different sources: <table><tr><th>Source</th><th>Version</th></tr><tr><td>[Netflix Shows](https://www.kaggle.com/shivamb/netflix-shows/version/2)</td><td>2</td></tr><tr><td>[User Ratings](https://www.kaggle.com/netflix-inc/netflix-prize-data?select=movie_titles.csv)</td><td>2</td></tr></table>

## Pre-processing

By executing this piece of code in the directory containing the input data, we will pre-process the raw data to obtain the files already placed in [preprocessed_data](preprocessed_data).
```
python prep.py
```
## Loading

With the folowing script we will build a property graph by loading our pre-processed data in an running database of Neo4j. Pre-processed data must be in the *import* folder of the database. Building the database takes 5 minutes.
```
python Make_graph.py
```
## Proof of concept (POC): Graph Exploitation

Finally, with the following command, we can run our proof of concept.
```
python poc.py
```
### Preview of the POC

The program has few options where you can choose:
- Your user ID. It can be a random user of the database or you can choose an existing user.
![alt text](https://github.com/JMiguelRamirez/OD_Project/blob/master/fig/Choose_user.png?raw=true)
- Take a look at a random sample of 50 movies from the database.
![alt text](https://github.com/JMiguelRamirez/OD_Project/blob/master/fig/list_movies.png?raw=true)
- A recommendation based on a movie. Based in the movie that you have typed.
![alt text](https://github.com/JMiguelRamirez/OD_Project/blob/master/fig/rec_show.png?raw=true)
- A recommendation based on your profile. It is based in your user ID.
![alt text](https://github.com/JMiguelRamirez/OD_Project/blob/master/fig/rec_hist.png?raw=true)

- And you can watch a movie and rate it. This rating will be added to the property graph for improving next recommendations
![alt text](https://github.com/JMiguelRamirez/OD_Project/blob/master/fig/watching_movie.png?raw=true)


## Authors
Sergi Aguiló & José Miguel Ramírez
