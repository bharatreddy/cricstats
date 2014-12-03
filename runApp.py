from flask import Flask, render_template, request, jsonify
import MySQLdb
import json
app = Flask(__name__)

db = MySQLdb.connect( user='root', host='localhost', port=3306, db='cricdata' )

@app.route("/")
def hello():
    return render_template('index_cric.html')

if __name__ == "__main__":
    app.debug=True
    app.run()