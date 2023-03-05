from pathlib import Path
import json


def json_write(resources, filename):
    with open(filename, "w", encoding="UTF8") as file:
        json.dump(resources, file, indent=4)

    return "File written to: " + str(Path(filename).absolute())
