#Import libraries
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#Flask Setup
app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

#Create the home page
@app.route("/")
def index():
    #mars = mongo.db.mars.find_one()
    return render_template("index.html")#, mars=mars)
    #return("hello")

#Create a site that collects all the scrapped stuff
@app.route("/scrape")
def scraper():
    mars = mongo.db.listings
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

#Needed to make everything work
if __name__ == "__main__":
    app.run(debug=True)
