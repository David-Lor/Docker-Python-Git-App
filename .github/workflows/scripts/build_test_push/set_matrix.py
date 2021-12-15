"""SET MATRIX Script
This script sets output variables for the build_test_push.yaml Github Workflow, using the images defined in images.json.

The two outputs are:
- images: the images.json file JSON content as-is, without line breaks
- archs: a JSON array of strings, with all the available archs, fetched from all the images defined on images.json
"""

import os
import json

IMAGES_FILE = os.getenv("IMAGES_FILE", "images.json")
OUTPUT_IMAGES_KEY = os.getenv("OUTPUT_IMAGES_ENV", "images")
OUTPUT_ARCHS_KEY = os.getenv("OUTPUT_ARCHS_KEY", "archs")


def export_variable(key, value):
    print(f"::set-output name={key}::{value}")


def load_images_file() -> list:
    with open(IMAGES_FILE, "r") as f:
        return json.load(f)


def export_images_variable(images_data: list):
    value = json.dumps(images_data)
    export_variable(OUTPUT_IMAGES_KEY, value)


def export_archs_variable(images_data: list):
    archs = set()
    for image in images_data:
        image_archs = image["archs"]
        archs.update(image_archs)

    archs = list(archs)
    value = json.dumps(archs)
    export_variable(OUTPUT_ARCHS_KEY, value)


def main():
    images = load_images_file()
    export_images_variable(images)
    export_archs_variable(images)


if __name__ == '__main__':
    main()
