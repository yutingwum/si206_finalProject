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

## Task 1: Dealing with movies

# write a list of movies
movie_list = ["Love Actually", "The Conjuring", "American Beauty"]

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
	movie_dic['year'] = m['Year']
	movie_dic['driector'] = m['Director']

	list_of_movie_dic.append(movie_dic)



def get_tweets(phrase):
	unique_identifier = "twitter_{}".format(phrase) 
	if unique_identifier in CACHE_DICTION: # if it is...
		print('using cached data for', phrase)
		pass
	else:
		print('getting data from internet for', phrase)
		twitter_results = api.search(q=phrase) # get it from the internet
		CACHE_DICTION[unique_identifier] = twitter_results
		# but also, save in the dictionary to cache it
		
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	return CACHE_DICTION[unique_identifier]

movie_tweets = []
for m in movie_list:
	movie_tweets.append(get_tweets(m))

print(len(movie_tweets))
print(type(movie_tweets))
print(type(movie_tweets[0]))
print(type(movie_tweets[0]['statuses']))
print(len(movie_tweets[0]['statuses']))
print(movie_tweets[0]['statuses'][1]['entities']['user_mentions'])

user_id = []
screen_name = []
num_favs = []
description []

for m in movie_tweets: # m is a dictionary from tweets of a movie
	for t in m['statuses']: # statuses contain lists of tweets
		if len(t['entities']['user_mentions']) >= 1:
			for i in t['entities']['user_mentions']:
				if i['id_str'] not in user_id:
					user_id.append(i['id_str'])
					name = i['screen_name'].lower()
					screen_name.append(name)
		if t['user']['id_str'] not in user_id:
			user_id.append(t['user']['id_str'])
			screen_name.append(t['user']['screen_name'])


			# print("-------- PRINT SCREEN NAME --------")
			# print(type(i['user']['screen_name']))
			# print(i['user']['screen_name'])
			# user_screenname_list.append(i['user']['screen_name']) 
			# if len(i['entities']['use_mentions']) >= 1: # check if there is any user mention
			# 	for j in i['entities']['use_mentions']: # j is a certain user mentioned in the tweet
			# 		user_screenname_list.append(j['screen_name'])


for n in screen_name:
	user_object = api.get_user(n)
	num_favs.append(user_object['favourites_count'])
	description.append(user_object['description'])



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
statement += 'Tweets (tweet_id TEXT PRIMARY_KEY, tweet_text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER)'
cur.execute(statement)

# table Users, with columns:
# - user_id (containing the string id belonging to the user, from twitter data -- note the id_str attribute) -- this column should be the PRIMARY KEY of this table
# - screen_name (containing the screen name of the user on Twitter)
# - num_favs (containing the number of tweets that user has favorited)
# - description (text containing the description of that user on Twitter, e.g. "Lecturer IV at UMSI focusing on programming" or "I tweet about a lot of things" or "Software engineer, librarian, lover of dogs..." -- whatever it is. OK if an empty string)
cur.execute('DROP TABLE IF EXISTS Users')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Users (user_id INTEGER PRIMARY_KEY, screen_name TEXT, num_favs INTEGER, description TEXT)'
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
statement = 'CREATE TABLE IF NOT EXISTS'
statement += 'Movies (imdb_id INTEGER PRIMARY_KEY, title TEXT, director TEXT, actors TEXT, revenue TEXT, num_of_language INTEGER, year TEXT, rating string)'
cur.execute(statement)

# def get_user_tweets(user_handle):
# 	unique_identifier = "twitter_{}".format(user_handle) 
# 	if unique_identifier in CACHE_DICTION: # if it is...
# 		print('using cached data for', user_handle)
# 		pass
# 	else:
# 		print('getting data from internet for', user_handle)
# 		twitter_results = api.user_timeline(user_handle) # get it from the internet
# 		CACHE_DICTION[unique_identifier] = twitter_results
# 		# but also, save in the dictionary to cache it
		
# 		f = open(CACHE_FNAME,'w') # open the cache file for writing
# 		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
# 		f.close()

# 	return CACHE_DICTION[unique_identifier]








# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)