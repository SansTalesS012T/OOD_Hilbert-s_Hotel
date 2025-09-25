class TreeNode:
    def __init__(self, data):
        self.__data = data
        self.__prev = self.__right = None 
        
    def get_data(self): return self.__data
    def set_data(self, data): self.__data = data
    
    def get_left(self): return self.__left
    def set_left(self, left): self.__left = left 
    
    def get_right(self): return self.__right 
    def set_right(self, right): self.__right = right

class LLNode:
    def __init__(self, data):
        self.__data = data
        self.__prev = self.__next = None 
        
    def get_data(self): return self.__data
    def set_data(self, data): self.__data = data
    
    def get_prev(self): return self.__prev
    def set_prev(self, prev): self.__prev = prev 
    
    def get_next(self): return self.__next 
    def set_next(self, next): self.__next = next