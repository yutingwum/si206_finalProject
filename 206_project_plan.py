## Your name: Yuting Wu
## The option you've chosen: 2

# Put import statements you expect to need here!
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


# construct a Movie class
# # imdb id, title, director, idmb rating, list of actors, num of languages
# class Movie(object):
# 	def __init__(self, search_term = " "):

movie = omdb.search("Big Little Lies")
print (movie)
# fetch data from Twitter and store it in a josn file


# fetch data from 














# Write your test cases here.

# class testMovie(unittest.TestCase):
# 	def test_movie_constructor(self):
# 		movie1 = Movie("Big little lies")
# 		self.assertEqual(movie1.title, "Big Little Lies")
# 		self.assertEqual(movie1.actors, "Reese Witherspoon, Nicole Kidman, Shailene Woodley, Alexander Skarsgård")
# 		self.assertEqual(movie1.num_of_lan, 1)
# 		self.assertEqual(movie1.imdb_id, "tt3920596")

# 	def test_movie_tuple(self):
# 		self.assertEqual(Movie("Big Little Lies").get_movie(), ("tt3920596", "Big Little Lies", "N/A", "8.5", "Reese Witherspoon, Nicole Kidman, Shailene Woodley, Alexander Skarsgård", 1))

# 	def test_movie_compare(Movie("True Grit")):
# 		movie1 = Movie("Big little lies")
# 		self.assertEqual(movie.compare(Movie("True Grit")), "Big Little Lies")


# class testTwitter(unittest.TestCase):




## Remember to invoke all your tests...