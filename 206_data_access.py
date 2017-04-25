###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import re
import random
import omdb
import requests

# Begin filling in instructions....

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE



### Setting up for gathering data
CACHE_FNAME = "SI206_final_project_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}



######## SETTING UP DB TABLES
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

# table Tweets, with columns:
# - tweet_id (containing the string id belonging to the Tweet itself, from the data you got from Twitter -- note the id_str attribute) -- this column should be the PRIMARY KEY of this table
# - text (containing the text of the Tweet)
# - user_id (an ID string, referencing the Users table, see below)
# - time_posted (the time at which the tweet was created)
# - retweets (containing the integer representing the number of times the tweet has been retweeted)

cur.execute('DROP TABLE IF EXISTS Tweets')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id TEXT PRIMARY_KEY, tweet_text TEXT, user_id TEXT, movie_id TEXT, favs INTEGER, retweets INTEGER)'
cur.execute(statement)

# table Users, with columns:
# - user_id (containing the string id belonging to the user, from twitter data -- note the id_str attribute) -- this column should be the PRIMARY KEY of this table
# - screen_name (containing the screen name of the user on Twitter)
# - num_favs (containing the number of tweets that user has favorited)
# - description (text containing the description of that user on Twitter, e.g. "Lecturer IV at UMSI focusing on programming" or "I tweet about a lot of things" or "Software engineer, librarian, lover of dogs..." -- whatever it is. OK if an empty string)
cur.execute('DROP TABLE IF EXISTS Users')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Users (user_id TEXT PRIMARY_KEY, screen_name TEXT, description TEXT, num_favs INTEGER, num_followers INTEGER)'
cur.execute(statement)

# table Movies, with columns:
# - imdb id (primary key)
# - title (string)
# - director (string)
# - actors (string)
# - revenue (string)
# - num_of_language (int)
# - year (string)
# - rating (string)

cur.execute('DROP TABLE IF EXISTS Movies')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Movies (imdb_id STRING PRIMARY_KEY, title TEXT, director TEXT, rating TEXT, actors TEXT, year INTEGER, revenue TEXT, num_of_language INTEGER)'
cur.execute(statement)




## Task 1: Dealing with movies

# write a list of movies
# movie_list = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "Schindler's List", "Pulp Fiction", "The Lord of the Rings: The Return of the King", "The Good, the Bad and the Ugly", "Fight Club", "Forrest Gump", "Inception", "One Flew Over the Cuckoo's Nest"]
movie_list = ["La La Land", "Moonlight", "Jackie", "Manchester by the Sea", "Rogue One", "Zootopia", "Captain America: Civil War", "Suicide Squad", "Nocturnal Animals", "Fantastic Beasts and Where to Find Them"]

# write a function to search for a movie and store them into the json file

def search_movie(movie):
	unique_identifier = "omdb_{}".format(movie) 
	if unique_identifier in CACHE_DICTION: # if it is...
		print('using cached data for', movie)
		pass
	else:
		print('getting data from internet for', movie)
		param_dict = {}
		param_dict['t'] = movie
		response = requests.get("http://www.omdbapi.com/?", params = param_dict) # get it from the internet
		omdb_dict = json.loads(response.text)
		CACHE_DICTION[unique_identifier] = omdb_dict
		# but also, save in the dictionary to cache it
		
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return CACHE_DICTION[unique_identifier]

# write a for loop to search the list of movies seperately and store the search result into a list

# beautiful = search_movie("A Beautiful Mind")
# print(beautiful['imdbRating'])
# print(type(beautiful['imdbRating']))
# print(beautiful['BoxOffice'])
# print(type(beautiful['BoxOffice']))
# print(beautiful['Year'])
# print(type(beautiful['Year']))
# print(type(beautiful['imdbID']))

movie_results = []
for movie in movie_list:
	movie_results.append(search_movie(movie))


# from each item in the list (meaning each movie), select the items that you want and make them into a dictionary (a movie's essentials)
# start a list and store the dictionaries into the list

list_of_movie_dic = []
for m in movie_results:
	# start a dictionary to store the movie essentials
	movie_dic = {}
	movie_dic['imdb_id'] = m['imdbID']
	movie_dic['title'] = m['Title']
	movie_dic['imdb_rating'] = m['imdbRating']
	movie_dic['actors'] = m['Actors']
	movie_dic['revenue'] = m["BoxOffice"]
	movie_dic['num_of_languages'] = (m['Language'].count(',') + 1)
	movie_dic['year'] = int(m['Year'])
	movie_dic['director'] = m['Director']

	list_of_movie_dic.append(movie_dic)




# CONSTRUCT A MOVIE CLASS
class Movie(object):
	def __init__(self, movie = {}):
		self.imdb_id = movie['imdb_id']
		self.title = movie['title']
		self.director = movie['director']
		self.rating = movie['imdb_rating']
		self.release_year = movie['year']
		self.actors = movie['actors'] 
		self.num_of_lan = movie['num_of_languages']
		self.revenue = movie['revenue']

	def __str__(self):
		return "Title: {}, Director: {}, imdb id: {}, rating: {}, release year: {}, actors: {}, number of languages: {}, revenue: {}".format(self.title,self.director,self.imdb_id,self.rating,self.release_year,self.actors,self.num_of_lan,self.revenue)

	def movie_tuple(self):
		return (self.imdb_id,self.title,self.director,self.rating,self.actors,self.release_year,self.revenue,self.num_of_lan)

# CONSTRUCT A LIST OF MOVIE OBJECTS
movie_tuple_list = []
movie_object_list = []
for m in list_of_movie_dic:
	movie_object_list.append(Movie(m))
	movie_tuple_list.append(Movie(m).movie_tuple())


# insert the movie tuple list into the movies table
movie_table = 'INSERT OR IGNORE INTO Movies VALUES (?,?,?,?,?,?,?,?)'
for u in movie_tuple_list:
	cur.execute(movie_table, u)
conn.commit()


# Write a function to get tweets from twitter
def get_tweets(phrase):
	unique_identifier = "twitter_{}".format(phrase) 
	if unique_identifier in CACHE_DICTION: # if it is...
		print('using cached data for', phrase)
		pass
	else:
		print('getting data from internet for', phrase)
		twitter_results = api.search(q=phrase, lang = "en", count = 100, result_type = "popular") # get it from the internet
		CACHE_DICTION[unique_identifier] = twitter_results
		# but also, save in the dictionary to cache it
		
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return CACHE_DICTION[unique_identifier]




# getting tweets about the movie
# getting the user list

tweet_list = []
user_list = []
for movie in movie_object_list:
	title = movie.title
	movie_id = movie.imdb_id
	tweet_search_result = get_tweets(title) #this is a list of tweets about the movie
	for t in tweet_search_result['statuses']:
		# for building a tweet dictionary
		if "RT @" not in t['text']:
			tweet = {}
			tweet['movie_id'] = movie_id
			tweet['tweet_id'] = t['id']
			tweet['tweet_text'] = t['text']
			tweet['user_id'] = t['user']['id_str']
			tweet['num_retweets'] = t['retweet_count']
			tweet['num_favs'] = t['favorite_count']
			# append the tweet to the tweet list
			tweet_list.append(tweet)

			# for building a user dictionary
			if len(t['entities']['user_mentions']) >= 1:
				for i in t['entities']['user_mentions']:
					if i['id_str'] not in user_list:
						user_list.append(i['id_str'])
			if t['user']['id_str'] not in user_list:
				user_list.append(t['user']['id_str'])




# Construct a tweet class
# parameters: 
# - tweet id
# - movie reference (imdb id)
# - tweet text
# - author's user id
# - num of favs
# - num of retweets

class Tweet(object):
	def __init__(self, tweet = {}):
		self.tweet_id = tweet['tweet_id']
		self.tweet_text = tweet['tweet_text']
		self.user_id = tweet['user_id']
		self.movie_id = tweet['movie_id']
		self.num_favorite = tweet['num_favs']
		self.num_retweets = tweet['num_retweets']

	def tweet_tuple(self):
		return (self.tweet_id, self.tweet_text, self.user_id, self.movie_id, self.num_favorite, self.num_retweets)

# make a list of tweet tuples
tweet_tuple_list = []
for t in tweet_list:
	tweet_tuple_list.append(Tweet(t).tweet_tuple())

tweet_table = 'INSERT OR IGNORE INTO Tweets VALUES (?,?,?,?,?,?)'
for u in tweet_tuple_list:
	cur.execute(tweet_table, u)
conn.commit()



def get_user_info(id):
	unique_identifier = "user_{}".format(id) 
	if unique_identifier in CACHE_DICTION: # if it is...
		print('using cached data for user id ', id)
		pass
	else:
		print('getting data from internet for user id ', id)
		user_results = api.get_user(id) # get it from the internet
		CACHE_DICTION[unique_identifier] = user_results
		# but also, save in the dictionary to cache it
		
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return CACHE_DICTION[unique_identifier]



# construct a list of user info
users = []
for u in user_list:
	user = {}
	user_object = get_user_info(u)
	user['user_id'] = u
	user['screen_name'] = user_object['screen_name']
	user['description'] = user_object['description']
	user['num_favs'] = user_object['favourites_count']
	user['num_followers'] = user_object['followers_count']
	users.append(user)



# Construct a tweetuser class
# parameters:
# - a user id
# the object has:
# - user id
# - user screen name
# - num of favs
# - description
# - num of followers

class TweetUser(object):
	def __init__(self, user = {}):
		self.user_id = user['user_id']
		self.screen_name = user['screen_name']
		self.description = user['description']
		self.num_favs = user['num_favs']
		self.num_followers = user['num_followers']

	def user_tuple(self):
		return (self.user_id, self.screen_name, self.description, self.num_favs, self.num_followers)

# use the user dictionary list to construct a list of user objects

user_tuple_list = []
for u in users:
	user_tuple_list.append(TweetUser(u).user_tuple())


user_table = 'INSERT OR IGNORE INTO Users VALUES (?,?,?,?,?)'
for u in user_tuple_list:
	cur.execute(user_table, u)
conn.commit()

print ("------------- END OF DATA SET UP ---------------------")
print ("\n\n")

#########################################################################################
# SETTING UP QUERIES
# 1. To pick movies that have rating over or equal to 8.0
q1 = 'SELECT title FROM Movies WHERE rating >= "8.0"'
cur.execute(q1)
movie_names = cur.fetchall()
movie_rating_over_8 = []
for i in movie_names:
	movie_rating_over_8.append(i[0])

# 2. To pick movies that have revenue over 100M
q2 = 'SELECT title FROM Movies WHERE revenue >= "$100,000,000.00"'
cur.execute(q2)
results = cur.fetchall()
movies_revenue_over_100m = []
for i in results:
	movies_revenue_over_100m.append(i[0])

# 3. To pick tweets with over 500 retweets for movies with a revenue over 100M



# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class test_movie_list(unittest.TestCase):
	def test_movie_list(self):
		self.assertEqual(type(movie_list), list)
	def test_movie_list_type(self):
		self.assertEqual(type(movie_list[0]), str)
	def test_movie_list_length(self):
		self.assertTrue(len(movie_list) >= 3)

	def test_movie_dic_list(self):
		self.assertEqual(type(list_of_movie_dic), list)
	def test_movie_dic_list_type(self):
		self.assertEqual(type(list_of_movie_dic[0]), dict)
	def test_movie_dic_list_length(self):
		self.assertTrue(len(list_of_movie_dic) >= 3)


class testMovie(unittest.TestCase):
	def test_movie_constructor(self):
		m = search_movie("The Dark Knight")
		movie_dic = {}
		movie_dic['imdb_id'] = m['imdbID']
		movie_dic['title'] = m['Title']
		movie_dic['imdb_rating'] = m['imdbRating']
		movie_dic['actors'] = m['Actors']
		movie_dic['revenue'] = m["BoxOffice"]
		movie_dic['num_of_languages'] = (m['Language'].count(',') + 1)
		movie_dic['year'] = int(m['Year'])
		movie_dic['director'] = m['Director']

		movie1 = Movie(movie_dic)
		self.assertEqual(movie1.title, "The Dark Knight")
		self.assertEqual(movie1.actors, "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine")
		self.assertEqual(movie1.num_of_lan, 2)
		self.assertEqual(movie1.imdb_id, "tt0468569")
		self.assertEqual(movie1.revenue, "$533,316,061.00")
		self.assertEqual(movie1.release_year, 2008)

	def test_movie_tuple(self):
		m = search_movie("The Dark Knight")
		movie_dic = {}
		movie_dic['imdb_id'] = m['imdbID']
		movie_dic['title'] = m['Title']
		movie_dic['imdb_rating'] = m['imdbRating']
		movie_dic['actors'] = m['Actors']
		movie_dic['revenue'] = m["BoxOffice"]
		movie_dic['num_of_languages'] = (m['Language'].count(',') + 1)
		movie_dic['year'] = int(m['Year'])
		movie_dic['director'] = m['Director']
		self.assertEqual(Movie(movie_dic).movie_tuple(), ('tt0468569', 'The Dark Knight', 'Christopher Nolan', '9.0', 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine', 2008, '$533,316,061.00', 2))

	def test_movie_cache(self):
		project_cache = open("SI206_final_project_cache.json","r").read()
		self.assertTrue("The Dark Knight" in project_cache)

	

class testMovieDB(unittest.TestCase):
	def test_movie_table1(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result)>=3, "Testing there are at least 3 movies in the Movies database")
		conn.close()

	def test_movie_table2(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[1])== 8, "Testing there are 8 columns in the Movies database")
		conn.close()

class testTweetsDB(unittest.TestCase):
	def test_tweet_table1(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing there are at least 20 records in the Tweets database")
		conn.close()

	def test_tweet_table2(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==6,"Testing that there are 5 columns in the Tweets table")
		conn.close()


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
# unittest.main(verbosity=2) 