from src.app import app
from flask import request, send_file, Response
from bson.json_util import dumps
from src.statistics import plot_todos, joined_list, overall_pearson_r
from src.tweet_functions import search_terms, tweetsDiarios,extractorTweets, limpiador
import json
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Call analysis results
@app.route("/tweets/results")
def years_plots():
    bytes_obj = plot_todos()

    return send_file(bytes_obj,
                     attachment_filename='grafica.png',
                     mimetype='image/png')
# Call raw tweets
@app.route("/tweets/<location>/search")
def searchTweets(location):
    date_start = request.args.get("start")
    date_end = request.args.get("end")

    # Apply the function to search the tweets:
    df = extractorTweets(search_terms, date_start, date_end, location)
    # Return as json
    return Response(df.to_json(orient="records"), mimetype='application/json')

# Clean and count tweets
@app.route("/tweets/<location>/byterm/search")
def TweetsByTerm(location):
    date_start = request.args.get("start")
    date_end = request.args.get("end")

    # Apply the function to search the tweets:
    df = extractorTweets(search_terms, date_start, date_end, location)
    clean = limpiador(df)
      
    # Initialize the matplotlib figure
    img = io.BytesIO()
    f, ax = plt.subplots(figsize=(10, 6), dpi=120)
    plt.subplots_adjust(bottom=0.4)
    f.suptitle(f"Number of tweets by search term in {location}", fontsize=14)
    sns.countplot(x='search_term', data=clean, ax=ax)
    ax.set_xlabel('Search Term')
    ax.set_ylabel('Number of tweets')
    plt.xticks(rotation=45)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)

# Count the tweets along time
@app.route("/tweets/<location>/count/search")
def countTweets(location):
    date_start = request.args.get("start")
    date_end = request.args.get("end")

    # Apply the function to search the tweets:
    df = extractorTweets(search_terms, date_start, date_end, location)
    clean = limpiador(df)
    daily = tweetsDiarios(clean)
    print('checawey',daily.columns)
   
    # Initialize the matplotlib figure
    img = io.BytesIO()
    f, ax = plt.subplots(figsize=(10, 6), dpi=120)
    plt.subplots_adjust(bottom=0.4)
    f.suptitle(f"Number of tweets over time in {location}", fontsize=14)
    plt.plot(daily.n_tweets)
    plt.xlabel("Day")
    plt.ylabel("Number of tweets")
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)