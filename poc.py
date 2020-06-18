from neo4j import GraphDatabase
import sys
import time
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))

def assignuser(userid):
	if userid == "0": # Assign random number
		with driver.session() as session:
			final_node = session.run("""
				MATCH (a:User)
				RETURN a.userID, rand() as r
				ORDER BY r
				LIMIT 1
			""")
			for i in final_node:
				user = i['a.userID']
				print("Your user ID will be:", user)
				break
			return user
	else: # Look if user ID exists
		with driver.session() as session:
			final_node = session.run('MATCH (a:User {userID:"' + userid + '"}) RETURN a.userID')
			if final_node:
				for i in final_node:
					user = i['a.userID']
					if len(user) >0:
						print("User ID", user, "is available")
						return user
			# If user is wrong, repeat again
			print("Wrong user ID. Type again a correct user ID or type 0 for a random user ID")
			userid = input("Type here: ")
			assignuser(userid)

def list_movies():
	with driver.session() as session:
		final_node = session.run("""
			MATCH (m:Movie)
			RETURN m.title, rand() as rand
			ORDER BY rand
			LIMIT 50
			""")

		for i in final_node:
			show = i['m.title']
			print(show)

def recommendation_show(movie):
	with driver.session() as session:
		rec_movies = session.run('''
			MATCH (m:Movie {title: "''' + movie + '''"})-[:LISTED_IN|:ACTS|:DIRECTS]-(x)-[:LISTED_IN|:ACTS|:DIRECTS]-(m2:Movie)
			WITH m, m2, COUNT(x) AS common, COLLECT(x.name) AS common_names

			MATCH (m)-[:LISTED_IN|:ACTS|:DIRECTS]-(mx)
			WITH m, m2, common, common_names, COLLECT(mx.name) AS only_in_m

			MATCH (m2)-[:LISTED_IN|:ACTS|:DIRECTS]-(m2x)
			WITH m, m2, common, common_names, only_in_m, COLLECT(m2x.name) AS only_in_m2
			WITH m, m2, common, only_in_m+[x IN only_in_m2 WHERE NOT x IN only_in_m] AS union, only_in_m, only_in_m2
			RETURN m2.title as Recommendation, ((1.0*common)/SIZE(union)) AS Jaccard_Index ORDER BY Jaccard_Index DESC LIMIT 10
            ''')
		if rec_movies:
			print("\nThe recommended shows are:")
			for i in rec_movies:
				if i:
					print(f"{i['Recommendation']} with jaccard index of {i['Jaccard_Index']}")
			return True
		print("Show not found")
		return False
def recommendation_history(user):
	with driver.session() as session:
		rec_movies = session.run('''
			MATCH (u:User {userID: "''' + user + '''"})-[r:RATES]->(m:Movie),
			  (m)-[:LISTED_IN]->(g:Genre)<-[:LISTED_IN]-(m2:Movie)
			WHERE r.rating >= 3 AND NOT EXISTS((u)-[:RATES]->(m2))
			WITH m, m2, [g.name, COUNT(*)] AS scores
			WITH m, m2, REDUCE (x=0,s in COLLECT(scores) | x+s[1]) AS genre_score
			
			OPTIONAL MATCH (m)<-[:ACTS]-(a:Actor)-[:ACTS]->(m2)
			WITH m, m2, genre_score, COUNT(a) AS cast_score
			
			OPTIONAL MATCH (m)<-[:DIRECTS]-(a:Director)-[:DIRECTS]->(m2)
			WITH m, m2, genre_score, cast_score, COUNT(a) AS director_score
			WITH m, m2, (5*genre_score)+(cast_score)+(2*director_score) as score
			RETURN m2.title AS Recommendation, REDUCE (x=0,s in COLLECT(score) | x+s) as score
			ORDER BY score DESC LIMIT 10
            ''')
		print("\nThe recommended shows are:")
		if rec_movies:
			for i in rec_movies:
				print(f"{i['Recommendation']} with a score of {i['score']}")
			return True
		print("There are no recommendations for this user")
		return False

def watching_movie(movie_w,user):

	print("Watching")
	time.sleep(2)
	print("THE END...")
	rating = input("What is your rating for this movie (One number from 1 to 5): ")
	if int(rating) <0 or int(rating) > 5:
		print("Incorrect rating, watch the movie again")
		watching_movie(movie_w, user)
	with driver.session() as session:
		creating_rating = session.run('''
	MATCH (m:Movie {title: "''' + movie_w + '''"}), (user:User {userID: "''' + user +'''"})
	CREATE (user) -[:RATES {rating:''' + rating + '''}] -> (m)
            ''')
	print("Rating added in the graph")

def choosing(user):

	print("To see a random subset of 50 shows, type 0")
	print("Otherwise, go to the recommenders - You can type anything")
	# Show the movies
	option = input("Type here: ")

	if option == "0":
		list_movies()

	print("\n\n")
	# Select the recommender or watch a movie
	print("If you want a recommendation based on a specific show, type: 0")
	print("If you want a recommendation based on a user's history, type 1")
	print("If you want to watch a movie directly, type any other values besides 0 and 1")
	recommender = input("Type here: ")
	result = True
	if recommender == "0":
		movie = input("Show that the recommendation will be based: ")
		result = recommendation_show(movie)
	elif recommender == "1":
		result = recommendation_history(user)
	if result == False: # If no results, go at the beginning
		print("No results. Program will go at the beginning")
		choosing(user)
	movie_w = input("Name of the movie that you are going to watch: ")
	watching_movie(movie_w,user)
	# Repeat agin
	print("\n\nWhat do you want to do now?")
	choosing(user)

def main():
	# Starting the POC
	print("Welcome to the Netflix recommender!\n\n")
	print("Type your user ID (If you do not have any user ID, it will be assigned randomly by typing 0):")
	# Read the userID
	userid = input("Type here: ")
	user = assignuser(userid)
	print("\n\n")
	# Continue with the recommenders
	choosing(user)


if __name__ == '__main__':
	main()

