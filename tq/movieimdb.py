#!/usr/bin/env python3

# Import the imdb package.
import imdb
import csv

ia = imdb.IMDb()

# Dictionary where the movie name is the key and the corresponding
# values are the list
movieSet = {}
numberOfMovies = 0
successMovie = 0

# Search for a movie (get a list of Movie objects).

movieDatabase = open("imdbmovie.csv", "w")


with open('links.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        numberOfMovies += 1 
        try:        
            s_result =  ia.get_movie(row[1])

            directorList = ""
            for director in s_result['director']:
                if(directorList == "") :
                    directorList = director['name']
                else:
                    directorList = directorList + "|" + director['name']
        
            castList =  ""
            for cast in s_result['cast']:
                if(castList == "") :
                    castList = cast['name']
                else:
                    castList = castList + "|" + cast['name']
           
            movieDatabase.write(row[1] + "," + castList + "," + directorList + "," + str(s_result['runtime'][0]) + "," + str(s_result['rating']) + "\n") 
            successMovie += 1
            print(str(successMovie) + " out of " + str(numberOfMovies) + " movies found")
        except Exception as error:
            print("Something went wrong. Error: " + str(error))

