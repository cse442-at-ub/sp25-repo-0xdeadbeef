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

def delete_save(slot):
    file_path = os.path.join(SAVE_DIR, f"save{slot}.json")
    if os.path.exists(file_path):
        os.remove(file_path)

def deleteAll():
    for file in os.listdir(SAVE_DIR):
        file_path = os.path.join(SAVE_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

# Delete all if needed 
# if __name__ == "__main__":
#     deleteAll()