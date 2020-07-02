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

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in legalActions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return legalActions[actionValues.index(best)]

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState):

    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):

    #inicijalizacija svega
    features = util.Counter()
    capsules = gameState.getCapsules()
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

    #features vezani za uzimanje hrane
    if len(foodList) != 0:
      if self.index > 1:
        distancesFromFood = []
        if (len(topFoodList) != 0):
          for food in topFoodList:
            distance = self.getMazeDistance(myPosition, food)
            distancesFromFood.append(distance)
          minDistance = min(distancesFromFood)
          features['distanceToFood'] = minDistance
        else:
          for food in botFoodList:
            distance = self.getMazeDistance(myPosition, food)
            distancesFromFood.append(distance)
          minDistance = min(distancesFromFood)
          features['distanceToFood'] = minDistance
      else:
        distancesFromFood = []
        if (len(botFoodList) != 0):
          for food in botFoodList:
            distance = self.getMazeDistance(myPosition, food)
            distancesFromFood.append(distance)
          minDistance = min(distancesFromFood)
          features['distanceToFood'] = minDistance
        else:
          for food in topFoodList:
            distance = self.getMazeDistance(myPosition, food)
            distancesFromFood.append(distance)
          minDistance = min(distancesFromFood)
          features['distanceToFood'] = minDistance

    #defensive features
    features['numInvaders'] = len(pacmans)
    if len(pacmans) > 0 and gameState.getAgentState(self.index).scaredTimer <= 10:
      distancesFromInvaders = []
      for invader in pacmans:
        distancesFromInvaders.append(self.getMazeDistance(myPosition, invader.getPosition()))
      features['invaderDistance'] = min(distancesFromInvaders)

    #features za bjezanje ako je pri napadanju duh blizu
    if len(ghosts) > 0 and gameState.getAgentState(self.index).isPacman:
      distancesFromGhosts = []
      #distancesManhattan = []
      for ghost in ghosts:
        distancesFromGhosts.append(self.getMazeDistance(myPosition, ghost.getPosition()))
      if min(distancesFromGhosts) < 7:
        if ghosts[distancesFromGhosts.index(min(distancesFromGhosts))].scaredTimer == 0:
          features['ghostDistance'] = min(distancesFromGhosts)

    return features

  def getWeights(self, gameState):

    if gameState.getScore() > 0:
      return {'ghostDistance': -2500,'numInvaders': -1000, 'invaderDistance': -10}
    else:
      return {'ghostDistance': -2500,'successorScore': -100, 'distanceToFood': -1, 'numInvaders': -100, 'invaderDistance': -10}

  def getActionValue(self, state):
    return self.evaluate(state)
