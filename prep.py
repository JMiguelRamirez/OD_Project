import csv
import re
import random

def write_genre(full_genres,movie_id,out_genre, out_only_genre):
    list_genres = full_genres.split(",") # For each list of genres
    global dict_genre
    for genre in list_genres:
        if len(genre) < 1: # Look if there is any Gender in the list
            continue
        if genre[0] == " ": # Remove the blank space after a comma
            genre = genre[1:]
        if genre not in dict_genre: # Every time we found a new Genre:
            dict_genre[genre] = 0   # Store it to the dict to avoid replications in the nodes

            # Write the Genre information
            out_only_genre.write(f"{genre}\n") # Unique Genres
            out_genre.write(f"{genre}\t{movie_id}\n") # Relation between Genre and Movie
        else:
            out_genre.write(f"{genre}\t{movie_id}\n")


def main_movie(list_movies,netflix_nov, movies_titles,out_movie_info, out_genre, out_only_genre):
    d_title ={} # Dictionary avoid replicated movies
    for netflix_movie in csv.reader(netflix_nov, quotechar='"', delimiter=',',
    quoting=csv.QUOTE_ALL, skipinitialspace=True): # Each line is a list (comma separated and considering the quotation marks)
        movies_titles.seek(0) # movie_titles is readed multiple times. Every time we start a new for loop, we need to start from the beggining
        for j in movies_titles:
            titles = j.strip().split(",")
            if titles[2] == netflix_movie[1]: # If both datasets have the same title, we accept the movie
                if titles[2] in d_title: # If the movie it is alreade in the dataset, we do not store it
                    continue
                d_title[titles[2]] = 1
                list_movies[titles[0]] = [netflix_movie[3], netflix_movie[2]] # Store actors and directors list
                duration = re.findall("\d+", netflix_movie[8])[0] # We assure that the Minutes are integers

                # Write the Movie node information
                out_movie_info.write(f"{titles[0]}\t{titles[2]}\t{titles[1]}\t"
                                     f"{netflix_movie[5]}\t{netflix_movie[7]}\t"
                                     f"{duration}\t{netflix_movie[11]}\n")
                # Function for writing Genre node
                write_genre(netflix_movie[9], titles[0], out_genre, out_only_genre)


def create_user(combine_data_1, combine_data_2,
                combine_data_3, combine_data_4, out_user, out_only_user):
    global list_movies
    current_ID = ""
    dict_users ={} # Avoid replicated users
    # File 1
    for i in combine_data_1:
        movie_rating=i.strip().split(",")
        # Retrive ID of the movie
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1] # Remove the ":" character
            if list_movies.get(current_ID): # Check if movie is common in both datasets
                IsAvailable = True
        # Retrive user - movie rating
        elif IsAvailable == True:
            if random.random() < 0.005: # As the file being so big, we reduce the number of ratings
                if movie_rating[0] not in dict_users: # For unique users
                    dict_users[movie_rating[0]] = 1
                    # Write unique users
                    out_only_user.write(f"{movie_rating[0]}\n")
                # Write users rating a movie
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    # File 2
    for i in combine_data_2:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.005:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    # File 3
    for i in combine_data_3:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.005:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    # File 4
    for i in combine_data_4:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.005:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")

def create_actor_director(out_director, out_actor, out_only_director, out_only_actor):
    global list_movies
    dic_Actor = {} # For avoiding replicated Actor nodes
    id_Actor = 0
    dic_Director = {} # For avoiding replicated Actor nodes
    id_director = 0
    for movie_id in list_movies:
        list_actor_director = list_movies[movie_id] # Extract the actors and directors of each movie
        actors = list_actor_director[0].split(",")
        directors = list_actor_director[1].split(",")

        # Extract the actors
        for actor in actors:
            if len(actor) < 1: # If actor found
                continue
            if actor[0] == " ": # Remove blank space after the comma
                actor = actor[1:]
            if actor not in dic_Actor: # Avoid replicated actors
                id_Actor += 1
                dic_Actor[actor] = "A_" + str(id_Actor)
                # Write unique actors and relations between actors and movies
                out_only_actor.write(f"{actor}\n")
                out_actor.write(f"{actor}\t{movie_id}\n")
            else:
                out_actor.write(f"{actor}\t{movie_id}\n")
        # Extract the directors
        for director in directors:
            if len(director) < 1: # If director found
                continue
            if director[0] == " ": # Remove blank space after the comma
                director = director[1:]
            if director not in dic_Director: # Avoid replicated directors
                id_director += 1
                dic_Director[director] = "D_" + str(id_director)
                # Write unique directors and relations between directors and movies
                out_only_director.write(f"{director}\n")
                out_director.write(f"{director}\t{movie_id}\n")
            else:
                out_director.write(f"{director}\t{movie_id}\n")

# Files that we need to read
## First dataset, information of the movies
netflix_nov = open("netflix_titles_nov_2019.csv", 'r')

## Secon dataset, rating of the movies
### File with the ID of the movie and the title
movies_titles = open("netflix-prize-data/movie_titles.csv", 'r', encoding = "ISO-8859-1", errors="ignore")
### Files storing the rating from one user to a movie
combine_data_1 = open("netflix-prize-data/combined_data_1.txt", 'r')
combine_data_2 = open("netflix-prize-data/combined_data_2.txt", 'r')
combine_data_3 = open("netflix-prize-data/combined_data_3.txt", 'r')
combine_data_4 = open("netflix-prize-data/combined_data_4.txt", 'r')

# Output files and header of each output
out_movie = open("out_movie","w")
out_movie.write("MovieID\tTitle\tYear\tReleaseDate\tRating\tMinutes\tType\n")
out_genre = open("out_genre", "w")
out_genre.write("Genre\tMovieID\n")
out_only_genre = open("out_only_genre", "w")
out_only_genre.write("Genre\n")
out_user = open("out_user","w")
out_user.write("UserID\tMovieID\tRating\n")
out_only_user = open("out_only_user","w")
out_only_user.write("UserID\n")
out_director = open("out_director","w")
out_director.write("Director\tMovieID\n")
out_only_director = open("out_only_director","w")
out_only_director.write("Director\n")
out_actor = open("out_actor","w")
out_actor.write("Actor\tMovieID\n")
out_only_actor = open("out_only_actor","w")
out_only_actor.write("Actor\n")

# Dictionaries used in the functions
list_movies = {} # This is used for storing information of the actors and directors of each movie
dict_genre = {} # This is used for storing the genre/s of each movie

if __name__ == '__main__':
    # Function to retrieve the Movie node and consequently the genres
    main_movie(list_movies, netflix_nov, movies_titles, out_movie,
               out_genre, out_only_genre)
    # Function to User node with the ratings
    create_user(combine_data_1, combine_data_2,
                combine_data_3, combine_data_1, out_user, out_only_user)
    # Extract actors and directors
    create_actor_director(out_director, out_actor, out_only_director, out_only_actor)
