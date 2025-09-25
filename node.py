class Node:
    def __init__(self, data):
        self.__data = data
        self.__left = self.__right = None 
        
    def get_data(self): return self.__data
    def set_data(self, data): self.__data = data
    
    def get_left(self): return self.__left
    def set_left(self, left): self.__left = left 
    
    def get_right(self): return self.__right 
    def set_right(self, right): self.__right = right