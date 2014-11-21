__author__ = 'Wanchun Zhao'
class Player:
      def __init__(self,name,score):
        self.name = name
        self.score = score

      def getName(self):
        return self.name

      def getScore(self):
        return self.score

      def setName(self, name):
          self.name = name

      def setScore(self, score):
          self.score = score
