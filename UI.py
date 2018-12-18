940#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 07:00:06 2018

@author: aashaiavadhani
"""

#retrieved data from https://github.com/christopherjenness/NBA-player-movement
from image_util import *
#create this its own window, in another window show the live stats of the
#game in the other window
from gatherData import Game
from circleClass import Circle
#from liveStatisticsWindow import
# Updated Animation Starter Code
from tkinter import *
from statistics import *
import copy
from scipy.spatial import ConvexHull
import numpy as np

def init(data):
    data.stateGame = "splashScreen"
    data.gameObject = Game('12.4.2015', 'Suns', 'Wizards')
#set of the circle objects which represent the players
    data.listCircles = []
    data.time = None
    data.currentScore = 0
    data.currentDescription = ""
    data.currentPlayers = dict()
    data.count = 0
    data.spacialAnalysisHome = False
    data.spacialAnalysisVisitor = False
    data.spacialAnalysisAreaHomeEfficiency = 0
    data.spacialAnalysisAreaVisitorEfficiency = 0
    data.pauseGame = False
    data.speedGame = False
    data.slowGame = False
    data.icon = PhotoImage(file = "nba.gif")

def currentPlayersOnCourt(data):

    dictionaryJerseyNumPlayerID = data.gameObject.dictionaryPlayerIDJerseyNum
    homePlayers = data.gameObject.homePlayers
    visitorPlayers = data.gameObject.visitorPlayers
    setCurrentPlayers = set()

    for playerID in data.gameObject.dictPlayersLocation:
        setCurrentPlayers.add(playerID)

    setHomePlayers = set()
    setVisitorPlayers = set()
    dictionarySet = dict()
    for playerID in setCurrentPlayers:
        if(playerID in homePlayers):

            setHomePlayers.add((homePlayers[playerID],dictionaryJerseyNumPlayerID[playerID]))
        elif(playerID in visitorPlayers):
            setVisitorPlayers.add((visitorPlayers[playerID],dictionaryJerseyNumPlayerID[playerID]))

    #seperate into a teams dictionary
    dictionarySet = {"home": setHomePlayers, "visitor": setVisitorPlayers}
    data.currentPlayers = dictionarySet



def mousePressed(event, data):
    clickX = event.x
    clickY = event.y
    #clicked button 1
    #create button 1 goes to the help screen
    coordButton1LeftX = data.width/2-(data.width/3) - 50
    coordButton1RightX = coordButton1LeftX + 200
    coordButton1TopY = data.height-100
    coordButton1BottomY = data.height
    #clicked button 2
    #create button 2 goes to the help screen
    coordButton2LeftX = data.width/2+(data.width/3)-100
    coordButton2RightX = (data.width/2+(data.width/3) - 100) + 200
    coordButton2TopY = data.height-100
    coordButton2BottomY = data.height


    boolButtonX1 = (clickX > coordButton1LeftX and clickX < coordButton1RightX)
    boolButtonY1 = (clickY < coordButton1BottomY and clickY > coordButton1TopY)

    boolButtonX2 = (clickX > coordButton2LeftX and clickX < coordButton2RightX)
    boolButtonY2 = (clickY < coordButton2BottomY and clickY > coordButton2TopY)



    spacialAnalysisHomeX = (clickX > data.width/8 - 100 and clickX < (data.width/8 - 100) + 200)
    spacialAnalysisHomeY = (clickY > data.height -50 and clickY < data.height)


    spacialAnalysisVisitorX = (clickX > data.width/2 + 120 and clickX < (data.width/2 + 120) + 140)
    spacialAnalysisVisitorY = (clickY > data.height -50 and clickY < data.height)



    offSet = 10
    pauseX = (clickX > ((940/2 - 120) + offSet) and clickX < ((940/2)+100) + offSet)
    pauseY = ((clickY > data.height-20) and (clickY < data.height))

    #button for the back button help Screen
    backHelperArea = (((clickX < 100)and(clickX>0)) and ((clickY < 100) and (clickY>0)))


    #button for the first game
    knicksGameX = (clickX>data.width/2- 200 and clickX<data.width/2 + 200)
    knicksGameY = (clickY > data.height/2 - 200 and clickY < data.height/2 - 100)

    #button for the second game
    sunsGameX = (clickX>data.width/2- 200 and clickX<data.width/2 + 200)
    sunsGameY = (clickY > data.height/2 and data.height/2+100)

    #button for the back to homescreen game

    homeScreenX = ((clickX > data.width-200) and (clickX < data.width)) and ((clickY > data.height-50) and (clickY < data.height))



    if(boolButtonX1 and boolButtonY1):
        data.stateGame = "playGame"
    elif(boolButtonX2 and boolButtonY2):
        data.stateGame = "helpScreen"

    elif(data.stateGame == "playGame" and (spacialAnalysisHomeX and spacialAnalysisHomeY)):
        data.spacialAnalysisHome = not(data.spacialAnalysisHome)

    elif(data.stateGame == "playGame" and (spacialAnalysisVisitorX and spacialAnalysisVisitorY)):
        data.spacialAnalysisVisitor = not(data.spacialAnalysisVisitor)


    elif(data.stateGame == "playGame" and (pauseX and pauseY)):
        data.pauseGame = not(data.pauseGame)

    elif(data.stateGame == "helpScreen" and backHelperArea):
        data.stateGame = "splashScreen"

    elif(data.stateGame == "helpScreen" and (knicksGameX and knicksGameY)):
        data.gameObject.playByPlayFileName = "ScoreData.csv"
        data.gameObject.trackingJson = "data1.json"
    elif(data.stateGame == "helpScreen" and (sunsGameX and sunsGameY)):
        data.gameObject.playByPlayFileName = "sunsGameGoodPlayData.csv"
        data.gameObject.trackingJson = "0021500284.json"
    elif(data.stateGame == "helpScreen" and (homeScreenX)):
        data.stateGame = "splashScreen"
    else:
        pass



def keyPressed(event, data):
    pass

def getScore(data,convertTimeFormat):
    dictionaryScore = data.gameObject.dictionaryScoreTime
    quarter = data.gameObject.moments.quarter[data.gameObject.frameNumber]
    dictionaryQuarter = dictionaryScore[quarter]
    if(convertTimeFormat in dictionaryQuarter):
        data.currentScore = dictionaryQuarter[convertTimeFormat]

def getDescription(data,convertTimeFormat):
    homeDict = data.gameObject.dictionaryTimeDescriptionHome
    visitorDict = data.gameObject.dictionaryTimeDescriptionVisitor
    quarter = data.gameObject.moments.quarter[data.gameObject.frameNumber]
    dictionaryQuarterHome = homeDict[quarter]
    dictionaryQuarterVisitor = visitorDict[quarter]
    if(convertTimeFormat in dictionaryQuarterHome):
        data.currentDescription = dictionaryQuarterHome[convertTimeFormat]
    elif(convertTimeFormat in dictionaryQuarterVisitor):
        data.currentDescription = dictionaryQuarterVisitor[convertTimeFormat]




def drawLiveScore(canvas,data):
    dataFrameTime = data.gameObject.moments["quarter_time"]
    quarter = data.gameObject.moments.quarter[data.gameObject.frameNumber]
    currentTime = dataFrameTime.iloc[data.gameObject.frameNumber]
    currentShotClock = data.gameObject.moments.shot_clock[data.gameObject.frameNumber]
    convertTimeFormat = StatisticsMethods.convertTimeLeftToStringFormat(currentTime)
    getScore(data,convertTimeFormat)
    getDescription(data,convertTimeFormat)
    canvas.create_text(90,10, text = "Home Team: " + str(data.gameObject.team1), font = "Times 19 bold")
    canvas.create_text(940 - 80,10, text = "Visitor Team: " + str(data.gameObject.team2),font = "Times 19 bold")
    canvas.create_text(940//2 - 80,10,text = "GameTime: " + str(convertTimeFormat),font = "Times 19 bold")
    canvas.create_text(940/4, 10, text = "Quarter: " + str(quarter), font = "Times 19 bold")
    canvas.create_text((940//2 + 940//4) - 30, 10, text = "Shot Clock: " + str(currentShotClock),font = "Times 19 bold")
    canvas.create_text(940//2+60,10,text = "Score: "+ str(data.currentScore),font = "Times 19 bold")
    canvas.create_text(940//2 - 40 ,data.height - 40,text = "Description: "+ str(data.currentDescription),
                        font = "Times 19 bold")


def drawCourt(canvas,data):
    #top line
    margin = 20
    canvas.create_rectangle(0,20,940,data.height-60, fill = "bisque")
    canvas.create_line(0,margin,940,margin,width = 3)
    #half line
    canvas.create_line(940/2,margin,940/2,data.height-60,width = 3)
    #bottom line
    canvas.create_line(0,data.height - 60,940, data.height-60,width = 3)
    #right line
    canvas.create_line(940,margin,940, data.height-60,width = 3)

    #creating the midline
    radius = (940 * 0.1276595745)/2
    centerX = (940)/2
    centerY = (data.height-60) /2
    canvas.create_oval(centerX - radius, centerY - radius,
                    centerX + radius, centerY + radius,width =3,fill = "light blue")
    canvas.create_text(centerX,centerY, text = '''      112
Basketball''', font = "Times 20 bold",fill = "black")
    #creating the basketball hoop
    lengthBackboard = (data.height-60) * 0.12

    radius = (lengthBackboard * 0.25) / 2


    lengthAwayBasketballAway = 940/2 + (940 * 0.4468085106)
    lengthAwayBasketballHome = 940/2 - (940 * 0.4468085106)


    lengthBackboard = data.height * 0.12

#LEFT side of the basketball court


        #basketball hoop
    #creating the semicircle
    centerLeftCircleX = (940-60) * (19/94)
    centerLeftCircleY = (data.height-60)/2
    radiusCircle = ((940-60) * 0.1276595745)/2

    canvas.create_rectangle(0,centerLeftCircleY - radiusCircle,
            centerLeftCircleX,centerLeftCircleY + radiusCircle, fill = "light blue")

    canvas.create_oval(lengthAwayBasketballHome-radius,((data.height-60)/2) - radius,
                    lengthAwayBasketballHome + radius, ((data.height-60)/2) + radius,width =3)
    canvas.create_line(lengthAwayBasketballHome-radius, ((data.height-60)/2) - lengthBackboard/2,
                        lengthAwayBasketballHome-radius, ((data.height-60)/2) + lengthBackboard/2,width =3)


    canvas.create_oval(centerLeftCircleX - radiusCircle, centerLeftCircleY - radiusCircle,
                        centerLeftCircleX + radiusCircle, centerLeftCircleY + radiusCircle,width =3,fill = "light blue")
    canvas.create_line(centerLeftCircleX, centerLeftCircleY - radiusCircle,
                        centerLeftCircleX, centerLeftCircleY + radiusCircle,width =3)

    #creating the two line thing
    lengthLineLeft = (940) * (19/94)
    widthLineArc  = 20 + (500 * 0.06)
    canvas.create_line(0,centerLeftCircleY - radiusCircle,centerLeftCircleX,
                        centerLeftCircleY - radiusCircle,width =3)


    displacement = (data.height-60) * (12/50)
    canvas.create_line(0,centerLeftCircleY + radiusCircle,centerLeftCircleX,
                        centerLeftCircleY + radiusCircle,width =3)




#creating the 3 point arc
    distBetweenHoop3Pt = 500 * 0.2857142857
    fourTeenFeet = (940) * 0.1489361702
    canvas.create_line(0, widthLineArc,
                    fourTeenFeet,widthLineArc,width =3)
    canvas.create_line(0,500 - widthLineArc ,
                    fourTeenFeet,500 - widthLineArc,width =3)
    canvas.create_arc(fourTeenFeet-150,widthLineArc,
                    fourTeenFeet + 150, 500 - widthLineArc,start = 90, extent = -180, style = "arc",width =3)



#create the arc
    distTo3PTLine = (13.9 / 94) * (940 - 60)
    #should be able to change to an arc , need help with that

#RIGHT side of the basketball court

    centerRightCircleX = (940) - ((940) * (19/94))
    centerRightCircleY = (data.height-60)/2

    canvas.create_rectangle(centerRightCircleX,centerRightCircleY-radiusCircle,
                    940,centerRightCircleY+radiusCircle,fill = "light blue")
    canvas.create_oval(lengthAwayBasketballAway-radius,((data.height-60)/2) - radius,
                lengthAwayBasketballAway + radius, ((data.height-60)/2) + radius,width =3)
    canvas.create_line(lengthAwayBasketballAway+radius, ((data.height-60)/2) - lengthBackboard/2,
                        lengthAwayBasketballAway+radius, ((data.height-60)/2) + lengthBackboard/2,width =3)


    #creating the semicircle
    canvas.create_oval(centerRightCircleX - radiusCircle, centerRightCircleY - radiusCircle,
                        centerRightCircleX + radiusCircle, centerRightCircleY + radiusCircle,width =3,fill = "light blue")
    #midline semicircle
    canvas.create_line(centerRightCircleX, centerRightCircleY - radiusCircle,
                        centerRightCircleX, centerRightCircleY + radiusCircle,width =3)
    #creating the two line thing
    canvas.create_line(940,centerRightCircleY - radiusCircle,940 - lengthLineLeft,centerRightCircleY - radiusCircle,width =3)
    canvas.create_line(940,centerRightCircleY + radiusCircle,940 - lengthLineLeft,centerRightCircleY + radiusCircle,width =3)


    #creating the 3pt arc
    canvas.create_line(940, widthLineArc,
                    940 - fourTeenFeet,widthLineArc,width =3)
    canvas.create_line(940,500 - widthLineArc ,
                    940 - fourTeenFeet,500 - widthLineArc,width =3)

    canvas.create_arc(940 - fourTeenFeet-150,widthLineArc,
                    940 - fourTeenFeet + 150, 500 - widthLineArc,start = 90, extent = 180, style = "arc",width =3)


#drawing the button for the home spacial analysis
    canvas.create_rectangle(data.width/8 - 120,data.height -50,
                            (data.width/8 - 120) + 140, data.height)
    canvas.create_text((data.width/8) - 50, data.height - 25, text = str('''Home
Spacial Analysis'''))

#drawing the button for the visitor spacial analysis
    canvas.create_rectangle(data.width/2 + 120,data.height -50,
                            (data.width/2 + 120) + 140, data.height)
    canvas.create_text(data.width/2 + 190, data.height - 25, text = str('''Visitor
Spacial Analysis'''))

    canvas.create_rectangle(data.width-200,data.height-50,data.width,
                            data.height)

    canvas.create_text(data.width-100,data.height-25,text = "Back to HomeScreen", font = "Times 16 bold")


def drawCircles(canvas,data):
    color = "SeaGreen1"
    for circle in data.listCircles:
        if(circle.side == "home"):
            color = "pink"
        elif(circle.side == "visitor"):
            color = "SeaGreen1"
        xCord = (circle.x * 10)
        yCord = (circle.y * 10)
        jerseyNum = circle.jerseyNum
        radiusCircle = circle.radius
        canvas.create_oval(xCord- radiusCircle, yCord - radiusCircle,
                            xCord + radiusCircle, yCord + radiusCircle,
                            fill = color)
        canvas.create_text(xCord,yCord, text = str(jerseyNum),font = "Times 14 bold",
        fill="black")


    #draw the ball
    balllistCoordinates = data.gameObject.ball
    xCor = (balllistCoordinates[0] * 10)
    yCor = (balllistCoordinates[1] * 10)
    radius = balllistCoordinates[2]
    canvas.create_oval(xCor-radius,yCor-radius,xCor + radius,yCor + radius,
                        fill = "brown")

    #SPACIAL DIAGRAMMMMMMMMMMMMMMMMMMMMM


    homeCircles = []
    visitorCircles = []
    for circle in data.listCircles:
        if(circle.side == "home"):
            homeCircles.append((circle.x,circle.y))

    for circle in data.listCircles:
        if(circle.side == "visitor"):
            visitorCircles.append((circle.x,circle.y))
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    x3 = 0
    y3 = 0
    x4 = 0
    y4 = 0
    x5 = 0
    y5 = 0



    if(data.spacialAnalysisHome and data.spacialAnalysisVisitor):
        #home spcial diagram
        for i in range(len(homeCircles)):
            tupleObject = homeCircles[i]
            if(i == 0):
                x1 = tupleObject[0] * 10
                y1 = tupleObject[1] * 10
            elif(i == 1):
                x2 = tupleObject[0] * 10
                y2 = tupleObject[1] * 10

            elif(i == 2):
                x3 = tupleObject[0] * 10
                y3 = tupleObject[1] * 10

            elif(i == 3):
                x4 = tupleObject[0] * 10
                y4 = tupleObject[1] * 10

            elif(i == 4):
                x5 = tupleObject[0] * 10
                y5 = tupleObject[1] * 10

        formatHome = []
        list1 = [x1,y1]
        list2 = [x2,y2]
        list3 = [x3,y3]
        list4 = [x4,y4]
        list5 = [x5,y5]
        formatHome.append(list1)
        formatHome.append(list2)
        formatHome.append(list3)
        formatHome.append(list4)
        formatHome.append(list5)

        homePoints = np.array(formatHome)
        hullConvex = ConvexHull(homePoints)
        data.spacialAnalysisAreaHomeEfficiency = int(((hullConvex.area / (940 * 500)) *1000000)) / 100
        hull_points = homePoints[hullConvex.vertices]

        if(len(hull_points) == 4):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            outline='black',fill ="",width = 3)

        elif(len(hull_points) == 5):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            point5CoordX = hull_points[4][0]
            point5CoordY = hull_points[4][1]

            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            point5CoordX,point5CoordY,outline='black',fill ="",width = 3)


        #visitor spcial diagram
        for i in range(len(visitorCircles)):
            tupleObject = visitorCircles[i]
            if(i == 0):
                x1 = tupleObject[0] * 10
                y1 = tupleObject[1] * 10
            elif(i == 1):
                x2 = tupleObject[0] * 10
                y2 = tupleObject[1] * 10

            elif(i == 2):
                x3 = tupleObject[0] * 10
                y3 = tupleObject[1] * 10

            elif(i == 3):
                x4 = tupleObject[0] * 10
                y4 = tupleObject[1] * 10

            elif(i == 4):
                x5 = tupleObject[0] * 10
                y5 = tupleObject[1] * 10

        formatVisitor = []
        list1 = [x1,y1]
        list2 = [x2,y2]
        list3 = [x3,y3]
        list4 = [x4,y4]
        list5 = [x5,y5]
        formatVisitor.append(list1)
        formatVisitor.append(list2)
        formatVisitor.append(list3)
        formatVisitor.append(list4)
        formatVisitor.append(list5)

        visitorPoints = np.array(formatVisitor)
        hullConvex = ConvexHull(visitorPoints)
        data.spacialAnalysisAreaVisitorEfficiency = int(((hullConvex.area / (940 * 500)) *1000000)) / 100
        hull_points = visitorPoints[hullConvex.vertices]


        if(len(hull_points) == 4):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            outline='red',fill ="",width = 3)

        elif(len(hull_points) == 5):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            point5CoordX = hull_points[4][0]
            point5CoordY = hull_points[4][1]

            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            point5CoordX,point5CoordY,outline='red',fill ="",width = 3)
    elif(data.spacialAnalysisHome):
        #home spcial diagram
        for i in range(len(homeCircles)):
            tupleObject = homeCircles[i]
            if(i == 0):
                x1 = tupleObject[0] * 10
                y1 = tupleObject[1] * 10
            elif(i == 1):
                x2 = tupleObject[0] * 10
                y2 = tupleObject[1] * 10

            elif(i == 2):
                x3 = tupleObject[0] * 10
                y3 = tupleObject[1] * 10

            elif(i == 3):
                x4 = tupleObject[0] * 10
                y4 = tupleObject[1] * 10

            elif(i == 4):
                x5 = tupleObject[0] * 10
                y5 = tupleObject[1] * 10

        formatHome = []
        list1 = [x1,y1]
        list2 = [x2,y2]
        list3 = [x3,y3]
        list4 = [x4,y4]
        list5 = [x5,y5]
        formatHome.append(list1)
        formatHome.append(list2)
        formatHome.append(list3)
        formatHome.append(list4)
        formatHome.append(list5)

        homePoints = np.array(formatHome)
        hullConvex = ConvexHull(homePoints)
        data.spacialAnalysisAreaHomeEfficiency = int(((hullConvex.area / (940 * 500)) *1000000)) / 100
        hull_points = homePoints[hullConvex.vertices]

        if(len(hull_points) == 4):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            outline='black',fill ="",width = 3)

        elif(len(hull_points) == 5):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            point5CoordX = hull_points[4][0]
            point5CoordY = hull_points[4][1]

            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            point5CoordX,point5CoordY,outline='black',fill ="",width = 3)




    elif(data.spacialAnalysisVisitor):
        #home spcial diagram
        for i in range(len(visitorCircles)):
            tupleObject = visitorCircles[i]
            if(i == 0):
                x1 = tupleObject[0] * 10
                y1 = tupleObject[1] * 10
            elif(i == 1):
                x2 = tupleObject[0] * 10
                y2 = tupleObject[1] * 10

            elif(i == 2):
                x3 = tupleObject[0] * 10
                y3 = tupleObject[1] * 10

            elif(i == 3):
                x4 = tupleObject[0] * 10
                y4 = tupleObject[1] * 10

            elif(i == 4):
                x5 = tupleObject[0] * 10
                y5 = tupleObject[1] * 10

        formatVisitor = []
        list1 = [x1,y1]
        list2 = [x2,y2]
        list3 = [x3,y3]
        list4 = [x4,y4]
        list5 = [x5,y5]
        formatVisitor.append(list1)
        formatVisitor.append(list2)
        formatVisitor.append(list3)
        formatVisitor.append(list4)
        formatVisitor.append(list5)

        visitorPoints = np.array(formatVisitor)
        hullConvex = ConvexHull(visitorPoints)
        data.spacialAnalysisAreaVisitorEfficiency = int(((hullConvex.area / (940 * 500)) *1000000)) / 100
        hull_points = visitorPoints[hullConvex.vertices]


        if(len(hull_points) == 4):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            outline='black',fill ="",width = 3)

        elif(len(hull_points) == 5):
            point1CoordX = hull_points[0][0]
            point1CoordY = hull_points[0][1]
            point2CoordX = hull_points[1][0]
            point2CoordY = hull_points[1][1]
            point3CoordX = hull_points[2][0]
            point3CoordY = hull_points[2][1]
            point4CoordX = hull_points[3][0]
            point4CoordY = hull_points[3][1]
            point5CoordX = hull_points[4][0]
            point5CoordY = hull_points[4][1]

            canvas.create_polygon(point1CoordX,point1CoordY,point2CoordX,point2CoordY,
                            point3CoordX,point3CoordY,point4CoordX,point4CoordY,
                            point5CoordX,point5CoordY,outline='black',fill ="",width = 3)

def createButtons(canvas,data):
    offSet = 10
    canvas.create_rectangle((940/2 - 120) + offSet, data.height-20, ((940/2)+100) + offSet, data.height)
    middleX = (((940/2 - 120) + offSet) + ((940/2)+100) + offSet)/2
    middleY = data.height-10
    canvas.create_text(middleX,middleY,text = "Speed Up the Game")

def drawSplashScreen(canvas,data):

    canvas.create_rectangle(0,0,data.width,data.height,fill = "black")
    canvas.create_image(data.width/2 - 100,100,anchor = NW, image = data.icon)

    canvas.create_text(data.width//2,50, text = "Welcome to a Python Simulation of an NBA Game", fill = "white",font = "ComicSans 40 bold")
    #create button 1 goes to the help screen
    coordButton1LeftX = data.width/2-(data.width/3) - 50
    coordButton1RightX = coordButton1LeftX + 200
    coordButton1TopY = data.height-100
    coordButton1BottomY = data.height
    canvas.create_rectangle(coordButton1LeftX, coordButton1TopY,
                            coordButton1RightX, coordButton1BottomY,
                            outline = "white")
    canvas.create_text((data.width/2 - (data.width/3) - 50) + 100,data.height - 50,
                        text = "See an NBA Game!!",fill = "white")

    #create button 2 goes to the help screen
    coordButton2LeftX = data.width/2+(data.width/3)-100
    coordButton2RightX = (data.width/2+(data.width/3) - 100) + 200
    coordButton2TopY = data.height-100
    coordButton2BottomY = data.height
    canvas.create_rectangle(coordButton2LeftX,coordButton2TopY,
                            coordButton2RightX, coordButton2BottomY,
                            outline = "white")
    canvas.create_text((data.width/2+(data.width/3)-100) + 100,data.height - 50,
                        text = "Introduction/Help Screen", fill = "white")


def drawPlayersCourt(canvas,data):
    if(len(data.currentPlayers) > 0):
        canvas.create_text(1050,20,text = data.gameObject.team2 + " Players",font = "Times 19 bold")

        textX = 1050
        textY = 40
        changeY = 20
        homePlayers = data.currentPlayers["home"]
        visitorPlayers = data.currentPlayers["visitor"]

        for player in homePlayers:
            namePlayer = player[0]
            jerseyNum = player[1]
            canvas.create_text(textX,textY + changeY, text = str(namePlayer) + " : " + str(jerseyNum),font = "Times 13 bold")
            textY += 40

        canvas.create_text(1200,20,text = data.gameObject.team1 + " Players",font = "Times 19 bold")

        textX2 = 1200
        textY2 = 40
        changeY = 20
        for player in visitorPlayers:
            namePlayer = player[0]
            jerseyNum = player[1]
            canvas.create_text(textX2,textY2 + changeY,text = str(namePlayer) + " : " + str(jerseyNum),font = "Times 13 bold")
            textY2 += 40



def drawEfficiencyArea(canvas,data):
    homeEfficiency = data.spacialAnalysisAreaHomeEfficiency
    visitorEfficiency = data.spacialAnalysisAreaVisitorEfficiency

    canvas.create_text(data.width-175, (data.height/2),
                        text = '''Home Team's Formation Efficiency:
                        %''' + str(homeEfficiency),font = "Times 19 bold")

    canvas.create_text(data.width-175, (data.height/2 +100),
                        text = '''Visitor Team's Formation Efficiency:
                        %''' +str(visitorEfficiency),font = "Times 19 bold")

    if(homeEfficiency > visitorEfficiency):
        canvas.create_text(data.width-175, (data.height/2 +200),
                        text = '''Home Team's formation is Better''',font = "Times 19 bold")

    elif(visitorEfficiency > homeEfficiency):
        canvas.create_text(data.width-175, (data.height/2 +200),
                        text = '''Visitor Team's formation is better''',font = "Times 19 bold")


def drawHelpScreen(canvas,data):

    #backbutton
    canvas.create_rectangle(0,0,data.width,data.height,fill = "black")
    canvas.create_rectangle(0,0,100,100,outline = "white")
    canvas.create_text(50,50,text = "Back",fill = "white")

    #making the button for the knicks game

    canvas.create_rectangle(data.width/2- 200, data.height/2-200,data.width/2 + 200,
                            data.height/2-100,outline = "white")

    canvas.create_text(data.width/2, data.height/2 - 150,text = "Watch the Kings play the Knicks!",
                font = "Times 20 bold",fill = "white")


    #making the button for another game
    canvas.create_rectangle(data.width/2- 200, data.height/2,data.width/2 + 200,
                            data.height/2+100,outline = "white")
    canvas.create_text(data.width/2, data.height/2 + 50,text = "Watch the Suns play the Wizards!",
                    font = "Times 20 bold",fill = "white")
def redrawAll(canvas, data):
    if(data.stateGame == "splashScreen"):
        drawSplashScreen(canvas,data)

    elif(data.stateGame == "playGame"):
        data.count += 1
        drawCourt(canvas,data)
        drawCircles(canvas,data)
        if(len(data.listCircles) >= 10): data.listCircles = []
        drawLiveScore(canvas,data)
        drawPlayersCourt(canvas,data)
        drawEfficiencyArea(canvas,data)
        createButtons(canvas,data)

    else:
        drawHelpScreen(canvas,data)



def determineSidePlayer(data,keyInput):

    #go through the homePlayers see if its within which players
    homePlayers = data.gameObject.homePlayers
    if(keyInput in homePlayers):
        return "home"

    #go through the visitor Players see if its within which players
    visitorPlayers = data.gameObject.visitorPlayers
    if(keyInput in visitorPlayers):
        return "visitor"

def timerFired(data):
    if(data.stateGame == "splashScreen"):
        pass

    elif(data.stateGame == "playGame"):
        data.gameObject.frameNumber += 1
        data.gameObject.getXYCoordinates()
        for key in data.gameObject.dictPlayersLocation:
        #value is going to be a tuple of x and y
            sidePlayer = determineSidePlayer(data,key)
            value = data.gameObject.dictPlayersLocation[key]
            xCord = value[0]
            yCord = value[1]
            jerseyNum = value[2]
            circleObj = Circle(xCord,yCord,jerseyNum,sidePlayer)
            data.listCircles.append(circleObj)
        currentPlayersOnCourt(data)
        if(data.pauseGame):
            data.timerDelay = 1
        elif(data.pauseGame == False):
            data.timerDelay = 35










####################################
# use the run function as-is
####################################

def run(width=1000, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 35 #changed to ensure that the remaining quarter time and the
                        #proper time is displayed every second
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 560)





#original dimensions were 940, 500
