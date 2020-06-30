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
               first='MyOffensiveAgent', second='MyDefensiveAgent'):
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
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########


class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

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

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

class MyDefensiveAgent(ReflexCaptureAgent):

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myPosition = successor.getAgentState(self.index).getPosition()
    enemies = []
    for opponent in self.getOpponents(successor):
      enemies.append(successor.getAgentState(opponent))

    invaders = []
    for enemy in enemies:
      if enemy.isPacman and enemy.getPosition() != None:
        invaders.append(enemy)
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:  # ima nekoga na nasoj strani, idi u defense
      offensive = False
      distancesToInvaders = []
      for invader in invaders:
        distance = self.getMazeDistance(myPosition, invader.getPosition())
        distancesToInvaders.append(distance)
      features['invaderDistance'] = min(distancesToInvaders)
    return features


  def getWeights(self, gameState, action):
    return {'numInvaders': -1000,
            'invaderDistance': -5}


class MyOffensiveAgent(ReflexCaptureAgent):

  def getFeatures(self, gameState, action):
    pass

  def getWeights(self, gameState, action):
    pass

