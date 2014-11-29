if __name__ == "__main__":
    import plyrGraph
    grphObj = plyrGraph.CricGraph()
    grphObj.create_tables()
    grphObj.populate_tables()
    grphObj.close()

class CricGraph(object):
    """
    Build a graph connecting batsmen and bowlers.

    Bharat Kunduri
    """
    def __init__(self):
        """
        Setup connections with the MySQL
        and connect with the cricdata DB.
        """
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='cricdata')
        self.cursor = self.conn.cursor()

    def player_rel_graph(self):
        """
        Get the ralation graph between batsman and bowler.
        The data has the following columns :
        Batsman, Bowler, Runs, Balls, StrikeRate, Matches, Dismissed.
        """
        import pandas
        # Query to retreive data and build the graph.
        graphQry = """
                    SELECT Batsman, Bowler, SUM(BatsmanRuns) as Runs, 
                    SUM( CASE WHEN Extra IS NULL THEN 1 ELSE 0 END) 
                    as Balls, 
                    SUM(BatsmanRuns)*100./COUNT(Over) as StrikeRate, 
                    COUNT( DISTINCT MatchId ) as Matches,
                    SUM( CASE WHEN Wicket IS NOT NULL THEN 1 ELSE 0 END) 
                    as Dismissed
                    FROM Deliveries
                    GROUP BY Batsman, Bowler;
                   """
        graphDF = pandas.read_sql( graphQry, self.conn )
        return graphDF

    def batsman_data(self):
        """
        Get the batsman graph.
        The data has the following columns :
        Name, Runs, Balls, StrikeRate, Matches and Dismissed.
        """
        import pandas
        # Query to retreive data and build the graph.
        batsmanQry = """
                    SELECT Batsman as Name, SUM(BatsmanRuns) as Runs, 
                    SUM( CASE WHEN Extra IS NULL THEN 1 ELSE 0 END) 
                    as Balls, 
                    SUM(BatsmanRuns)*100./COUNT(Over) as StrikeRate, 
                    COUNT( DISTINCT MatchId ) as Matches,
                    SUM( CASE WHEN Wicket IS NOT NULL THEN 1 ELSE 0 END) 
                    as Dismissed
                    FROM Deliveries
                    GROUP BY Batsman;
                   """
        batsmanDF = pandas.read_sql( batsmanQry, self.conn )
        return batsmanDF

    def bowler_data(self):
        """
        Get the bowler graph.
        The data has the following columns :
        Name, Runs, Balls, StrikeRate, Matches and Wickets.
        """
        import pandas
        # Query to retreive data and build the graph.
        bowlerQry = """
                    SELECT Bowler as Name, SUM(BatsmanRuns) as Runs, 
                    SUM( CASE WHEN Extra IS NULL THEN 1 ELSE 0 END) 
                    as Balls, 
                    SUM(BatsmanRuns)/
                    (SUM( CASE WHEN Extra IS NULL THEN 1 ELSE 0 END)/6.)
                    as RunRate, 
                    COUNT( DISTINCT MatchId ) as Matches,
                    SUM( CASE WHEN Wicket IS NOT NULL THEN 1 ELSE 0 END) 
                    as Wickets
                    FROM Deliveries
                    GROUP BY Bowler;
                   """
        bowlerDF = pandas.read_sql( bowlerQry, self.conn )
        return bowlerDF

    def create_tables(self):
        """
        Create the playerGraph, batsman and bowlers tables
        """
        # create the Batsman table
        batsmanStr = """
                    CREATE TABLE IF NOT EXISTS Batsman(
                        Name VARCHAR(100) NOT NULL,
                        Runs INT NULL,
                        Balls INT NULL,
                        StrikeRate FLOAT NULL,
                        Matches INT NULL,
                        Dismissed INT NULL,
                        PRIMARY KEY (Name)
                        )
                    """
        bowlerStr = """
                    CREATE TABLE IF NOT EXISTS Bowler(
                        Name VARCHAR(100) NOT NULL,
                        Runs INT NULL,
                        Balls INT NULL,
                        RunRate FLOAT NULL,
                        Matches INT NULL,
                        Wickets INT NULL,
                        PRIMARY KEY (Name)
                        )
                    """
        # create the PlayerGraph table
        plyrGrphStr = """
                    CREATE TABLE IF NOT EXISTS PlayerGraph(
                        Batsman VARCHAR(100) NOT NULL,
                        Bowler VARCHAR(100) NOT NULL,
                        Runs INT NULL,
                        Balls INT NULL,
                        StrikeRate FLOAT NULL,
                        Matches INT NULL,
                        Dismissed INT NULL,
                        FOREIGN KEY (Batsman) REFERENCES Batsman(Name),
                        FOREIGN KEY (Bowler) REFERENCES Bowler(Name)
                        )
                    """
        self.cursor.execute(batsmanStr)
        self.cursor.execute(bowlerStr)
        self.cursor.execute(plyrGrphStr)
        self.conn.commit()

    def populate_playergraphtab(self, plGrphDict):
        """
        Insert values into the player graph table
        plGrphDict : Dictionary containing values to be inserted
                    into the table.
        """
        query = ("INSERT INTO PlayerGraph "
               " (Batsman, Bowler, Runs, Balls, StrikeRate, Matches, Dismissed) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   Batsman=VALUES(Batsman), "
               "   Bowler=VALUES(Bowler), "
               "   Runs=VALUES(Runs), "
               "   Balls=VALUES(Balls), "
               "   StrikeRate=VALUES(StrikeRate), "
               "   Matches=VALUES(Matches), "
               "   Dismissed=VALUES(Dismissed) ")
        params = (
            plGrphDict['Batsman'],
            plGrphDict['Bowler'], 
            plGrphDict['Runs'], 
            plGrphDict['Balls'], 
            plGrphDict['StrikeRate'], 
            plGrphDict['Matches'], 
            plGrphDict['Dismissed'])
        self.cursor.execute(query, params)
        self.conn.commit()

    def populate_batsmantab(self, batsmanDict):
        """
        Insert values into the batsman table
        batsmanDict : Dictionary containing values to be inserted
                    into the table.
        """
        query = ("INSERT INTO Batsman "
               " (Name, Runs, Balls, StrikeRate, Matches, Dismissed) "
               " VALUES (%s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   Name=VALUES(Name), "
               "   Runs=VALUES(Runs), "
               "   Balls=VALUES(Balls), "
               "   StrikeRate=VALUES(StrikeRate), "
               "   Matches=VALUES(Matches), "
               "   Dismissed=VALUES(Dismissed) ")
        params = (
            batsmanDict['Name'], 
            batsmanDict['Runs'], 
            batsmanDict['Balls'], 
            batsmanDict['StrikeRate'], 
            batsmanDict['Matches'], 
            batsmanDict['Dismissed'])
        self.cursor.execute(query, params)
        self.conn.commit()

    def populate_bowlertab(self, bowlerDict):
        """
        Insert values into the bowler table
        bowlerDict : Dictionary containing values to be inserted
                    into the table.
        """
        query = ("INSERT INTO Bowler "
               " (Name, Runs, Balls, RunRate, Matches, Wickets) "
               " VALUES (%s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   Name=VALUES(Name), "
               "   Runs=VALUES(Runs), "
               "   Balls=VALUES(Balls), "
               "   RunRate=VALUES(RunRate), "
               "   Matches=VALUES(Matches), "
               "   Wickets=VALUES(Wickets) ")
        params = (
            bowlerDict['Name'], 
            bowlerDict['Runs'], 
            bowlerDict['Balls'], 
            bowlerDict['RunRate'], 
            bowlerDict['Matches'], 
            bowlerDict['Wickets'])
        self.cursor.execute(query, params)
        self.conn.commit()

    def populate_tables(self):
        """
        Populate the Batsman, Bowler and PlayerGraph tables
        """
        import pandas
        # get the relevant DFs
        playerGraphDF = self.player_rel_graph()
        batsmanDF = self.batsman_data()
        bowlerDF = self.bowler_data()
        # Loop through each of the DF's and populate the tables
        # Note we need to populate batsman and bowler tables first
        # due to foreign key constraints.
        print "Currently working with Batsman table..."
        for ba in batsmanDF.iterrows():
            self.populate_batsmantab( ba[1] )
        print "Currently working with Bowler table..."
        for bo in bowlerDF.iterrows():
            self.populate_bowlertab( bo[1] )
        print "Currently working with playerGraph table..."
        for pg in playerGraphDF.iterrows():
            self.populate_playergraphtab( pg[1] )

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.conn.close()