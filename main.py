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
        "Hotel Setup and Room Management",
        "Check in ",
        "Search for a Guest and Display Rooms",
        "Rearrange room no.",
        "Export Room List to a File",
        "Display Current Memory Usage",
        "Quit"
    ]

    Hotel_Setup_and_Room_Managements = [
        "Initialize Hotel",
        "Manually Add a Room",
        "Manually Delete a Room",
        "Quit"

    ]
    check_ins = [
        "Check-in Finite Group",
        "Check-in ONE Infinite Bus",
        "Check-in Infinite Buses of Infinite Guests (Simulation)",
        "Quit"
    ]
    
    Search_for_a_Guest_and_Display_Rooms = [
        "Search for a Guest",
        "Display All Occupied Rooms",
        "Quit"
    ]
    

    while True:
        print(r"""
$$\   $$\ $$\ $$\ $$\                            $$\  $$\                $$\   $$\            $$\               $$\ 
$$ |  $$ |\__|$$ |$$ |                           $$ | $  |               $$ |  $$ |           $$ |              $$ |
$$ |  $$ |$$\ $$ |$$$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\\_/ $$$$$$$\       $$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\  $$ |
$$$$$$$$ |$$ |$$ |$$  __$$\ $$  __$$\ $$  __$$\\_$$  _|  $$  _____|      $$$$$$$$ |$$  __$$\\_$$  _|  $$  __$$\ $$ |
$$  __$$ |$$ |$$ |$$ |  $$ |$$$$$$$$ |$$ |  \__| $$ |    \$$$$$$\        $$  __$$ |$$ /  $$ | $$ |    $$$$$$$$ |$$ |
$$ |  $$ |$$ |$$ |$$ |  $$ |$$   ____|$$ |       $$ |$$\  \____$$\       $$ |  $$ |$$ |  $$ | $$ |$$\ $$   ____|$$ |
$$ |  $$ |$$ |$$ |$$$$$$$  |\$$$$$$$\ $$ |       \$$$$  |$$$$$$$  |      $$ |  $$ |\$$$$$$  | \$$$$  |\$$$$$$$\ $$ |
\__|  \__|\__|\__|\_______/  \_______|\__|        \____/ \_______/       \__|  \__| \______/   \____/  \_______|\__|                                                                                                                                                                                                                                                                                                                                                   
""")


        print("--- Hilbert's Hotel Simulation Menu ---")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        
        choice = input("\nPlease select an option: ")

        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("Invalid choice, please enter a number from the menu.")
            input("Press Enter to continue...")
            clear_screen()
            continue

        choice = int(choice)
        clear_screen()

        
        match choice:
            case 1:
                print("--- Hotel_Setup_and_Room_Management ---")
                for i, Hotel_Setup_and_Room_Management in enumerate(Hotel_Setup_and_Room_Managements):
                    print(f"{i + 1}. {Hotel_Setup_and_Room_Management}")

                Hotel_Setup_and_Room_Management_choice = input("Please select option: ").strip()

                if not Hotel_Setup_and_Room_Management_choice.isdigit() or not 1 <= int(Hotel_Setup_and_Room_Management_choice) <= len(Hotel_Setup_and_Room_Managements):
                    print("Invalid choice, please enter a number from the list.")
                    input("Press Enter to continue...")
                    clear_screen()
                    continue

                Hotel_Setup_and_Room_Management_choice = int(Hotel_Setup_and_Room_Management_choice)
                clear_screen()
            

                match Hotel_Setup_and_Room_Management_choice:
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
                            start_time = time.perf_counter()
                            hotel.bulk_load_from_channels(channels, channel_names)
                            end_time = time.perf_counter()
                        except ValueError:
                            print("Invalid input. Please enter a number for guest counts.")

                    case 2:
                        print("--- Manually Add a Room ---")
                        try:
                            room_no = int(input("Enter room number to add at: "))
                            guest_no = int(input("Enter a unique ID for the new guest: "))
                            start_time = time.perf_counter()
                            hotel.manual_add_room(room_no, guest_no)
                            end_time = time.perf_counter()
                        except ValueError:
                            print("Invalid input. Please enter numbers.")

                    case 3:
                        print("--- Manually Delete a Room ---")
                        try:
                            room_no = int(input("Enter room number to delete: "))
                            start_time = time.perf_counter()
                            hotel.manual_delete_room(room_no)
                            end_time = time.perf_counter()
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    case 4:
                        print("Exiting program.")
                        continue
            case 2:
                print("--- Check-in Options ---")
                for i, check_in_option in enumerate(check_ins):
                    print(f"{i + 1}. {check_in_option}")

                check_in_choice = input("Please select a check-in option: ").strip()

                if not check_in_choice.isdigit() or not 1 <= int(check_in_choice) <= len(check_ins):
                    print("Invalid choice, please enter a number from the list.")
                    input("Press Enter to continue...")
                    clear_screen()
                    continue

                check_in_choice = int(check_in_choice)
                clear_screen()

                match check_in_choice:
                    case 1:
                        print("--- Check-in Finite Group ---")
                        try:
                            num_guests = int(input("Enter number of new guests: "))
                            channel = input("Enter arrival channel name: ")
                            start_time = time.perf_counter()
                            hotel.check_in_new_arrival(num_guests, channel)
                            end_time = time.perf_counter()
                        except ValueError:
                            print("Invalid input for number of guests.")

                    case 2:
                        print("--- Check-in ONE Infinite Bus ---")
                        channel = input("Enter arrival channel: ")
                        start_time = time.perf_counter()
                        hotel.check_in_infinite_guests(channel)
                        end_time = time.perf_counter()

                    case 3:
                        print("--- Check-in Infinite Buses of Infinite Guests (Simulation) ---")
                        print("Simulates infinite buses by assigning each bus and guest to unique rooms.")
                        try:
                            num_buses = int(input("Enter the number of infinite buses to SIMULATE: "))
                            # num_guests_per_bus = int(input("Enter the number of guests per bus to SIMULATE: "))
                            num_guests_of_each_bus = []
                            for i in range(num_buses):
                                num_guests_of_each_bus.append(int(input(f"Enter amount of guest in bus {i + 1}: ")))
                            prefix = input("Enter a channel name prefix (e.g., 'InfBus'): ")
                            start_time = time.perf_counter()
                            hotel.check_in_infinite_buses_with_infinite_guests(
                                num_buses, num_guests_of_each_bus, prefix
                            )
                            end_time = time.perf_counter()
                        except ValueError:
                            print("Invalid input. Please enter numbers for the simulation counts.")
                    case 4:
                        print("Exiting program.")
                        continue

            case 3:
                print("--- Search_for_a_Guest_and_Display_Room ---")
                for i, Search_for_a_Guest_and_Display_Room in enumerate(Search_for_a_Guest_and_Display_Rooms):
                    print(f"{i + 1}. {Search_for_a_Guest_and_Display_Room}")

                Search_for_a_Guest_and_Display_Room_choice = input("Please select option: ").strip()

                if not Search_for_a_Guest_and_Display_Room_choice.isdigit() or not 1 <= int(Search_for_a_Guest_and_Display_Room_choice) <= len(Search_for_a_Guest_and_Display_Rooms):
                    print("Invalid choice, please enter a number from the list.")
                    input("Press Enter to continue...")
                    clear_screen()
                    continue

                Search_for_a_Guest_and_Display_Room_choice = int(Search_for_a_Guest_and_Display_Room_choice)
                clear_screen()
            

                match Search_for_a_Guest_and_Display_Room_choice:
                    case 1:
                        print("--- Search for a Guest ---")
                        try:
                            room_no = int(input("Enter room number to search for: "))
                            start_time = time.perf_counter()
                            guest = hotel.find_guest(room_no)
                            end_time = time.perf_counter()
                            if guest:
                                print(f"Found: {guest}")
                            else:
                                print(f"Room #{room_no} is empty.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    case 2:
                        print("--- All Occupied Rooms (Sorted) ---")
                        start_time = time.perf_counter()
                        hotel.display_as_table()
                        end_time = time.perf_counter()
                    case 3:
                        print("Exiting program.")
                        continue
            
            case 4:
                print("--- Rearranging all room in hotel ---")
                start_time = time.perf_counter()
                hotel.rearrange()
                end_time = time.perf_counter()

            case 5:
                print("--- Export to File ---")
                filename = input("Enter filename to save as (e.g., hotel_export.csv): ")
                start_time = time.perf_counter()
                hotel.export_to_file(filename)
                end_time = time.perf_counter()
            
            case 6:
                print("--- Memory Usage ---")
                start_time = time.perf_counter()
                memory = get_process_memory()
                end_time = time.perf_counter()
                
                if isinstance(memory, int):
                    pref = {"GB": 10**9, "MB": 10**6, "KB": 10**3, "B": 1}
                    show = [None, None]
                    for i, j in pref.items():
                        if(memory / j >= 1):
                            show[0], show[1] = memory / j, i
                            break
                    print(f"Current memory usage: {show[0]:,.3f} {show[1]}")
                else:
                    print(f"Could not retrieve memory usage: {memory}")

            case 7:
                print("Exiting program.")
                return

        
        runtime = end_time - start_time
        print(f"\n[Function executed in {runtime:.6f} seconds]")

        input("\nPress Enter to return to the menu...")
        clear_screen()

if __name__ == "__main__":
    main()