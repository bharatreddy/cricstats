from flask import Flask, render_template, request, jsonify
import MySQLdb
import json
app = Flask(__name__)

db = MySQLdb.connect( user='root', host='localhost', port=3306, db='cricdata' )
# db = MySQLdb.connect( user='root', host='localhost', port=3306, db='gituserinfo' )

@app.route("/dataBatsman")
def dataBatsman():
    # Query the database for Batsman stats
    queryBatsman = """
            SELECT Name, Runs, Balls, StrikeRate, Matches
            FROM Batsman
            """
    db.query( queryBatsman )
    batsmanSmryRet = db.store_result().fetch_row( maxrows=0 )
    batsmandet = [ s for s in batsmanSmryRet ]
    return json.dumps( [ { 'Name': batsmandet[r][0], 'Runs':batsmandet[r][1], \
        'Balls':batsmandet[r][2],'StrikeRate':batsmandet[r][3], 'Matches':batsmandet[r][4] }
         for r in range( len( batsmandet ) ) ] )

@app.route("/dataBowler")
def dataBowler():
    # Query the database for Bowler stats
    queryBowler = """
            SELECT Name, Runs, Balls, RunRate, Matches, Wickets
            FROM Bowler
            """
    db.query( queryBowler )
    bowlerSmryRet = db.store_result().fetch_row( maxrows=0 )
    bowlerdet = [ s for s in bowlerSmryRet ]
    return json.dumps( [ { 'Name': bowlerdet[r][0], 'Runs':bowlerdet[r][1], 'Balls':bowlerdet[r][2], \
        'RunRate':bowlerdet[r][3],'Matches':bowlerdet[r][4], 'Wickets':bowlerdet[r][5] }
         for r in range( len( bowlerdet ) ) ] )

@app.route("/dataGraph")
def dataGraph():
    # Query the database for Bowler stats
    queryGraph = """
            SELECT Batsman, Bowler, StrikeRate, Matches, Dismissed
            FROM PlayerGraph
            """
    db.query( queryGraph )
    graphSmryRet = db.store_result().fetch_row( maxrows=0 )
    graphdet = [ s for s in graphSmryRet ]
    return json.dumps( [ { 'Batsman': graphdet[r][0], 'Bowler':graphdet[r][1], 'StrikeRate':graphdet[r][2], \
        'Matches':graphdet[r][3],'Dismissed':graphdet[r][4] }
         for r in range( len( graphdet ) ) ] )

@app.route("/")
def hello():
    return render_template('index_cric.html')

@app.route("/<pagename>")
def regularpage( pagename=None ):
    """
    if route not found
    """
    return "No such page as " + pagename + " please go back!!! "

if __name__ == "__main__":
    app.debug=True
    app.run()