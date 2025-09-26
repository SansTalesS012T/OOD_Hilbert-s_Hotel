class Room:
    def __init__(self, room_no, guest_no):
        self.__room_no  = room_no
        self.__guest_no = guest_no
    
    def get_room_no(self): return self.__room_no
    
    def get_guest_no(self): return self.__guest_no
    
    def is_same_room_no(self, room_no): return self.__room_no == room_no 
    
    def is_same_guest_no(self, guest_no): return self.__guest_no == guest_no

import src.linked_list as lib
class RoomList(lib.DLL):
    def __init__(self):
        super.__init__()
    
    def add_room(self, num):   
        room = Room(num, num)
        temp = self.get_head()
        room_index = 0
        if self.is_empty():
            self.append(room)
            return
        while temp.get_next():  # move until get index before room to set
            if temp.get_next().get_data().get_room_no() < num:
                room_index += 1
                temp = temp.get_next()
        self.insert(room, room_index)
        return
    
    def search_by_no(self, num)-> Room | None:
        current = self.get_head()
        while current:
            room: Room = current.get_data()
            if room.is_same_room_no(num):
               return room
            current = current.get_next()
        return None
        
    def del_room(self, num):
        temp = self.get_head()
        while(temp != None):
            if(temp.get_data().is_same_room_no(num)):
                prev, next = temp.get_prev(), temp.get_next()
                if(prev == None): # head node
                    self.pop(0)
                elif(next == None): # tail node
                    self.pop()
                else: # middle node
                    prev.set_next(next)
                    next.set_prev(prev)
                return
            temp = temp.get_next()