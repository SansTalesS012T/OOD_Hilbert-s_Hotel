import time
import os
from _hotel import Hotel

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        from track import get_process_memory
    except ImportError:
        print("Warning: 'track.py' not found. Memory usage tracking will be disabled.")
        def get_process_memory():
            return "N/A"

    hotel = Hotel()
    
    # Updated menu options
    options = [
        "Initialize Hotels",
        "Check-in Finite Group",
        "Check-in ONE Infinite Bus",
        "Check-in INFINITE Buses of INFINITE Guests",
        "Manually Add a Room",
        "Manually Delete a Room",
        "Search for a Guest by Room Number",
        "Display All Occupied Rooms",
        "Export Room List to a File",
        "Display Current Memory Usage",
        "Quit"
    ]

    while True:
        print("\n--- Hilbert's Hotel Simulation Menu ---")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        
        choice = input("\nPlease select an option: ")

        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("Invalid choice, please enter a number from the menu.")
            input("Press Enter to continue...")
            clear_screen()
            continue

        choice = int(choice)
        
        start_time = time.perf_counter()
        clear_screen()

        match choice:
            case 1:
                print("--- Initialize Hotel ---")
                try:
                    num_channels = int(input("How many arrival channels? "))
                    channels, channel_names = [], []
                    for i in range(num_channels):
                        name = input(f"Enter name for channel {i+1}: ")
                        count = int(input(f"Enter number of guests for '{name}': "))
                        channel_names.append(name)
                        channels.append(count)
                    hotel.bulk_load_from_channels(channels, channel_names)
                except ValueError:
                    print("Invalid input. Please enter a number for guest counts.")

            case 2:
                print("--- Check-in Finite Group ---")
                try:
                    num_guests = int(input("Enter number of new guests: "))
                    channel = input("Enter arrival channel name: ")
                    hotel.check_in_new_arrival(num_guests, channel)
                except ValueError:
                    print("Invalid input for number of guests.")

            case 3:
                print("--- Check-in ONE Infinite Bus ---")
                channel = input("Enter arrival channel: ")
                hotel.check_in_infinite_guests(channel)

            case 4:
                # New case for infinite buses of infinite guests
                print("--- Check-in Infinite Buses of Infinite Guests (Simulation) ---")
                print("This method moves existing guests to room 2^n and assigns new buses to powers of subsequent primes (3, 5, 7...).")
                try:
                    num_buses = int(input("Enter the number of infinite buses to SIMULATE: "))
                    num_guests_per_bus = int(input(f"Enter the number of guests per bus to SIMULATE: "))
                    prefix = input("Enter a channel name prefix (e.g., 'InfBus'): ")
                    hotel.check_in_infinite_buses_with_infinite_guests(num_buses, num_guests_per_bus, prefix)
                except ValueError:
                    print("Invalid input. Please enter numbers for the simulation counts.")

            case 5:
                print("--- Manually Add a Room ---")
                try:
                    room_no = int(input("Enter room number to add at: "))
                    guest_no = int(input("Enter a unique ID for the new guest: "))
                    hotel.manual_add_room(room_no, guest_no)
                except ValueError:
                    print("Invalid input. Please enter numbers.")

            case 6:
                print("--- Manually Delete a Room ---")
                try:
                    room_no = int(input("Enter room number to delete: "))
                    hotel.manual_delete_room(room_no)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            case 7:
                print("--- Search for a Guest ---")
                try:
                    room_no = int(input("Enter room number to search for: "))
                    guest = hotel.find_guest(room_no)
                    if guest:
                        print(f"Found: {guest}")
                    else:
                        print(f"Room #{room_no} is empty.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            case 8:
                print("--- All Occupied Rooms (Sorted) ---")
                hotel.display_as_table()

            case 9:
                print("--- Export to File ---")
                filename = input("Enter filename to save as (e.g., hotel_export.csv): ")
                hotel.export_to_file(filename)

            case 10:
                print("--- Memory Usage ---")
                memory = get_process_memory()
                if isinstance(memory, int):
                    print(f"Current memory usage: {memory:,} bytes")
                else:
                    print(f"Could not retrieve memory usage: {memory}")

            case 11:
                print("Exiting program.")
                return

        end_time = time.perf_counter()
        runtime = end_time - start_time
        print(f"\n[Function executed in {runtime:.6f} seconds]")

        input("\nPress Enter to return to the menu...")
        clear_screen()

if __name__ == "__main__":
    main()