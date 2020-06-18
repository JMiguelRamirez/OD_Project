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

With the folowing script we will build a property graph by loading our pre-processed data in an running database of Neo4j. Script and pre-processed data must be in the same folder.
```
python Make_graph.py
```
## Proof of concept

With the following command, we will show you our proof of concept.
```
python poc.py
```
### Explanation of the proof of concept

The program is simple, it has few options where you can choose:
- Your user ID
- Look at a random sample of 50 movies that you have in the database.
- A recommendation based on a movie.
- Recommendation based on you profile.

Alternatively, you also can watch a movie and rate it. This rate will be added to the property graph.
