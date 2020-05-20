from src.app import app
from flask import request, send_file
from src.statistics import plot_todos, joined_list, overall_pearson_r

@app.route("/tweets/analysis")
def years_plots():
    bytes_obj = plot_todos()
    
    return send_file(bytes_obj,
                     attachment_filename='../img/plot.png',
                     mimetype='image/png')

