class CricGraph(object):
    """
    Build a graph connecting batsmen and bowlers.

    Bharat Kunduri
    """
    def __init__(self):
        """
        Setup connections with the MySQL
        and connect with the cricdata DB
        """
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='cricdata')