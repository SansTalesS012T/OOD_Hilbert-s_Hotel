class Node:
    def __init__(self, data):
        self.__data = data
        self.__left = self.__right = None 
        
    def getData(self): return self.__data
    def setData(self, data): self.__data = data
    
    def getLeft(self): return self.__left
    def setLeft(self, left): self.__left = left 
    
    def getRight(self): return self.__right 
    def setRight(self, right): self.__right = right