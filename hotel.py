from room import Room, RoomList

class Hotel:
    def __init__(self, order=16):
        self.__room_list = RoomList(order=order)
        self.__last_guest_no = 0
        print("Empty hotel shell created. Ready to be loaded.")

    def bulk_load_from_channels(self, channels: list, channel_names: list):
        """Builds the entire hotel at once from a list of guest counts per channel."""
        if len(channels) != len(channel_names):
            print("Error: The 'channels' and 'channel_names' lists must be the same size.")
            return

        self.__room_list.clear()
        self.__last_guest_no = 0
        
        total_rooms = sum(channels)
        print(f"Starting bulk load for a new hotel with {total_rooms} rooms...")

        rooms_to_load = []
        guest_count = 1
        for i, num_guests in enumerate(channels):
            channel_name = channel_names[i]
            for _ in range(num_guests):
                new_room = Room(room_no=guest_count, guest_no=guest_count, arrival_channel=channel_name)
                rooms_to_load.append(new_room)
                guest_count += 1
        
        if rooms_to_load:
            self.__last_guest_no = rooms_to_load[-1].get_guest_no()
            self.__room_list.bulk_load_rooms(rooms_to_load)
        
        print("SUCCESS: Hotel has been fully loaded with all guests.")
    
    
    def check_in_new_arrival(self, num_new_guests: int, channel: str):
        print(f"\n>> {num_new_guests} new guests arriving from channel: '{channel}'...")

        existing_guests = self.__room_list.get_all_rooms()
        print(f"There are currently {len(existing_guests)} guests in the hotel.")

        new_guests = []
        for i in range(num_new_guests):
            guest_no = self.__last_guest_no + i + 1
            new_guests.append(Room(room_no=0, guest_no=guest_no, arrival_channel=channel))

        if new_guests:
            self.__last_guest_no = new_guests[-1].get_guest_no()
    
        all_guests = existing_guests + new_guests
        for i, guest_room in enumerate(all_guests):
            guest_room.set_room_no(i + 1)
            
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
    
        print(f"SUCCESS: All {len(all_guests)} guests have been assigned new rooms.")
    
    def check_in_infinite_guests(self, channel: str):
        """
        Handles 'infinite' arrivals by shifting existing guests from room 'n' to '2n'
        and filling the vacant odd-numbered rooms.
        """
        print(f"\n>> An infinite bus of new guests is arriving from channel: '{channel}'...")
        existing_guests = self.__room_list.get_all_rooms()
        num_existing_guests = len(existing_guests)
        print(f"There are currently {num_existing_guests} guests to be relocated.")

        # Re-assign old guests to room '2n'.
        for guest_room in existing_guests:
            current_room_no = guest_room.get_room_no()
            guest_room.set_room_no(current_room_no * 2)

        # Create new guests and assign them to the odd-numbered rooms.
        new_guests = []
        for i in range(num_existing_guests):
            new_guest_no = self.__last_guest_no + i + 1
            new_room_no = 2 * i + 1  # Generates odd numbers: 1, 3, 5, ...
            new_guests.append(Room(room_no=new_room_no, guest_no=new_guest_no, arrival_channel=channel))
        
        # Update the tracker with the new highest guest ID.
        if new_guests:
            self.__last_guest_no = new_guests[-1].get_guest_no()

        all_guests = existing_guests + new_guests
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: The hotel now accommodates all {len(all_guests)} guests.")
 
    # Inserts a new guest at a specific room number, shifting all subsequent guests up.
    def manual_add_room(self, room_no_to_add: int, guest_no: int, channel="Manual Add"):
        print(f"\n>> Manually adding Guest #{guest_no} at Room #{room_no_to_add}...")

        all_guests = self.__room_list.get_all_rooms()

        if not 1 <= room_no_to_add <= len(all_guests) + 1:
            print(f"FAILED: Room number must be between 1 and {len(all_guests) + 1}.")
            return

        new_room = Room(room_no=0, guest_no=guest_no, arrival_channel=channel)
        insert_index = room_no_to_add - 1
        all_guests.insert(insert_index, new_room)

        if guest_no > self.__last_guest_no:
            self.__last_guest_no = guest_no
            
        # Re-number all rooms sequentially to create the "shift" effect
        for i, guest_room in enumerate(all_guests):
            guest_room.set_room_no(i + 1)
        
        # Rebuild the B+ Tree with the new, shifted arrangement
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: Room added. Hotel now has {len(all_guests)} rooms.")

    def manual_delete_room(self, room_no_to_delete: int):
        """Deletes a guest from a specific room, shifting all subsequent guests down."""
        print(f"\n>> Manually deleting Room #{room_no_to_delete}...")

        all_guests = self.__room_list.get_all_rooms()
        
        if not 1 <= room_no_to_delete <= len(all_guests):
            print(f"FAILED: Room #{room_no_to_delete} does not exist.")
            return

        deleted_guest = all_guests.pop(room_no_to_delete - 1)
        print(f"Guest #{deleted_guest.get_guest_no()} has been removed.")

        # Re-number all remaining rooms sequentially to fill the gap
        for i, guest_room in enumerate(all_guests):
            guest_room.set_room_no(i + 1)
        
        # Rebuild the B+ Tree
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: Room removed. Hotel now has {len(all_guests)} rooms.")

    def find_guest(self, room_num) -> Room | None:
        return self.__room_list.search_by_no(room_num)

    def display_occupancy(self):
        self.__room_list.display_rooms_list()
        

    def display_as_table(self):
        all_rooms = self.__room_list.get_all_rooms()

        if not all_rooms:
            print("\n--- The hotel is currently empty. ---")
            return

        print("\n--- Hotel Occupancy Report ---")
        
        col_widths = {
            "room_no": len("Room No"),
            "guest_no": len("Guest ID"),
            "channel": len("Arrival Channel")
        }
        
        for room in all_rooms:
            if len(str(room.get_room_no())) > col_widths["room_no"]:
                col_widths["room_no"] = len(str(room.get_room_no()))
            if len(str(room.get_guest_no())) > col_widths["guest_no"]:
                col_widths["guest_no"] = len(str(room.get_guest_no()))
            if len(room.get_arrival_channel()) > col_widths["channel"]:
                col_widths["channel"] = len(room.get_arrival_channel())
        
        header = (
            f" {'Room No':<{col_widths['room_no']}} |"
            f" {'Guest ID':<{col_widths['guest_no']}} |"
            f" {'Arrival Channel':<{col_widths['channel']}} "
        )
        separator = "-" * len(header)
        
        print(separator)
        print(header)
        print(separator)

        for room in all_rooms:
            row = (
                f" {str(room.get_room_no()):<{col_widths['room_no']}} |"
                f" {str(room.get_guest_no()):<{col_widths['guest_no']}} |"
                f" {room.get_arrival_channel():<{col_widths['channel']}} "
            )
            print(row)

        print(separator)
        print(f"Total Occupied Rooms: {len(all_rooms)}")
        print("------------------------------")