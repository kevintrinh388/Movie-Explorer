Movie Explorer App

Link to app - https://rocky-woodland-86089.herokuapp.com/

Technologies, frameworks, libraries, and APIs used:

- Python, HTML, CSS, JavaScript, React
- Python imports: Flask, requests, random, os, python-dotenv, Flask-Login, psycopg2-binary, Flask-SQLALchemy
- Heroku
- PostgreSQL
- Wikipedia API (MediaWiki Action API)
- The Movie Database (TMDB) API

How to set up project:

1. Install python
2. Use pip to install Flask, requests, and python-dotenv, Flask-login, psycopg2-binary,
and Flask-SQLAlchemy
3. Install heroku
4. Create .env that contains your TMDB api key, Database URL(found in heroku's config vars), and secret key
5. The .env file should look like this:

export TMDB_KEY = "YOUR_KEY_HERE"

export MY_DATABASE_URL = "YOUR_DATABASE_URL_HERE"

export SECRET_KEY = "YOUR_SECRET_KEY_HERE"

6. Create a heroku app and add a postgresql database to it using "heroku addons:create heroku-postgres:hobby-dev"and push to it
7. Go to your heroku app settings and add your tmdb key, database url, and secret key from your .env file to the config vars.
8. You should now be able to see the web app!!!

Questions:

1. What are at least 3 technical issues you encountered with your project? How did you fix them?

- The first major issue that I encountered during Milestone 3 was figuring out how to retrieve all of a user's reviews and send it to the react page so that it can be displayed. At first I tried querying all the comments and doing flask.jsonify on it but it would not work. I ended up iterating through that query, creating a dictionary of the comment's values, and then added that to a list to be jsonified. Then in the App.js I displayed all of the comments using the map function.

- The second major issue was that I had no clue how I was going to keep track of what the user will edit/delete in the reviews page. I ended up playing around with useRef and found out that I could use that to keep track of what reviews need to be deleted/edited. This would lead to another problem which was how could I update the useRef everytime the user interacted with the comment/rating inputs. I was able to solve this problem using the onChange event for the comment/rating inputs.

- The final issue that I encountered was trying make the server respond with some sort of status message after the react app sends the reviews to be edited/deleted. I ended up making it so that if the server sees that the list of things to be deleted is empty, then it would just respond with a json object {"SUCCESS":"FALSE"}. For the reviews to be edited, if the user has chosen everything to be deleted (which means the list of things to be edited would be empty) then it would just respond with a json object {"SUCCESS":"FALSE"}. If any of these lists are not empty, then the server would respond with a json object {"SUCCESS":"TRUE"}.

2. What was the hardest part of the project for you, across all milestones? What is the most useful thing you learned, across all milestones?

- Personally, this milestone was probably the hardest because it required decent knowledge about React. The hardest part about this project was figuring out how to keep track of the user's edits and deletes and sending that data to the server to work with the database.

- Across all the milestones, learning how to use flask to create routes and basically make your own web app was by far the most useful thing.
