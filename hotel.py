import src.linked_list as lib
from room import *

class Hotel:
    def __init__(self) -> None:
        self.__room_list = RoomList() # create doubly linked list named room_list

    def add_room(self, num) -> None:
        if self.search_room(num): # check if that room already has a person
            return "Full"
        else:
            self.__room_list.add_room(num)
            return f"Check in {num}"

    
    def del_room(self, num) -> None:
        pass
    
    def search_room(self, num) -> Room:
        return self.__room_list.search_by_no(num)
