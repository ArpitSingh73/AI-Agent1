"""
module to save chat history
"""

import json
import os


# Check if file exists
def save_context(new_entry, filename="context.json"):
    try:
        if os.path.isfile(filename):
            # Read existing data
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Append new chat
        data.append(new_entry)

        # Write updated list back to file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print("Error occcured while saving context: ", e)
