if __name__ == "__main__":
    import inningsDump
    dbo = inningsDump.InnData()
    dbo.populate_tables(iplData=True)

class InnData(object):
    """
    A utilities class to populate innings/deliveries data from the yaml files to the DB.
    """

    def __init__(self):
        import mysql.connector
        # set up connections to the DB
        self.conn = mysql.connector.Connect(host='localhost',user='root',\
                                password='',database='cricdata')
        self.cursor = self.conn.cursor()

    def populate_tables(self, iplData=False, allData=False):
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
            print "curr Match->", j, loopCntr
            loopCntr += 1
            stream = open(i, 'r')
            matchDict = yaml.load(stream)
            # get the file number and convert it to int
            Id = int(j[:-5])
            # Loop through innings
            for inn in matchDict['innings']:
                innKey = inn.keys()
                for ik in innKey:
                    if 'team' in inn[ik]:
                        if 'Super Over' not in ik:
                            innNum = int(ik[0])
                        else:
                            innNum = 0
                        teamName = inn[ik]['team']
                        self.popInningsTab( Id, innNum, teamName )
                    if 'deliveries' in inn[ik]:
                        for dlvrs in inn[ik]['deliveries']:
                            for dk in dlvrs.keys():
                                delvrsDict = {}
                                overNum = float(dk)
                                delvrsDict['Over'] = overNum
                                delvrsDict['InnNum'] = innNum
                                if 'batsman' in dlvrs[dk]:
                                    delvrsDict['Batsman'] = dlvrs[dk]['batsman']
                                else:
                                    delvrsDict['Batsman'] = None
                                if 'bowler' in dlvrs[dk]:
                                    delvrsDict['Bowler'] = dlvrs[dk]['bowler']
                                else:
                                    delvrsDict['Bowler'] = None
                                if 'non_striker' in dlvrs[dk]:
                                    delvrsDict['NonStriker'] = dlvrs[dk]['non_striker']
                                else:
                                    delvrsDict['NonStriker'] = None
                                if 'runs' in dlvrs[dk]:
                                    if 'batsman' in dlvrs[dk]['runs']:
                                        delvrsDict['BatsmanRuns'] = dlvrs[dk]['runs']['batsman']
                                    else:
                                        delvrsDict['BatsmanRuns'] = None
                                    if 'extras' in dlvrs[dk]['runs']:
                                        delvrsDict['ExtraRuns'] = dlvrs[dk]['runs']['extras']
                                    else:
                                        delvrsDict['ExtraRuns'] = None
                                    if 'non_boundary' in dlvrs[dk]['runs']:
                                        delvrsDict['NonBoundary'] = dlvrs[dk]['runs']['non_boundary']
                                    else:
                                        delvrsDict['NonBoundary'] = None
                                else:
                                    delvrsDict['BatsmanRuns'] = None
                                    delvrsDict['ExtraRuns'] = None
                                    delvrsDict['NonBoundary'] = None
                                if 'supersub' in dlvrs[dk]:
                                    delvrsDict['Substitution'] = str(dlvrs[dk]['supersub'])
                                else:
                                    delvrsDict['Substitution'] = None
                                # Not sure what thekey was
                                if 'super_sub' in dlvrs[dk]:
                                    delvrsDict['Substitution'] = str(dlvrs[dk]['super_sub'])
                                else:
                                    delvrsDict['Substitution'] = None
                                if 'wicket' in dlvrs[dk]:
                                    delvrsDict['Wicket'] = "True"
                                    if "fielders" in dlvrs[dk]['wicket']:
                                        delvrsDict['WicketFielder'] = dlvrs[dk]['wicket']['fielders'][0]
                                    else:
                                        delvrsDict['WicketFielder'] = None
                                    if "kind" in dlvrs[dk]['wicket']:
                                        delvrsDict['WicketKind'] = dlvrs[dk]['wicket']['kind']
                                    else:
                                        delvrsDict['WicketKind'] = None
                                    if "player_out" in dlvrs[dk]['wicket']:
                                        delvrsDict['WicketPlayerOut'] = dlvrs[dk]['wicket']['player_out']
                                    else:
                                        delvrsDict['WicketPlayerOut'] = None
                                else:
                                    delvrsDict['Wicket'] = None
                                    delvrsDict['WicketFielder'] = None
                                    delvrsDict['WicketKind'] = None
                                    delvrsDict['WicketPlayerOut'] = None
                                if 'extras' in dlvrs[dk]:
                                    delvrsDict['Extra'] = dlvrs[dk]['extras'].keys()[0]
                                else:
                                    delvrsDict['Extra'] = None
                                self.popDeliveriesTab( Id, delvrsDict )

    def popDeliveriesTab(self, Id, delvrsDict):
        """
        Populate the Delivieries table
        """
        query = ("INSERT INTO Deliveries "
               " (MatchId, InnNum, Over, Batsman, NonStriker, Bowler, BatsmanRuns, ExtraRuns,"
               " NonBoundary, Substitution, Wicket, WicketFielder, WicketKind, WicketPlayerOut, Extra) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   InnNum=VALUES(InnNum), "
               "   Over=VALUES(Over), "
               "   Batsman=VALUES(Batsman), "
               "   NonStriker=VALUES(NonStriker), "
               "   Bowler=VALUES(Bowler), "
               "   BatsmanRuns=VALUES(BatsmanRuns), "
               "   ExtraRuns=VALUES(ExtraRuns), "
               "   NonBoundary=VALUES(NonBoundary), "
               "   Substitution=VALUES(Substitution), "
               "   Wicket=VALUES(Wicket), "
               "   WicketFielder=VALUES(WicketFielder), "
               "   WicketKind=VALUES(WicketKind), "
               "   WicketPlayerOut=VALUES(WicketPlayerOut), "
               "   Extra=VALUES(Extra) ")
        params = (
            Id,
            delvrsDict['InnNum'],
            delvrsDict['Over'], 
            delvrsDict['Batsman'], 
            delvrsDict['NonStriker'], 
            delvrsDict['Bowler'], 
            delvrsDict['BatsmanRuns'], 
            delvrsDict['ExtraRuns'], 
            delvrsDict['NonBoundary'], 
            delvrsDict['Substitution'], 
            delvrsDict['Wicket'], 
            delvrsDict['WicketFielder'], 
            delvrsDict['WicketKind'], 
            delvrsDict['WicketPlayerOut'], 
            delvrsDict['Extra'])
        self.cursor.execute(query, params)
        self.conn.commit()


    def popInningsTab( self, Id, innNum, teamName ):
        """
        Populate the Innings table
        """
        query = ("INSERT INTO Innings "
               " (MatchId, InningsNum, Team) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   MatchId=VALUES(MatchId), "
               "   InningsNum=VALUES(InningsNum), "
               "   Team=VALUES(Team) ")
        params = (
            Id,
            innNum, 
            teamName)
        self.cursor.execute(query, params)
        self.conn.commit()
