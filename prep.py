import csv
import re
import random

def write_genre(full_genres,movie_id,out_genre, out_only_genre):
    list_genres = full_genres.split(",")
    global dict_genre
    for genre in list_genres:
        if len(genre) < 1:
            continue
        if genre[0] == " ":
            genre = genre[1:]
        if genre not in dict_genre:
            dict_genre[genre] = 0
            out_only_genre.write(f"{genre}\n")
            out_genre.write(f"{genre}\t{movie_id}\n")
        else:
            out_genre.write(f"{genre}\t{movie_id}\n")


def main_movie(list_movies,netflix_nov, movies_titles,out_movie_info, out_genre, out_only_genre):
    for netflix_movie in csv.reader(netflix_nov, quotechar='"', delimiter=',',
    quoting=csv.QUOTE_ALL, skipinitialspace=True):
        movies_titles.seek(0)
        for j in movies_titles:
            titles = j.strip().split(",")
            if titles[2] == netflix_movie[1]:
                list_movies[titles[0]] = [netflix_movie[3], netflix_movie[2]] # actor and director
                duration = re.findall("\d+", netflix_movie[8])[0]
                out_movie_info.write(f"{titles[0]}\t{titles[2]}\t{titles[1]}\t"
                                     f"{netflix_movie[5]}\t{netflix_movie[7]}\t"
                                     f"{duration}\t{netflix_movie[11]}\n")
                #Write genre
                write_genre(netflix_movie[9], titles[0], out_genre, out_only_genre)

def create_user(combine_data_1, combine_data_2,
                combine_data_3, combine_data_4, out_user, out_only_user):
    global list_movies
    current_ID = ""
    dict_users ={}
    for i in combine_data_1:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.01:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    for i in combine_data_2:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.01:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    for i in combine_data_3:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.01:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")
    for i in combine_data_4:
        movie_rating=i.strip().split(",")
        if len(movie_rating) == 1:
            IsAvailable = False
            current_ID = movie_rating[0][:-1]
            if list_movies.get(current_ID):
                IsAvailable = True
        elif IsAvailable == True:
            if random.random() < 0.01:
                if movie_rating[0] not in dict_users:
                    dict_users[movie_rating[0]] = 1
                    out_only_user.write(f"{movie_rating[0]}\n")
                out_user.write(f"{movie_rating[0]}\t{current_ID}\t{movie_rating[1]}\n")

def create_actor_director(out_director, out_actor, out_only_director, out_only_actor):
    global list_movies
    dic_Actor = {}
    id_Actor = 0
    dic_Director = {}
    id_director = 0
    for movie_id in list_movies:
        list_actor_director = list_movies[movie_id]
        actors = list_actor_director[0].split(",")
        directors = list_actor_director[1].split(",")
        for actor in actors:
            if len(actor) < 1:
                continue
            if actor[0] == " ":
                actor = actor[1:]
            if actor not in dic_Actor:
                id_Actor += 1
                dic_Actor[actor] = "A_" + str(id_Actor)
                out_only_actor.write(f"{actor}\n")
                out_actor.write(f"{actor}\t{movie_id}\n")
            else:
                out_actor.write(f"{actor}\t{movie_id}\n")
        for director in directors:
            if len(director) < 1:
                continue
            if director[0] == " ":
                director = director[1:]
            if director not in dic_Director:
                id_director += 1
                dic_Director[director] = "D_" + str(id_director)
                out_only_director.write(f"{director}\n")
                out_director.write(f"{director}\t{movie_id}\n")
            else:
                out_director.write(f"{director}\t{movie_id}\n")

netflix_nov = open("netflix_titles_nov_2019.csv", 'r')
movies_titles = open("netflix-prize-data/movie_titles.csv", 'r', encoding = "ISO-8859-1", errors="ignore")
combine_data_1 = open("netflix-prize-data/combined_data_1.txt", 'r')
combine_data_2 = open("netflix-prize-data/combined_data_2.txt", 'r')
combine_data_3 = open("netflix-prize-data/combined_data_3.txt", 'r')
combine_data_4 = open("netflix-prize-data/combined_data_4.txt", 'r')
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

list_movies = {}
dict_genre = {}

if __name__ == '__main__':
    main_movie(list_movies, netflix_nov, movies_titles, out_movie,
               out_genre, out_only_genre)
    create_user(combine_data_1, combine_data_2,
                combine_data_3, combine_data_1, out_user, out_only_user)
    create_actor_director(out_director, out_actor, out_only_director, out_only_actor)