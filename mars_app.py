# Import dependencies

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraper

#Create your app
mars_app = Flask(__name__)

#Connect to Mongo DB with PyMongo; create a new database
mongo = PyMongo(mars_app, uri="mongodb://localhost:27017/Mars_dict")

@mars_app.route("/")
def home():
    Mars_data1 = mongo.db.collection.find_one()
    return render_template("index.html", Mars_dict = Mars_data1)

@mars_app.route("/scrape")
def scrape():
    Mars_dict = mars_scraper.scrape_mars()
    mongo.db.collection.update({}, Mars_dict, upsert=True)
    return redirect("/")
    
if __name__=="__main__":
    mars_app.run(debug = True)
