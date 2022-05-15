from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    print('hi')
    mars_db = mongo.db.collection.find_one()
    print(mars_db)
    return render_template("index.html", mars=mars_db)




@app.route("/scrape")
def scrape():
    print('start scrape')
        # Run the scrape function
    mars = scrape_mars.scrape_all()

    #print(mars.mars_facts_html)
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

#run flask
#$env:FLASK_ENV = "debug"; python app.py



