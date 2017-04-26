# si206_finalProject

OPTION PICKED: option 2

index:
- overview of project
- How to run the project
- Dependencies
- Other relevent files
- Class explanation
- Function explanation
- Database tables
- Data manipulation explanation
- Project motivation





Overview of Project:
This project consists of two main parts: 1. getting data from omdb (a movie online database) and twitter  2. processing and analyzing the data. To be specific, the program will send requests to omdb for information on a list of 10 movies in 2016 and store key information (such as title, director etc) into a Movies database table. Then the program will search for movie related tweets on twitter (the search term is the movie title) and select key information and store it into a Tweets database table. The program will also search for all the users who tweeted or were mentioned in the tweets and store key information of the users into a Users database table. Finally, the program will create queries to make interesting queries. It will output data analysis results





How to Run the Project:
You need to have a twitter_info.py file with your own twitter acount info and put it in the same folder as the 206_data_access.py file is in order to run this project.





Dependencies:
unittest: for unit testing
collections: for using counter when analyzing the data
tweepy: for search for tweets and users on twitter
twitter_info: necessary for using tweepy
json: to create json file
sqlite3: to make database table and make queries
omdb: to search info of the movies on omdb
requests: to make requests to omdb
math: to calculate interaction index of twitter accounts





Other relevant files:
final_project.db: database tables for movies, tweets and users
SI206_final_project_cache.json: raw data from movie search on omdb, tweets search from twitter, users search from twitter
data_summary.txt: results of data analysis




Function explanation:

search_movie:
parameter: name of movie title (string)
what it does: 
	1. check if the movie related information is in the cache file
	2. if yes, retrive the movie info from cache file
	3. if no, send request to omdb to obtain movie info, then open the cache file and store the data in it
return: the movie information 

get_tweets:
parameter: name of movie title (string)
what it does: 
	1. check if the movie related tweet information is in the cache file
	2. if yes, retrive the tweet from cache file
	3. if no, search movie related tweets from twitter, then open the cache file and store the tweets in it
return: the tweets related to that particular movie

get_user_info:
parameter: user id (int)
what it does: 
	1. check if the user information is in the cache file
	2. if yes, retrive the user from cache file
	3. if no, search the user from twitter, then open the cache file and store the user in it
return: the user information










Class explanation:

Movie class
A Movie instance is a movie, with title, director, actors, released year, revenue, imdb rating, number of languages
constructor:
name: __init__
parameter: a dictionary with the essential information of a movie (title, director, actors, released year, revenue, imdb rating, number of languages)
what it does: init a Movie instance with title, director, actors, released year, revenue, imdb rating, number of languages

print:
name: __print__
parameter: self
what it does: print out the information of a movie
return: nothing

turn to tuple:
name: movie_tuple
parameter: self
what it does: turn the instance variables of a Movie instance into a tuple (for later use when inserting the movies into the database table)
return: the movie tuple



Tweet class
A Tweets class is a tweet, with tweet id, tweet text, user id, movie id, number of favorites, number of retweets
constructor:
name: __init__
paramter: a dictionary with tweet id, tweet text, user id (reference to the user table), movie id (reference to the movie table), number of favorites, number of retweets
what it does: init a Tweet instance with tweet id, tweet text, user id, movie reference (movie id of the movie in the table), number of favorites, number of retweets

turn to tuple:
name: tweet_tuple
parameter: self
what it does: turn the instance variables of a Tweet instance into a tuple (for later use when inserting the tweets into the database table)
return: the tweet tuple



User class
A Users instance is a user, with user id, screen name, description, number of favorites, number of followers
constructor:
name: __init__
paramter: a dictionary with user id, screen name, description, number of favorites, number of followers
what it does: init a Tweet instance with user id, screen name, description, number of favorites, number of followers

turn to tuple:
name: tweet_tuple
parameter: self
what it does: turn the instance variables of a Users instance into a tuple (for later use when inserting the users into the database table)
return: the user tuple








Database Tables:

Movies:
each row represents a movie
attributes: imdb_id, title, director, rating, actors, year, revenue, num_of_language

Tweets:
each row represents a tweet
attributes: tweet_id, tweet_text, user_id, movie_id, favs (number of favorites), retweets (number of retweets)

Users:
each row represents a user
attributes: user_id, screen_name, description, num_favs, num_followers








Data Manipulation:

1. select movies that have have over or equal to 8.0 imdb rating
Use list comprehension to store the movie titles in the list

2. select movies that have over 100M revenue
User list comprehension to store the movie titles in the list

3. store the most common character in the tweets (with retweets more than 100) of movies with revenue higher than 100M
	1. split the tweets into words, then split the words into characters
	2. store the characters as a list and append it to the movie title as the value of the key (the key is the movie title)
	3. then a dicitionary, whose key is a movie and who values is a list of characters, is created
	4. use counter (from collection library) to count the occurrences of the characters
	5. user dictionary comprehension to append the counter object to the movie
	6. user dictionary comprehension to append the tuple, which has the most common character and its number of occurrences, to the movie

4. store Interaction Index (num of followers / num of favs) of users that have tweets with more than 200 retweets
	1. select screen_name, num_favs, num_followers from the tweets and users table
	2. user mapping in list comprehension to create a list tuples, each of which has the user screen name and interaction index
	3. use sorted method to reorder the list

5. select screen names of users whose tweets (about a movie) that more than 100 retweets
	1. user set comprehension on a list comprehension to put the names into a list without having duplicates





Project Motivation:
I choose this option because I LOVE movies and I am quite familiar with twitter API.  I want to see if there is any interesting information about movies and tweets.





