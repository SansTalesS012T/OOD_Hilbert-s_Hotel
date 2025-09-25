from node import *

class DLL: # doubly linked list
    def __init__(self):
        self.__head = self.__tail = None
        self.__size = 0
        
    def size(self): return self.__size
    
    def is_empty(self): return self.__size == 0
    
    def __move(self, node, n):
        temp = node
        while(temp != None and n > 0):
            temp = temp.get_next() 
            n -= 1
        return temp
    
    def append(self, data):
        node = LLNode(data)
        if(self.is_empty()):
            self.__head = self.__tail = node
        else:
            self.__tail.set_next(node)
            self.__tail = node
        self.__size += 1
        return True
        
    def pop(self, index = None):
        if(self.is_empty()): return False
        if(index == None): index = self.__size - 1
        if(index == 0):
            self.__head = self.__head.get_next()
        else:
            temp = self.__move(self.__head, index - 1)
            temp.set_next(temp.get_next().get_next()) 
            if(index == self.__size - 1): self.__tail = temp
        self.__size -= 1
        return True
        
    def insert(self, data, index):
        if(0 > index or index > self.__size): return False
        if(index == self.__size): return self.append(data)
        node = LLNode(data)
        if(index == 0):
            node.set_next(self.__head)
            self.__head = node
        else:
            temp = self.__move(self.__head, index - 1)
            node.set_next(temp.get_next())
            temp.set_next(node)
            if(index == self.__size - 1): self.__tail = node
        self.__size += 1
        return True
        
    def remove(self, data):
        index = self.search(data)
        if(index != -1): return self.pop(index)
        return False
        
    def search(self, data):
        temp = self.__head
        n = 0
        while(temp != None and temp.data != data):
            temp = temp.get_next()
            n += 1
        return n if(temp != None) else -1   

    def clear(self):
        self.__head = self.__tail = None
        self.__size = 0
    