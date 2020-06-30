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
    print(legalActions)
    print(actionValues)
    best = max(actionValues)
    return legalActions[actionValues.index(best)]

  def evaluate(self, gameState):

    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):

    # OFFENSIVE
    features = util.Counter()
    foodList = self.getFood(gameState).asList()
    features['successorScore'] = len(foodList)  # self.getScore(successor)
    myPosition = gameState.getAgentState(self.index).getPosition()
    walls = gameState.getWalls()
    topFoodList = [(x, y) for x, y in foodList if y > math.floor(walls.height / 2)]
    botFoodList = [(x, y) for x, y in foodList if y <= math.floor(walls.height / 2)]

    if self.index > 1:
      distancesFromFood = []
      if(len(topFoodList) != 0):
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
      if len(botFoodList) != 0:

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


    enemies = []
    for opponent in self.getOpponents(gameState):
      enemies.append(gameState.getAgentState(opponent))
    pacmans = [] #invaders
    ghosts = []  #defenders
    for enemy in enemies:
      if enemy.isPacman and enemy.getPosition() != None:
        pacmans.append(enemy)
      else:
        ghosts.append(enemy)
    features['numghosts'] = - len(ghosts)
    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPosition, ghost.getPosition()) for ghost in ghosts]
      features['ghostDistance'] = - min(dists)

    escape = [gameState.getLegalActions()]
    if len(ghosts) > 0:
      distancesFromGhost = []
      for ghost in ghosts:
        distancesFromGhost.append(self.getMazeDistance(myPosition, ghost.getPosition()))
      minGhostDistance = min(distancesFromGhost)
      if len(escape) == 1 and minGhostDistance < 4:
        features['deadend'] = 1
      else:
        features['deadend'] = 0

    if gameState.getAgentState(self.index).numCarrying > 3:

      features['runaway'] = 100
    else:
      features['runaway'] = 0

    # DEFENSIVE FEATURES

    features['numInvaders'] = len(pacmans)
    if len(pacmans) > 0:
      distancesFromInvaders = []
      for invader in pacmans:
        distancesFromInvaders.append(self.getMazeDistance(myPosition, invader.getPosition()))
      features['invaderDistance'] = min(distancesFromInvaders)

    fooddefenseList = self.getFoodYouAreDefending(gameState).asList()
    features['savefood'] = len(fooddefenseList)

    return features

  def getWeights(self, gameState):


    if gameState.getScore() > 0:
      return {'numInvaders': -1000, 'invaderDistance': -10, 'deadend': 0, 'runaway': 1}
    else:
      return {'successorScore': -100, 'distanceToFoodTOP': -1, 'distanceToFoodBOTTOM': -1, 'numInvaders': -100, 'invaderDistance': -10}

  def getActionValue(self, state):
    return self.evaluate(state)