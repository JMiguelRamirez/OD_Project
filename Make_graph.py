from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))

def generate_graph():
	with driver.session() as session:
		session.run("""MATCH ()-[r]->() DELETE r""")
		session.run("""MATCH (r) DELETE r""")
	# Movie node
	print("Creating Movie nodes")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_movie" AS csv FIELDTERMINATOR '\t'
			CREATE (:Movie {id:csv.MovieID, title:csv.Title, year:csv.Year,
			releasedate:csv.ReleaseDate, tvrating:csv.Rating, minutes:toInteger(csv.Minutes),
			 type:csv.Type})
			""")
	except:
		print("----> Error creating Movie nodes")
	# User node
	print("Creating User nodes")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_only_user" AS csv
			CREATE (user:User {userID:csv.UserID})
		 """)
	except:
		print("----> Error creating User nodes")
	# :RATES edge
	print("Creating User-Movie edge")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_user" AS csv FIELDTERMINATOR '\t'
			MATCH (m:Movie {id:csv.MovieID}), (user:User {userID:csv.UserID})
			CREATE (user) -[:RATES {rating:toInteger(csv.Rating)}] -> (m)
		 """)
	except:
		print("----> Error creating User-Movie edge")
	# Director node
	print("Creating Director nodes")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_only_director" AS csv
			CREATE (director:Director {name:csv.Director})
			""")
	except:
		print("----> Error creating Director nodes")
	# :DIRECTS edge
	print("Creating Director-Movie edge")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_director" AS csv FIELDTERMINATOR '\t'
			MATCH (mov:Movie {id:csv.MovieID}),(director:Director {name:csv.Director})
			CREATE (director) -[:DIRECTS]-> (mov)
			""")
	except:
		print("----> Error creating Director-Movie edge")
	# Actor node
	print("Creating Actor nodes")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_only_actor" AS csv
			CREATE (actor:Actor {name:csv.Actor})
			 """)
	except:
		print("----> Error creating Actor nodes")
	# :ACTS edge
	print("Creating Actor-Movie edge")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_actor" AS csv FIELDTERMINATOR '\t'
			MATCH (mov:Movie {id:csv.MovieID}), (actor:Actor {name:csv.Actor})
			CREATE (actor) -[:ACTS]-> (mov)
			 """)
	except:
		print("----> Error creating Actor-Movie edge")
	# Genre node
	print("Creating Genre nodes")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_only_genre" AS csv
			CREATE (genre:Genre {name:csv.Genre})
			 """)
	except:
		print("----> Error creating Actor nodes")
	# :LISTED_IN edge
	print("Creating Movie-Genre edge")
	try:
		session.run("""
			LOAD CSV WITH HEADERS FROM "file:///out_genre" AS csv FIELDTERMINATOR '\t'
			MATCH (mov:Movie {id:csv.MovieID}), (genre:Genre {name:csv.Genre})
			CREATE (mov) -[:LISTED_IN]-> (genre)
			 """)
	except:
		print("----> Error creating Movie-Genre edge")


if __name__ == '__main__':
    generate_graph()

