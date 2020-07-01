# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
import math



from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions, Actions
import game
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveReflexAgent', second='DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [MyAgent(firstIndex), MyAgent(secondIndex)]


##########
# Agents #
##########

class MyAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):

    legalActions = gameState.getLegalActions(self.index)
    nextStates = []
    for action in legalActions:
      nextStates.append(gameState.generateSuccessor(self.index, action))
    actionValues = []

    for state in nextStates:
      actionValues.append(self.getActionValue(state))
    best = max(actionValues)
    print(legalActions)
    print(actionValues)
    print(legalActions[actionValues.index(best)])
    return legalActions[actionValues.index(best)]

  def evaluate(self, gameState):

    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):

    #inicijalizacija svega
    features = util.Counter()
    foodList = self.getFood(gameState).asList()
    features['successorScore'] = len(foodList)  # self.getScore(successor)
    myPosition = gameState.getAgentState(self.index).getPosition()
    walls = gameState.getWalls()
    topFoodList = [(x, y) for x, y in foodList if y > math.floor(walls.height / 2)]
    botFoodList = [(x, y) for x, y in foodList if y <= math.floor(walls.height / 2)]
    enemies = []
    for opponent in self.getOpponents(gameState):
      enemies.append(gameState.getAgentState(opponent))
    pacmans = []  # invaders
    ghosts = []  # defenders
    for enemy in enemies:
      if enemy.isPacman and enemy.getPosition() != None:
        pacmans.append(enemy)
      else:
        ghosts.append(enemy)
    #======================================================================

    if self.index > 1:
      distancesFromFood = []
      if (len(topFoodList) != 0):
        for food in topFoodList:
          distance = self.getMazeDistance(myPosition, food)
          distancesFromFood.append(distance)
        minDistance = min(distancesFromFood)
        features['distanceToFoodTOP'] = minDistance
      else:
        for food in botFoodList:
          distance = self.getMazeDistance(myPosition, food)
          distancesFromFood.append(distance)
        minDistance = min(distancesFromFood)
        features['distanceToFoodBOTTOM'] = minDistance
    else:
      distancesFromFood = []
      if (len(botFoodList) != 0):
        for food in botFoodList:
          distance = self.getMazeDistance(myPosition, food)
          distancesFromFood.append(distance)
        minDistance = min(distancesFromFood)
        features['distanceToFoodBOTTOM'] = minDistance
      else:
        for food in topFoodList:
          distance = self.getMazeDistance(myPosition, food)
          distancesFromFood.append(distance)
        minDistance = min(distancesFromFood)
        features['distanceToFoodTOP'] = minDistance


    features['numInvaders'] = len(pacmans)
    if len(pacmans) > 0:
      distancesFromInvaders = []
      for invader in pacmans:
        distancesFromInvaders.append(self.getMazeDistance(myPosition, invader.getPosition()))
      if gameState.getAgentState(self.index).scaredTimer == 0 or self.checkTeammate(gameState) == False:
        features['invaderDistance'] = min(distancesFromInvaders)


    if len(ghosts) > 0 and gameState.getAgentState(self.index).isPacman:
      distancesFromGhosts = []
      for ghost in ghosts:
        distancesFromGhosts.append(self.getMazeDistance(myPosition, ghost.getPosition()))
      if min(distancesFromGhosts) < 6:
        if ghosts[distancesFromGhosts.index(min(distancesFromGhosts))].scaredTimer == 0:
          print("USAO U DUH JE BLIZU")
          features['ghostDistance'] = min(distancesFromGhosts)

    return features

  def checkTeammate(self, gameState):
    if (self.index == 0 or self.index == 1) and gameState.getAgentState(self.index).isPacman:
      if not gameState.getAgentState(self.index+2).isPacman:
        return True
      else:
        return False
    else:
      if not gameState.getAgentState(self.index-2).isPacman:
        return True
      else:
        return False


  def getWeights(self, gameState):

    if gameState.getScore() > 0:
      return {'ghostDistance': -1700,'numInvaders': -1000, 'invaderDistance': -10}
    else:
      return {'ghostDistance': -1700,'successorScore': -100, 'distanceToFoodTOP': -1, 'distanceToFoodBOTTOM': -1, 'numInvaders': -100, 'invaderDistance': -10}

  def getActionValue(self, state):
    return self.evaluate(state)