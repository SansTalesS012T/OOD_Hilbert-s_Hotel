class Room:
    def __init__(self, room_no, guest_no):
        self.__room_no  = room_no
        self.__guest_no = guest_no
    
    def get_room_no(self): return self.__room_no
    
    def get_guest_no(self): return self.__guest_no