import json
import os

def save_to_json(screenplay_title, screenplay_content, metadata=None, output_dir="screenplays"):
    """
    Save screenplay content and metadata to a JSON file.

    Args:
        screenplay_title (str): The title of the screenplay.
        screenplay_content (str): The text content of the screenplay.
        metadata (dict, optional): Metadata related to the screenplay (e.g., year, writers). Defaults to None.
        output_dir (str, optional): The directory where the JSON file will be saved. Defaults to "screenplays".

    Raises:
        ValueError: If output_dir is not a string.
    """
    # Ensure output_dir is a valid string
    if not isinstance(output_dir, str):
        raise ValueError(f"output_dir must be a string, but got {type(output_dir)}")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Format the filename safely
    filename = f"{screenplay_title.replace(' ', '_').replace('/', '_')}.json"
    filepath = os.path.join(output_dir, filename)

    # Prepare the JSON structure
    screenplay_data = {
        "title": screenplay_title,
        "content": screenplay_content,
        "metadata": metadata or {}  # Default to an empty dictionary if metadata is None
    }

    # Save the JSON file
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(screenplay_data, json_file, indent=4)

    print(f"Screenplay '{screenplay_title}' saved to {filepath}")


