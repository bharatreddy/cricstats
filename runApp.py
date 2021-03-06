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

@app.route("/dataGraph/<srchPlyr>/<srchBy>")
def dataGraph(srchPlyr='DefaultPlayer',srchBy='DefaultOrder'):
    # # Query the database for stats related to the graph.
    # srchPlyr = request.args.get('playerSrch')
    # print '-----------helloooooooooooo-->', srchPlyr
    srchPlyr = srchPlyr
    srchBy = srchBy
    if srchPlyr == 'DefaultPlayer':
        srchPlyr = 'MS Dhoni'
    if srchBy == 'DefaultOrder':
        srchBy = "Balls"
    if srchPlyr is None:
        srchPlyr = 'MS DHONI'
    queryGraph = "SELECT Batsman, Bowler, Runs, Balls, StrikeRate, Matches, Dismissed " + \
                "FROM PlayerGraph WHERE Batsman = '" + srchPlyr + "'" + \
                "OR Bowler = '" + srchPlyr + "'" + \
                "ORDER BY " + srchBy + " DESC LIMIT 25"
    db.query( queryGraph )
    graphSmryRet = db.store_result().fetch_row( maxrows=0 )
    graphdet = [ s for s in graphSmryRet ]
    linksList = json.dumps( [ { 'Batsman': graphdet[r][0], 'Bowler':graphdet[r][1],\
     'Runs':graphdet[r][2], 'Balls':graphdet[r][3], \
        'StrikeRate':graphdet[r][4], \
        'Matches':graphdet[r][5],'Dismissed':graphdet[r][6] }
         for r in range( len( graphdet ) ) ] )
    return linksList

@app.route('/searchPlayers')
def searchPlayers():
    search = request.args.get('search')
    querySrchStr = "SELECT Name FROM Bowler WHERE Name LIKE " + "'%" + search + "%' " +\
                    "UNION SELECT Name FROM Batsman WHERE Name LIKE " + "'%" + search + "%' "
    db.query( querySrchStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    resOut = [ res[0] for res in query_results ]
    return json.dumps( resOut )

# @app.route("/updtGraph")
# def updateGraph():
#     srchPlyr = request.args.get('playerSrch')
#     print srchPlyr, '-----------hellooooo'
#     return render_template('index_cric.html')

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