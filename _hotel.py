from room import Room, RoomList
import os

class Hotel:
    def __init__(self, order=16):
        self.__room_list = RoomList(order=order)
        self.__last_guest_no = 0
        self.__primes_cache = [2, 3, 5, 7, 11, 13] # Cache for commonly used primes
        print("Empty hotel shell created. Ready to be loaded.")

    # Get primes
    def _generate_primes_up_to(self, limit):
        # Generate all prime numbers up to a given limit using the Sieve of Eratosthenes
        sieve = [True] * (limit + 1)
        sieve[0:2] = [False, False]
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        return [i for i, is_prime in enumerate(sieve) if is_prime]

    def _get_nth_prime(self, n):
        # Already cached enough
        if n <= len(self.__primes_cache):
            return self.__primes_cache[n - 1]

        import math
        #predict upper bound
        estimate = int(n * (math.log(n) + math.log(math.log(n)))) + 10
        while True:
            primes = self._generate_primes_up_to(estimate)
            if len(primes) >= n:
                self.__primes_cache = primes
                return primes[n - 1]
            estimate *= 2  # expand range if not enough primes


    def bulk_load_from_channels(self, channels: list, channel_names: list):
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
        print(">> Using the 'n -> 2n' shifting method.")
        existing_guests = self.__room_list.get_all_rooms()
        print(f"There are currently {len(existing_guests)} guests. Calculating new room arrangement...")
        for guest_room in existing_guests:
            guest_room.set_room_no(guest_room.get_room_no() * 2)
        new_guests = []
        for i in range(num_new_guests):
            guest_no = self.__last_guest_no + i + 1
            new_room_no = 2 * i + 1
            new_guests.append(Room(room_no=new_room_no, guest_no=guest_no, arrival_channel=channel))
        if new_guests:
            self.__last_guest_no = new_guests[-1].get_guest_no()
        all_guests_final = existing_guests + new_guests
        print("Rebuilding hotel structure...")
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests_final)
        print(f"SUCCESS: All {len(all_guests_final)} guests have been assigned new rooms.")
    
    def check_in_infinite_guests(self, channel: str):
        print(f"\n>> An infinite bus of new guests is arriving from channel: '{channel}'...")
        existing_guests = self.__room_list.get_all_rooms()
        num_existing_guests = len(existing_guests)
        print(f"There are currently {num_existing_guests} guests to be relocated...")
        for guest_room in existing_guests:
            guest_room.set_room_no(guest_room.get_room_no() * 2)
        new_guests = []
        for i in range(num_existing_guests):
            new_guest_no = self.__last_guest_no + i + 1
            new_room_no = 2 * i + 1
            new_guests.append(Room(room_no=new_room_no, guest_no=new_guest_no, arrival_channel=channel))
        if new_guests:
            self.__last_guest_no = new_guests[-1].get_guest_no()
        all_guests = existing_guests + new_guests
        print("Rebuilding hotel structure...")
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: The hotel now accommodates all {len(all_guests)} guests.")

    def check_in_infinite_buses_with_infinite_guests(self, num_buses_to_simulate: int, num_guests_per_bus_to_simulate: int, channel_prefix: str):
        """
        Handles infinite buses of infinite guests using the prime power method.
        """
        print(f"\n>> Simulating {num_buses_to_simulate} infinite buses with {num_guests_per_bus_to_simulate} guests each...")
        print(">> Using the Prime Power shifting method.")

        # Step 1: Get and relocate existing guests to rooms 2^n
        existing_guests = self.__room_list.get_all_rooms()
        print(f"Relocating {len(existing_guests)} existing guests to rooms of the form 2^n...")
        for guest_room in existing_guests:
            guest_room.set_room_no(2 ** guest_room.get_room_no())
        
        # Step 2: Create the simulated new guests
        new_guests = []
        guest_id_counter = self.__last_guest_no
        
        for bus_idx in range(num_buses_to_simulate):
            # The first bus (index 0) will use the 2nd prime (3).
            # The second bus (index 1) will use the 3rd prime (5), and so on.
            prime_base = self._get_nth_prime(bus_idx + 2)
            channel_name = f"{channel_prefix}_{bus_idx + 1}"
            print(f"  - Assigning guests from Bus #{bus_idx + 1} to rooms with base prime {prime_base}...")

            for guest_idx in range(1, num_guests_per_bus_to_simulate + 1):
                guest_id_counter += 1
                new_room_no = prime_base ** guest_idx
                new_guests.append(Room(room_no=new_room_no, guest_no=guest_id_counter, arrival_channel=channel_name))
        
        if new_guests:
            self.__last_guest_no = new_guests[-1].get_guest_no()

        # Step 3: Combine lists and rebuild the B+ Tree
        all_guests_final = existing_guests + new_guests
        print("\nRebuilding hotel structure with all new and relocated guests...")
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests_final)
        print(f"SUCCESS: All {len(all_guests_final)} guests are now accommodated.")

    def guest_exists(self, guest_no: int) -> bool:
        """Check if a guest ID already exists in the hotel."""
        for room in self.__room_list.get_all_rooms():
            if room.get_guest_no() == guest_no:
                return True
        return False

    def manual_add_room(self, room_no_to_add: int, guest_no: int, channel="Manual Add"):
        
        if self.guest_exists(guest_no):
            print(f"FAILED: Guest ID #{guest_no} already exists in the hotel.")
            return
        
        all_guests = self.__room_list.get_all_rooms()
        if not 1 <= room_no_to_add <= len(all_guests) + 1:
            print(f"FAILED: Room number must be between 1 and {len(all_guests) + 1}.")
            return
        new_room = Room(room_no=0, guest_no=guest_no, arrival_channel=channel)
        all_guests.insert(room_no_to_add - 1, new_room)
        if guest_no > self.__last_guest_no:
            self.__last_guest_no = guest_no
        for i, guest_room in enumerate(all_guests):
            guest_room.set_room_no(i + 1)
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: Room added. Hotel now has {len(all_guests)} rooms.")

    def manual_delete_room(self, room_no_to_delete: int):
        all_guests = self.__room_list.get_all_rooms()
        if not 1 <= room_no_to_delete <= len(all_guests):
            print(f"FAILED: Room #{room_no_to_delete} does not exist.")
            return
        deleted_guest = all_guests.pop(room_no_to_delete - 1)
        print(f"Guest #{deleted_guest.get_guest_no()} has been removed.")
        for i, guest_room in enumerate(all_guests):
            guest_room.set_room_no(i + 1)
        self.__room_list.clear()
        self.__room_list.bulk_load_rooms(all_guests)
        print(f"SUCCESS: Room removed. Hotel now has {len(all_guests)} rooms.")

    def find_guest(self, room_num) -> Room | None:
        return self.__room_list.search_by_no(room_num)
        
    def display_as_table(self):
        all_rooms = self.__room_list.get_all_rooms()
        if not all_rooms:
            print("\n--- The hotel is currently empty. ---")
            return
        print("\n--- Hotel Occupancy Report ---")
        col_widths = { "room_no": len("Room No"), "guest_no": len("Guest ID"), "channel": len("Arrival Channel") }
        for room in all_rooms:
            if len(str(room.get_room_no())) > col_widths["room_no"]: col_widths["room_no"] = len(str(room.get_room_no()))
            if len(str(room.get_guest_no())) > col_widths["guest_no"]: col_widths["guest_no"] = len(str(room.get_guest_no()))
            if len(room.get_arrival_channel()) > col_widths["channel"]: col_widths["channel"] = len(room.get_arrival_channel())
        header = f" {'Room No':<{col_widths['room_no']}} | {'Guest ID':<{col_widths['guest_no']}} | {'Arrival Channel':<{col_widths['channel']}} "
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)
        for room in all_rooms:
            row = f" {str(room.get_room_no()):<{col_widths['room_no']}} | {str(room.get_guest_no()):<{col_widths['guest_no']}} | {room.get_arrival_channel():<{col_widths['channel']}} "
            print(row)
        print(separator)
        print(f"Total Occupied Rooms: {len(all_rooms)}")
        print("------------------------------")

        
    def export_to_file(self, filename: str):
    
        all_rooms = self.__room_list.get_all_rooms()
        
        if not all_rooms:
            print("No data to export. The hotel is empty.")
            return
        
        if not filename.lower().endswith(".csv"):
            filename += ".csv"

        try:
            data = [["Room No", "Guest ID", "Arrival Channel"]]
            for room in all_rooms:
                data.append([
                        str(room.get_room_no()),
                        str(room.get_guest_no()),
                        str(room.get_arrival_channel())
                    ])
                
            column_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
            spacing = 4

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                for row in data:
                    formatted_row = []
                    for i, item in enumerate(row):
                        # Pad each item to its respective column width, then add spacing
                        formatted_row.append(str(item).ljust(column_widths[i]))
                    # Join the formatted items with the desired spacing
                    file.write((" " * spacing).join(formatted_row) + "\n")

            abs_path = os.path.abspath(filename)
            print(f" Export successful! File saved as: {abs_path}")
        
        except Exception as e:
            print(f" Error exporting file: {e}")