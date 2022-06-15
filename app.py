from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

# scraping.py uses splinter, beautifulsoup & a chrome web-driver to scrape multiple websites
import scraping

# set up Flask
app = Flask(__name__)

# set up mongo connection using PyMongo with Uniform Resource Indentifier (URI)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

# create an index route
@app.route("/")

def index():

    # find the collection "mars" in database
    mars = mongo.db.mars.find_one()
    # renders a template from the template folder with the given context
    return render_template("index.html", mars=mars)

# create the scrape route
@app.route("/scrape")

def scrape():

    # point to the mars mongo database
    mars = mongo.db.mars

    # reference scrape_all function in scraping.py
    mars_data = scraping.scrape_all()

    # update the database with the gathered data
    mars.update_one({}, {"$set":mars_data}, upsert=True)

    return redirect('/', code=302)

if __name__ == "__main__":

    app.run()


