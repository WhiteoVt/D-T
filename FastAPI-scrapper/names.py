import re

def extract_ids_and_names_from_file():
    file_path = "fetched_data.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_data = file.read()

        # Updated pattern to extract id and name information
        pattern = r'<item type="boardgame" id="(\d+)">\s*<name type="primary" sortindex="1" value="([^"]+)"\s*/>\s*<name type="alternate".*?\s*value="([^"]+)"\s*/>'


        matches = re.findall(pattern, raw_data, re.MULTILINE)
        games_info = [{"id": match[0], "name": match[1]} for match in matches]

        return games_info

    except Exception as e:
        print(f"Error processing data: {e}")
        return None
