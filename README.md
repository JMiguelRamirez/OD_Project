# OD_Project: Movie Recommender

## Pre-requisites

The following software is necessary:

<table> <tr><th>Software</th><th>Version</th></tr><tr><td>python</td><td>3.6.5</td></tr></tr><tr><td>Neo4j</td><td>3.5.14</td></tr></tr></table>

The input data has been obtained from two different sources: <table><tr><th>Source</th><th>Version</th></tr><tr><td>[Netflix Shows](https://www.kaggle.com/shivamb/netflix-shows/version/2)</td><td>2</td></tr><tr><td>[User Ratings](https://www.kaggle.com/netflix-inc/netflix-prize-data?select=movie_titles.csv)</td><td>2</td></tr></table>

## Pre-processing

Executing this peace of code in the directory containing the input data, we will pre-process the raw data to create the files already placed in [preprocessed_data](preprocessed_data).
```
python prep.py
```
## Loading

With the folowing script we will build a property graph by loading our pre-processed data.
```
python Make_graph.py
```
## Exploitation
