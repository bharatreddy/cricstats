if __name__ == "__main__":
    import cricDump
    dbo = cricDump.CrData()
    dbo.populate_main_tables(iplData=True)

class CrData(object):
    """
    A utilities class to populate data from the yaml files to the DB.
    """

    def __init__(self):
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='cricdata')
        self.cursor = self.conn.cursor()

    def populate_main_tables(self, iplData=False, allData=False):
        """
        popluate ipl data into main tables

        #### INPUTS ####
        iplData : populate data from ipl matches folder
        allData : populate data from all matches folder
        #### INPUTS ####
        """
        import yaml
        import os
        # Directory of ipl data
        iplDir = '/Users/bharat/Desktop/cric/ipl/'
        allDir = '/Users/bharat/Desktop/cric/all/'
        # get all the 'yaml' files in the directory
        cricFiles = []
        # we also need a list of the file names (not including the dir)
        fnList = []
        if iplData:
            iplFiles = [ iplDir+f for f in os.listdir(iplDir) \
            if os.path.isfile(os.path.join(iplDir,f)) and 'yaml' in f ]
            fnList += [ f for f in os.listdir(iplDir) \
            if os.path.isfile(os.path.join(iplDir,f)) and 'yaml' in f ]
            cricFiles += iplFiles
        if allData:
            allFiles = [ allDir+f for f in os.listdir(allDir) \
            if os.path.isfile(os.path.join(allDir,f)) and 'yaml' in f ]
            fnList += [ f for f in os.listdir(allDir) \
            if os.path.isfile(os.path.join(allDir,f)) and 'yaml' in f ]
            cricFiles += allFiles
        # Loop throught the files and parse them.
        loopCntr = 1 # just a counter to keep track of num files looped
        for i,j in zip(cricFiles,fnList):
            print "curr File->", j, loopCntr
            loopCntr += 1
            stream = open(i, 'r')
            matchDict = yaml.load(stream)
            # Main tbl data
            mainDict = {}
            # get the file number and convert it to int
            Id = int(j[:-5])
            if 'city' in mainDict:
                mainDict['city'] = matchDict['info']['city']
            else:
                mainDict['city'] = None
            if type(matchDict['info']['dates']) == list:
                mainDict['mDate'] = matchDict['info']['dates'][0]
            else:
                mainDict['mDate'] = matchDict['info']['dates']
            mainDict['mType'] = matchDict['info']['match_type']
            mainDict['mVenue'] = matchDict['info']['venue']
            mainDict['mComptn'] = matchDict['info']['competition']
            mainDict['mOvers'] = matchDict['info']['overs']
            self.popMainTab( Id, mainDict )
            # Toss tbl data
            tossDict = {}
            mToss = matchDict['info']['toss']
            tossDict['TossDec'] = mToss['decision']
            tossDict['TossWin'] = mToss['winner']
            self.popTossTab( Id, tossDict )
            # Teams tbl data
            teamDict = {}
            mTeam = matchDict['info']['teams']
            teamDict['Team1'] = mTeam[0]
            teamDict['Team2'] = mTeam[1]
            self.popTeamsTab( Id, teamDict )
            # Umpires tbl data
            umpireDict = {}
            mUmpire = matchDict['info']['umpires']
            umpireDict['Umpire1'] = mUmpire[0]
            umpireDict['Umpire2'] = mUmpire[1]
            self.popUmpiresTab( Id, umpireDict )
            # player of Match tbl data
            if 'player_of_match' in matchDict['info']:
                mPoM = matchDict['info']['player_of_match']
            else:
                mPoM = [None]
            self.popPlayerOfMatchTab( Id, mPoM )
            # Outcome tbl data
            outDict = {}
            mOut = matchDict['info']['outcome']
            if 'winner' in mOut:
                outDict['winner'] = mOut['winner']
            else:
                outDict['winner'] = None
            if 'result'in mOut:
                outDict['result'] = mOut['result']
            else:
                outDict['result'] = None
            if 'eliminator' in mOut:
                outDict['eliminator'] = mOut['eliminator']
            else:
                outDict['eliminator'] = None
            if 'method' in mOut:
                outDict['method'] = mOut['method']
            else:
                outDict['method'] = None
            if 'by' in mOut:
                mOutBy = mOut['by'].keys()
                if type(mOutBy) == list:
                    mOutBy = mOutBy[0]
                if mOutBy.lower() == 'innings':
                    outDict['Innings'] = mOut['by']['innings']
                else:
                    outDict['Innings'] = None
                if mOutBy.lower() == 'runs':
                    outDict['Runs'] = mOut['by']['runs']
                else:
                    outDict['Runs'] = None
                if mOutBy.lower() == 'wickets':
                    outDict['Wickets'] = mOut['by']['wickets']
                else:
                    outDict['Wickets'] = None
            else:
                outDict['Innings'] = None
                outDict['Runs'] = None
                outDict['Wickets'] = None
            self.popOutcomeTab( Id, outDict)

    def popMainTab(self, Id, mainDict):
        """
        Populate the Game table
        """
        query = ("INSERT INTO Game "
               " (Id, MatchDate, Type, Venue, Competition, Overs) "
               " VALUES (%s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   Id=VALUES(Id), "
               "   MatchDate=VALUES(MatchDate), "
               "   Type=VALUES(Type), "
               "   Venue=VALUES(Venue), "
               "   Competition=VALUES(Competition), "
               "   Overs=VALUES(Overs) ")
        params = (
            Id, 
            mainDict['mDate'][0], 
            mainDict['mType'], 
            mainDict['mVenue'], 
            mainDict["mComptn"], 
            mainDict["mOvers"])
        self.cursor.execute(query, params)
        self.conn.commit()

    def popOutcomeTab(self, Id, outDict):
        """
        Populate the Outcome table
        """
        query = ("INSERT INTO Outcome "
               " (MatchId, Winner, Innings, Runs, Wickets, Result, Eliminator, Method) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   Winner=VALUES(Winner), "
               "   Innings=VALUES(Innings), "
               "   Runs=VALUES(Runs), "
               "   Wickets=VALUES(Wickets), "
               "   Result=VALUES(Result), "
               "   Eliminator=VALUES(Eliminator), "
               "   Method=VALUES(Method)")
        params = (
            Id, 
            outDict['winner'],
            outDict['Innings'], 
            outDict["Runs"], 
            outDict["Wickets"],
            outDict["result"],
            outDict["eliminator"],
            outDict["method"])
        self.cursor.execute(query, params)
        self.conn.commit()

    def popPlayerOfMatchTab(self, Id, playerList):
        """
        Populate the PlayerOfMatch table
        """
        for p in playerList:
            query = ("INSERT INTO PlayerOfMatch "
                   " (MatchId, Player) "
                   " VALUES (%s, %s) "
                   " ON DUPLICATE KEY UPDATE "
                   "   MatchId=VALUES(MatchId), "
                   "   Player=VALUES(Player) ")
            params = (
                Id, 
                p)
            self.cursor.execute(query, params)
            self.conn.commit()

    def popTeamsTab(self, Id, teamDict):
        """
        Populate the Teams table
        """
        query = ("INSERT INTO Teams "
               " (MatchId, Team1, Team2) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   Team1=VALUES(Team1), "
               "   Team2=VALUES(Team2) ")
        params = (
            Id, 
            teamDict['Team1'],
            teamDict['Team2'])
        self.cursor.execute(query, params)
        self.conn.commit()

    def popUmpiresTab(self, Id, umpireDict):
        """
        Populate the Umpires table
        """
        query = ("INSERT INTO Umpires "
               " (MatchId, Umpire1, Umpire2) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   Umpire1=VALUES(Umpire1), "
               "   Umpire2=VALUES(Umpire2) ")
        params = (
            Id, 
            umpireDict['Umpire1'],
            umpireDict['Umpire2'])
        self.cursor.execute(query, params)
        self.conn.commit()

    def popTossTab(self, Id, tossDict):
        """
        Populate the Toss table
        """
        query = ("INSERT INTO Toss "
               " (MatchId, Winner, Decision) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   Decision=VALUES(Decision), "
               "   Winner=VALUES(Winner) ")
        params = (
            Id, 
            tossDict['TossDec'],
            tossDict['TossWin'])
        self.cursor.execute(query, params)
        self.conn.commit()