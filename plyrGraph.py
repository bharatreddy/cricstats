if __name__ == "__main__":
    import plyrGraph
    grphObj = plyrGraph.CricGraph()
    grphObj.player_graph()
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

    def player_graph(self):
        """
        Get the ralation graph between batsman and bowler.
        The data has the following columns :
        Batsman, Bowler, Runs, Balls, out.
        """
        import pandas
        # Query to retreive data and build the graph.
        graphQry = """
                    SELECT Batsman, Bowler, SUM(BatsmanRuns) as Runs, 
                    SUM( CASE WHEN Extra IS NULL THEN 1 ELSE 0 END) 
                    as Balls, 
                    SUM(BatsmanRuns)*100./COUNT(Over) as StrikeRate, 
                    SUM( CASE WHEN Wicket IS NOT NULL THEN 1 ELSE 0 END) 
                    as Wicket
                    FROM Deliveries
                    GROUP BY Batsman, Bowler;
                   """
        graphDF = pandas.read_sql( graphQry, self.conn )
        return graphDF

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
                        PRIMARY KEY (Name)
                        )
                    """
        bowlerStr = """
                    CREATE TABLE IF NOT EXISTS Bowler(
                        Name VARCHAR(100) NOT NULL,
                        Runs INT NULL,
                        Balls INT NULL,
                        RunRate FLOAT NULL,
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
                        Wicket INT NULL,
                        FOREIGN KEY (Batsman) REFERENCES Batsman(Name),
                        FOREIGN KEY (Bowler) REFERENCES Bowler(Name)
                        )
                    """
            self.cursor.execute(batsmanStr)
            self.cursor.execute(bowlerStr)
            self.cursor.execute(plyrGrphStr)
            self.conn.commit()

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.conn.close()