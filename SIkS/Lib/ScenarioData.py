##################################
#                                # 
# Author: Gavin Moore            #
# Date: 06/23/2023               #
#                                #
# File that contains definitions #
# of all data used in dataset    #
#                                #
##################################


#################################
#                               # 
# Define position/shape classes #
#                               #
#################################
class Point():
    def __init__(self, x=0, y=0) -> None:
        '''
        Barebones class that simply packages points so that we can access x and y
        coordinates of any location in space
        '''
        self.xPos = x
        self.yPos = y

class Shape():
    def __init__(self, xPos=0, yPos=0) -> None:
        '''
        Barebones shape object that only contains the position of each shape
        can be modified through sub-classes to contain a more well defined shape
        '''
        self.Position = Point(x=xPos, y=yPos)

class Circle(Shape):
    def __init__(self, radius=1, xPos=0, yPos=0) -> None:
        '''
        Subclass of shape that defines a circle shape
        '''
        super().__init__(xPos=xPos, yPos=yPos)
        self.Radius = radius
    
class Rectangle(Shape):
    def __init__(self, xPos=0, yPos=0, xLen=1, yLen=1) -> None:
        super().__init__(xPos, yPos)
        # WIP outline of how the position/lengths should relate 
        # GOAL: Keep position center of shape while adhering to side lengths
        self.TopLeft  = Point(x=xPos-(xLen/2), y=yPos-(yLen/2))
        self.BotRight = Point(x=xPos+(xLen/2), y=yPos+(yLen/2))
        
        
        
    
class Path():
    def __init__(self, pathingObject=None, interval=[], points=[]) -> None:
        '''
        This object will contain all data needed to navigate an object/shape through
        the plane via a "path" or set of points that direct the object/shape to move
        
        pathingObject => this object is the shape object that will be moving 
                         along the path
                         
        interval => this list is the time interval between each point in points; 
                    must be either the same length as points, or an integer representing
                    the standard interval for all points
                    
        points => this list is the list of points to be navigated to defining this path
        '''
        pass
    
#################################
#                               # 
# End of position/shape classes #
#                               #
#################################
    
#########################################################################################
    
#################################
#                               # 
#   Define Sensor/ROI classes   #
#                               #
#################################
    
    
class SensorData():
    def __init__(self, senseRange=0, commRange=0) -> None:
        '''
        We assume that sensor data will always consist of a circular 
        sensing/communication range but their relationship is arbitrary
        '''
        self.SensingRange = senseRange
        self.CommRange = commRange
        

class Sensor(Shape):
    def __init__(self, xPos=0, yPos=0) -> None:
        '''
        Inherits from shape so that it can contain position
        also contains a SenseData member that contains sensor data
        RemainingPower is a value representing how much energy the sensor still has
        '''
        super().__init__(xPos=xPos, yPos=yPos)
        self.SenseData = SensorData()
        self.RemainingPower = 0
        
    
    
        
    
class RegionOfInterest(Shape):
    def __init__(self) -> None:
        '''
        Object that will essentially define a shape with the property that it will
        be considered differently than other shapes as it is the "region to be covered"
        '''
        super().__init__()
        
        
