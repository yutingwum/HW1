## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
# I referenced the lecture and discussion sample code and also those I wrote in lecture and discussion
# ALso the page (link below) for Flask Jsonify examples (which is used in problem 2)
# http://flask.pocoo.org/docs/0.12/api/
# Problem 4 takes refernece from Google Maps Distance matrix API and an example on github, link: https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return 'Welcome to SI 364!'



## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!
from flask import Flask, render_template
from flask import jsonify
import requests
import json

@app.route('/movie/<one_word_movie_name>')
def movie_name(one_word_movie_name):
    url = "https://itunes.apple.com/search?term=" + one_word_movie_name + "&entity=movie"
    r = requests.get(url)
    movie_json = json.loads(r.text)

    return jsonify(movie_json)


## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
from flask import Flask,request

@app.route('/question')
def enterData():
    s = """<!DOCTYPE html>
<html>
<body>
<form action="/result" method="GET">
  Please type your favorite number:<br>
  <input type="text" name="number">
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
# Note that by default eggs would be entered in the input field
    return s

@app.route('/result',methods = ['GET'])
def displayNumber():
  if request.method == 'GET':
    number = request.args.get('number', '')
    return "Double your number is " + str(int(number) * 2)


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form


## This application is suppose to ask the user for a start and destination address and a travel mode
## Then the data will be taken to Google Maps distance matrix to get the distance

# However, right now it does not work and I do not know why or know. Would appreciate it a lot if I can get some feedback on it.
import googlemaps
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
# gmaps = googlemaps.Client(key='AIzaSyC7fpK0XEG_Jj0xpK0XHSetaGew4Vh7GkQ')


@app.route('/problem4form',methods=["GET"])
def problem4form():
    return """ <form action="" method='GET'>
    <input type="text" name="address1"> Enter the start address: <br>
    <input type="text" name="address2"> Enter the destination address: <br>
    <input type="radio" name="travelmode" value="driving"> Drive<br>
    <input type="radio" name="travelmode" value="transit"> Public Transit<br>
    <input type="radio" name="travelmode" value="walking"> Walk<br>
    <input type="submit" value="Submit">
</form>""" 

@app.route('/problem4form',methods = ['GET'])
def get_distance():
  if request.method == 'GET':
  	payload = {'origins' : '|'.join(request.args.get('address1','')),'destinations' : '|'.join(request.args.get('address2','')), 'mode' : request.form['travelmode'],'api_key' : 'AIzaSyC7fpK0XEG_Jj0xpK0XHSetaGew4Vh7GkQ'}
  	r = requests.get(base_url, params = payload)
  	results = json.loads(r.text)
  	distance = results['rows'][0]['elements'][0]['distance']['text']
  	time = results['rows'][0]['elements'][0]['duration']['text']

  	return ('The distance is ' + distance + " and the time is " + time)



## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.



if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
