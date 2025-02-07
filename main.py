import sys
import os

import xml.etree.ElementTree as ET
import copy

def format_xml(input_file, info_file='SaveGameInfo'):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Find the host user and farmhand users
    player_element = root.find('player')
    farmhands_element = root.find('farmhands')
    assert player_element is not None and farmhands_element is not None, "Invalid save file format"

    # Extract the player and farmhands information
    player = {
        'name': player_element.find('name').text,
        'homeLocation': player_element.find('homeLocation').text,
        'uniqueMultiplayerID': player_element.find('UniqueMultiplayerID').text
    }
    farmhands = [{
        'name': farmer.find('name').text,
        'homeLocation': farmer.find('homeLocation').text,
        'uniqueMultiplayerID': farmer.find('UniqueMultiplayerID').text
    } for farmer in farmhands_element.findall('Farmer')]

    # Print the info of the host user and farmhand users
    print(f"{'Player List':-^30}\n")
    print(f"Current Host User:")
    print(f"{player['name']} @ {player['homeLocation'][:13]} ({player['uniqueMultiplayerID'][:4]})")
    print("\nOther Users:")
    for index, farmer in enumerate(farmhands):
        print(f"{index + 1}. {farmer['name']} @ {farmer['homeLocation'][:13]} ({farmer['uniqueMultiplayerID'][:4]})")

    # Print Menu 
    print("\nWhich player should be the host user?")
    while(True):
        try:
            choice = int(input("Enter the index of the player: "))
            if choice <= 0 or choice > len(farmhands):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    print(f"Changing host user from {player['name']} to {farmhands[choice - 1]['name']}.")

    # Swap the host user and the selected farmhand user
    root.remove(player_element)
    new_player_element = copy.deepcopy(farmhands_element[choice - 1])
    new_player_element.tag = 'player'
    new_player_element.find('homeLocation').text = player['homeLocation']
    root.append(new_player_element)

    farmhands_element.remove(farmhands_element[choice - 1])
    new_farmer_element = copy.deepcopy(player_element)
    new_farmer_element.tag = 'Farmer'
    new_farmer_element.find('homeLocation').text = farmhands[choice - 1]['homeLocation']
    farmhands_element.append(new_farmer_element)

    # Swap the owner of the buildings
    # Sorry for the mess
    locations_element = root.find('locations')
    assert locations_element is not None, "Invalid save file format"
    for game_location_element in locations_element:
        buildings_element = game_location_element.find('buildings')
        for building_element in buildings_element:
            indoors_element = building_element.find('indoors')
            if indoors_element is not None:
                farmhand_reference = indoors_element.find('farmhandReference')
                if farmhand_reference is not None:
                    if farmhand_reference.text == player['uniqueMultiplayerID']:
                        farmhand_reference.text = farmhands[choice - 1]['uniqueMultiplayerID']
                    elif farmhand_reference.text == farmhands[choice - 1]['uniqueMultiplayerID']:
                        farmhand_reference.text = player['uniqueMultiplayerID']
    

    # Write the modified content to the input file
    backup_save_file(input_file)
    backup_save_file(info_file)

    # Swap the save info
    # Not Necessary
    try:
        root_info = ET.parse(info_file).getroot()
        root_info.clear()
        for child in new_player_element:
            root_info.append(child)

        rough_string = ET.tostring(root_info, 'unicode')
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(rough_string)
    except FileNotFoundError:
        pass 

    rough_string = ET.tostring(root, 'unicode')
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(rough_string)

    

def backup_save_file(file_path):
    import shutil
    import os
    if os.path.exists(file_path):
        shutil.copy(file_path, file_path + ".bak")

if __name__ == "__main__":
    try:
        print("Stardew Valley Save File Host Swapper\n")

        # Input file path
        args = sys.argv
        if len(args) == 1:
            input_file = input("Enter the path of the save file: ")
        elif len(args) == 2:
            input_file = args[1]
        else:
            print("Usage: python main.py [input_file]")
            sys.exit(1)
        
        if os.path.exists(input_file) is False:
            print("Error: The input file does not exist.")
            sys.exit(1)

        # If the path is absolute, change the working directory
        if os.path.isabs(input_file):
            os.chdir(os.path.dirname(input_file))
            input_file = os.path.basename(input_file)
        

        try:
            format_xml(input_file)
            print("Save file has been updated successfully. You can find backup file with the extension .bak.")
        except AssertionError as e:
            print(f"Error: {e}")
            print("Make sure multiple players are present in the save file.")
        except Exception as e:
            print(f"Error: {e}")
            print("An unexpected error occurred. Please try again.")

            
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
