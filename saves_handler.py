import os
import json

SAVE_DIR = "User Saves"  # Directory to store save files

# Check if save slot json exist in directory
def check_save(slot):
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")
    return os.path.exists(file_path)

# Load data from a save slot number
def load_save(slot):
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)  # Return save data as a dictionary
    return None  # No save file exists

def create_new_save(slot):
    """Create a new save file with default values."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)  # Create directory if it doesn't exist
    
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")
    default_data = {
        "slot": slot,
        "character": "directory",
    }
    with open(file_path, "w") as file:
        json.dump(default_data, file, indent=4)
    
    return default_data  # Return newly created data

def update_save(slot, new_data):
    """Update the save file with new data for the given slot."""
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")

    # Load existing save data
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            save_data = json.load(file)
    else:
        print(f"Save file for slot {slot} does not exist. Creating a new save...")
        save_data = create_new_save(slot)  # Create new save if it doesn't exist

    # Update the save data with new values
    save_data.update(new_data)  

    # Save the updated data back to the file
    with open(file_path, "w") as file:
        json.dump(save_data, file, indent=4)
    
    print(f"Save Slot {slot} updated successfully!")

def achievement_counter(slot, level_info):
    # Update achievment counter when level completed
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")

    # Load existing data 
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            save_data = json.load(file)

    else:
        print(f"Save file for slot {slot} does not exist. Creating a new save...")
        save_data = create_new_save(slot)  # Create new save if it doesn't exist

    #Check if level already cleared
    if level_info not in save_data:
        level_first_clear = {level_info: 1}
        save_data.update(level_first_clear)
        print(f"First time clearing {level_info}!")

    else: 
        number_of_clears = save_data[level_info]
        level_updated_clear = {level_info: number_of_clears + 1}
        save_data.update(level_updated_clear) 
    
    with open(file_path, "w") as file:
        json.dump(save_data, file, indent=4)
    
    print(f"{level_info} counter updated successfully")


def eclipse_increment(slot, coin_count):

    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")

    # Load existing data 
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            save_data = json.load(file)

    else:
        print(f"Save file for slot {slot} does not exist. Creating a new save...")
        save_data = create_new_save(slot)  # Create new save if it doesn't exist

    #Check if eclipse counter is started 
    if "Eclipse" not in save_data:
        start_eclipse_counter = {"Eclipse": coin_count}
        save_data.update(start_eclipse_counter)
        print("First Eclipse Collection!")

    else:
        number_of_eclipses = save_data["Eclipse"]
        update_eclipse_counter = {"Eclipse": number_of_eclipses + coin_count}
        save_data.update(update_eclipse_counter)

    with open(file_path, "w") as file:
        json.dump(save_data, file, indent=4)

    print("Eclipse counter updated")
        


def delete_save(slot):
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")
    if os.path.exists(file_path):
        os.remove(file_path)