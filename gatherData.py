import requests as req
from pandas import *
import pandas as pd
import numpy as np

#import matplotlib.pyplot as plt
#import seaborn as sns
import os
#from IPython.display import IFrame
import json
import copy
from statistics import *


curl_request = None
class Game():
    def __init__(self, date, team1, team2):
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.moments = None
        self.events = None
        self.bigJson = None
        self.frameNumber = 0
        self.playByPlayFileName = "sunsGameGoodPlayData.csv"
        self.trackingJson = "0021500284.json"
        self._get_tracking_data()
        self.homeData = self.events["home"]
        self.visitorData = self.events["visitor"]
        self.homePlayers = None
        self.visitorPlayers = None
        self.listPlayers()
        self.ball = [0,0,0]
        #will get the x and y location of the player on each team on
        #that particular frame
        self.dictPlayersLocation = dict()
        self.getXYCoordinates()
        #will increment everytime to increase the frame
        self.frameNumber = 0
        self.game_id = self.bigJson["gameid"]
        self.pbpDataFrame = pd.read_csv(self.playByPlayFileName)
        self.dictionaryScoreTime = None
        self.formatTimeScoreDictionary()
        self.dictionaryTimeDescriptionHome = None
        self.dictionaryTimeDescriptionVisitor = None
        self.formatTimeDescriptionDictionaryHome()
        self.formatTimeDescriptionDictionaryVisitor()
        self.dictionaryPlayerIDJerseyNum = None
        self.getJerseyNum()


    def formatTimeDescriptionDictionaryVisitor(self):
        self.dictionaryTimeDescriptionVisitor = dict()
        dataFrameCopy = copy.deepcopy(self.pbpDataFrame)
        dictionary1 = dict()
        dictionary2 = dict()
        dictionary3 = dict()
        dictionary4 = dict()
        for i in range(len(dataFrameCopy)):
            temp = dataFrameCopy.iloc[i]
            time = temp["PCTIMESTRING"]
            if(len(time) == 4): time = "0" + time
            quarter = temp["PERIOD"]
            description = temp["VISITORDESCRIPTION"]
            if(type(description) == type("hello")):
                if(quarter == 1):
                    dictionary1[time] = description

                elif(quarter == 2):
                    dictionary2[time] = description


                elif(quarter == 3):
                    dictionary3[time] = description


                elif(quarter == 4):
                    dictionary4[time] = description



        self.dictionaryTimeDescriptionVisitor[1] = dictionary1
        self.dictionaryTimeDescriptionVisitor[2] = dictionary2
        self.dictionaryTimeDescriptionVisitor[3] = dictionary3
        self.dictionaryTimeDescriptionVisitor[4] = dictionary4

    def formatTimeDescriptionDictionaryHome(self):
        self.dictionaryTimeDescriptionHome = dict()
        dataFrameCopy = copy.deepcopy(self.pbpDataFrame)
        dictionary1 = dict()
        dictionary2 = dict()
        dictionary3 = dict()
        dictionary4 = dict()
        for i in range(len(dataFrameCopy)):
            temp = dataFrameCopy.iloc[i]
            time = temp["PCTIMESTRING"]
            if(len(time) == 4): time = "0" + time
            quarter = temp["PERIOD"]
            description = temp["HOMEDESCRIPTION"]
            if(type(description) == type("hello")):
                if(quarter == 1):
                    dictionary1[time] = description

                elif(quarter == 2):
                    dictionary2[time] = description


                elif(quarter == 3):
                    dictionary3[time] = description


                elif(quarter == 4):
                    dictionary4[time] = description



        self.dictionaryTimeDescriptionHome[1] = dictionary1
        self.dictionaryTimeDescriptionHome[2] = dictionary2
        self.dictionaryTimeDescriptionHome[3] = dictionary3
        self.dictionaryTimeDescriptionHome[4] = dictionary4


    def formatTimeScoreDictionary(self):
        self.dictionaryScoreTime = dict()
        dataFrameCopy = copy.deepcopy(self.pbpDataFrame)
        dictionary1 = dict()
        dictionary2 = dict()
        dictionary3 = dict()
        dictionary4 = dict()
        for i in range(len(dataFrameCopy)):
            temp = dataFrameCopy.iloc[i]
            time = temp["PCTIMESTRING"]
            if(len(time) == 4): time = "0" + time
            quarter = temp["PERIOD"]
            score = temp["SCORE"]
            if(type(score) == type("hello")):
                if(quarter == 1):
                    dictionary1[time] = score

                elif(quarter == 2):
                    dictionary2[time] = score


                elif(quarter == 3):
                    dictionary3[time] = score


                elif(quarter == 4):
                    dictionary4[time] = score



        self.dictionaryScoreTime[1] = dictionary1
        self.dictionaryScoreTime[2] = dictionary2
        self.dictionaryScoreTime[3] = dictionary3
        self.dictionaryScoreTime[4] = dictionary4




#will return a dicionary of players and their playerIDs in the current frame
    def listPlayers(self):
        frameNum = self.frameNumber


        #HOME players
        #get dictionary of player IDs to their names
        dictHomePlayers = dict()
        temp = copy.deepcopy(self.homeData.iloc[10])

        listPlayers = temp["players"]

        listPlayerID = []
        for setObj in listPlayers:
            playerID = setObj["playerid"]
            namePlayer = setObj["firstname"] + setObj["lastname"]
            dictHomePlayers[playerID] = namePlayer
        self.homePlayers = copy.copy(dictHomePlayers)

        #VISITOR players
        #get dictionary of player IDs to their names
        dictVisitorPlayers = dict()
        temp = copy.deepcopy(self.visitorData.iloc[10])
        listPlayers = temp["players"]

        listPlayerID = []
        for setObj in listPlayers:
            playerID = setObj["playerid"]
            namePlayer = setObj["firstname"] + setObj["lastname"]
            dictVisitorPlayers[playerID] = namePlayer
        self.visitorPlayers = copy.copy(dictVisitorPlayers)


    def getPlayByPlayData(self):
        pass


    def _get_tracking_data(self):
        nameFile = self.trackingJson
        with open(nameFile.format(self=self)) as data_file:
            self.bigJson = json.load(data_file)  # Load this json
        events = pd.DataFrame(self.bigJson['events'])
        self.events = events
        moments = []
        # Extract 'moments': Each moment is an individual frame
        for row in events['moments']:
            for inner_row in row:
                moments.append(inner_row)
        moments = pd.DataFrame(moments)
        moments = moments.drop_duplicates(subset=[1])
        moments = moments.reset_index()
        moments.columns = ['index', 'quarter', 'universe_time', 'quarter_time',
                           'shot_clock', 'unknown', "positions"]
        moments['game_time'] = (moments.quarter - 1) * 720 + \
                               (720 - moments.quarter_time)
        moments.drop(['index', 'unknown'], axis=1, inplace=True)

        self.moments = moments



    #be able to use matplotlib to plot the coordinates of the x and y conditions
    #of the players onto the coordinate plane
    def getXYCoordinates(self):
        frameNum = self.frameNumber

        #this is a series of the all the locations of the players throughout the
        #game
        pandaMomentsPosition = self.moments["positions"]

        overallPosition = copy.copy(pandaMomentsPosition.iloc[frameNum])
        #get the teamID

        for positionElement in overallPosition:
            indexTeamID = positionElement[0]
            playerID = positionElement[1]
            #its the balls position
            if(indexTeamID == -1):
                #x location ball
                self.ball[0] = positionElement[2]
                #y location ball
                self.ball[1] = positionElement[3]
                #radius of ball
                self.ball[2] = positionElement[-1]

            else:

                playerIDTeam = positionElement[1]
                playerJersey = self.retrieveJerseyNum(playerIDTeam)
                xCorPlayer = positionElement[2]
                yCorPlayer = positionElement[3]
                self.dictPlayersLocation[playerIDTeam] = [xCorPlayer,yCorPlayer,
                                                                playerJersey]

    def retrieveJerseyNum(self,playerID):
        copyHomeData = self.homeData.iloc[10]
        copyVisitorData = self.visitorData.iloc[10]


        playerListHomes = copyHomeData["players"]
        for elementDict in playerListHomes:
            playerIDEstimate = elementDict["playerid"]
            if(playerIDEstimate == playerID):
                return elementDict["jersey"]

        playerListVisitor = copyVisitorData["players"]
        for elementDict in playerListVisitor:
            playerIDEstimate = elementDict["playerid"]
            if(playerIDEstimate == playerID):
                return elementDict["jersey"]

    def getJerseyNum(self):
        frameNum = self.frameNumber
        dictionaryIDJersey = dict()
        pandaMomentsPosition = self.moments["positions"]

        overallPosition = copy.copy(pandaMomentsPosition.iloc[frameNum])
        #getting the current players on the court and a dictionary with
        #their playerID and their jersey number
        for positionElement in overallPosition:
            playerID = positionElement[1]
            jerseyNumber = self.retrieveJerseyNum(playerID)
            dictionaryIDJersey[playerID] = jerseyNumber
        self.dictionaryPlayerIDJerseyNum = dictionaryIDJersey
