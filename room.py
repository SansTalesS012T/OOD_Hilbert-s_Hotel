# import src.linked_list as lib
import src.B_plus_Tree as BPT

class Room:
    def __init__(self, room_no, guest_no):
        self.__room_no  = room_no
        self.__guest_no = guest_no
    
    def get_room_no(self): 
        return self.__room_no
    
    def get_guest_no(self): 
        return self.__guest_no
    
    def __str__(self):
        # A helper method to make printing Room objects more readable.
        return f"Room(No: {self.__room_no}, Guest: {self.__guest_no})"

class RoomList(BPT.BPTree):
    def __init__(self, order=4):
        self.__bptree = BPT.BPTree(order)

    def add_room(self, room: Room):
        self.__bptree.insert(room.get_room_no(), room)
    
    def search_by_no(self, room_num) -> Room | None:
        return self.__bptree.search(room_num)
        
    def del_room(self, room_num):
        self.__bptree.delete(room_num)
        
    def bulk_load_rooms(self, rooms: list):
        # Prepares room data and performs a bulk load on the B+ Tree.
        # The B+ Tree's bulk_load expects a list of (key, value) tuples.
        data_to_load = [(room.get_room_no(), room) for room in rooms]
        self.__bptree.bulk_load(data_to_load)
        

    # Util for display --Debugger--
    def display_tree(self):
        print("--- Hotel B+ Tree Structure ---")
        self.__bptree.display_tree_ascii()
        print("-----------------------------")



# class Room:
#     def __init__(self, room_no, guest_no):
#         self.__room_no  = room_no
#         self.__guest_no = guest_no
    
#     def get_room_no(self): return self.__room_no
    
#     def get_guest_no(self): return self.__guest_no
    
#     def is_same_room_no(self, room_no): return self.__room_no == room_no 
    
#     def is_same_guest_no(self, guest_no): return self.__guest_no == guest_no

# class RoomList(lib.DLL):
#     def __init__(self):
#         super.__init__()
    
#     def add_room(self, num):   
#         room = Room(num, num)
#         temp = self.get_head()
#         room_index = 0
#         if self.is_empty():
#             self.append(room)
#             return
#         while temp.get_next():  # move until get index before room to set
#             if temp.get_next().get_data().get_room_no() < num:
#                 room_index += 1
#                 temp = temp.get_next()
#         self.insert(room, room_index)
#         return
    
#     def search_by_no(self, num)-> Room | None:
#         current = self.get_head()
#         while current:
#             room: Room = current.get_data()
#             if room.is_same_room_no(num):
#                return room
#             current = current.get_next()
#         return None
        
#     def del_room(self, num):
#         temp = self.get_head()
#         while(temp != None):
#             if(temp.get_data().is_same_room_no(num)):
#                 prev, next = temp.get_prev(), temp.get_next()
#                 if(prev == None): # head node
#                     self.pop(0)
#                 elif(next == None): # tail node
#                     self.pop()
#                 else: # middle node
#                     prev.set_next(next)
#                     next.set_prev(prev)
#                 return
#             temp = temp.get_next()
