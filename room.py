class Room:
    def __init__(self, room_no, guest_no):
        self.__room_no  = room_no
        self.__guest_no = guest_no
    
    def get_room_no(self): return self.__room_no
    
    def get_guest_no(self): return self.__guest_no
    
    def same_room_no(self, room_no): return self.__room_no == room_no 
    
    def same_guest_no(self, guest_no): return self.__guest_no == guest_no

import src.linked_list as lib
class RoomList(lib.DLL):
    def __init__(self):
        super.__init__()
    
    def search_by_no(self, num)-> Room | None:
        current = self.get_head()
        while current:
            room: Room = current.get_data()
            if room.get_room_no() == num:
               return room
            current = current.get_next()
        return None
        
    def del_room(self, num):
        temp = self.get_head()
        # while(temp != )
