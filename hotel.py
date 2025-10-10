from room import Room, RoomList

class Hotel:
    def __init__(self, bpt_order=4) -> None:
        self.__room_list = RoomList(order=bpt_order)
    
    def bulk_load(self, num_rooms: int):
        # Creates and bulk loads a specified number of rooms into the hotel
        print(f"Preparing {num_rooms} rooms for bulk loading...")
        rooms_to_load = [Room(room_no=i, guest_no=i) for i in range(num_rooms)]
        
        self.__room_list.bulk_load_rooms(rooms_to_load)
        print(f"SUCCESS: Bulk loaded {num_rooms} rooms.") 
    
    
    def check_in(self, room_num, guest_num=None):
        if guest_num is None:
            guest_num = room_num

        if self.__room_list.search_by_no(room_num):
            print(f"FAILED: Room {room_num} is already occupied.")
            return "Full"
        
        # If vacant, create a new Room object and add it to the RoomList
        new_room = Room(room_num, guest_num)
        self.__room_list.add_room(new_room)
        print(f"SUCCESS: Guest {guest_num} checked into Room {room_num}.")
        return f"Check in {room_num}"

    def check_out(self, room_num) -> str:
        """Checks a guest out of a room, making it vacant."""
        # First, check if the room exists
        if not self.__room_list.search_by_no(room_num):
            print(f"FAILED: Room {room_num} is not occupied or does not exist.")
            return "Not Found"
        
        # If it exists, delete it
        self.__room_list.del_room(room_num)
        print(f"SUCCESS: Room {room_num} is now vacant.")
        return f"Check out {room_num}"
    
    def find_guest(self, room_num) -> Room | None:
        """Finds the details of a room by its number."""
        room = self.__room_list.search_by_no(room_num)
        if room:
            print(f"FOUND: {room}")
        else:
            print(f"NOT FOUND: Room {room_num} is vacant or does not exist.")
        return room
    
    def display_occupancy(self):
        """Displays the internal B+ Tree structure for debugging."""
        self.__room_list.display_tree()