from flask import Flask, render_template, request, jsonify
import MySQLdb
import json
app = Flask(__name__)

# db = MySQLdb.connect( user='root', host='localhost', port=3306, db='cricdata' )
db = MySQLdb.connect( user='root', host='localhost', port=3306, db='gituserinfo' )

@app.route("/dataUser")
#, userDict=userD3List
def dataUser():
    # Query the database for some initial stuff
    queryMainGraph = """
            SELECT userdetail.nflwr, count(repocontr.login), repocontr.login
            FROM repocontr JOIN userdetail 
            ON repocontr.login=userdetail.login 
            GROUP BY repocontr.login;
            """
    db.query( queryMainGraph )
    userSmryRet = db.store_result().fetch_row( maxrows=0 )
    # print userSmryRet
    userdet = [ s for s in userSmryRet ]

    return json.dumps( [ { 'login': userdet[r][2], 'nflwrs':userdet[r][0], 'nrepos':userdet[r][1] }
         for r in range( len( userdet ) ) ] )


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