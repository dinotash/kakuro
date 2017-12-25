#!/usr/local/bin/Python3

"""
Finds new puzzles in the database and updates them with image details.
"""

import logging
import re
from io import BytesIO
import requests
import bs4
from PIL import Image
import logger
from datastore_client import DatastoreClient
from kakurizer_types import ImageMetadata

def find():
    """
    Updates all puzzles in the database for which we don't yet have an image.
    """
    logger.setup_logger()
    datastore = DatastoreClient()
    for entity in datastore.get_index_puzzles():
        update_puzzle_with_image(datastore, entity)


def update_puzzle_with_image(datastore, entity):
    """
    Updates existing database entity with details of the puzzle image and saves an update.

    :param datastore: datastore_client.DatastoreClient for accessing Google Cloud Datastore
    :param entity: the database entry to be updated
    :returns: None
    """
    logging.getLogger().info("Finding image for puzzle %s", entity['id'])
    url = __extract_img_url(entity)
    blob = __get_img_blob(url)
    metadata = __get_img_metadata(blob)

    entity['has_img'] = True
    entity['img_url'] = url
    entity['img_blob'] = blob
    entity.exclude_from_indexes = ('img_blob',)
    entity['img_width'] = metadata.width
    entity['img_height'] = metadata.height
    entity['img_format'] = metadata.format

    datastore.update(entity)


def __extract_img_url(entity):
    """
    Extracts the URL pointing to the puzzle image for a given puzzle.

    :param entity: database entry representing a puzzle
    :returns: url as a string pointing to the image
    :raises ValueError: if there are no
    """
    puzzle_page = requests.get(entity['page_url'])
    puzzle_html = bs4.BeautifulSoup(puzzle_page.text, "html.parser")
    sources = puzzle_html.find_all("source")
    widest_sources = sorted(sources, key=lambda x: x.attrs['sizes'], reverse=True)
    try:
        raw_url = widest_sources[0].attrs['srcset']
        url = re.search("([^ ]*) .*", raw_url).group(1).replace("&amp;", "&")
        return url
    except IndexError:
        raise ValueError("No possible image URLs found for puzzle " + str(entity['id']) 
            + " on page " + entity['page_url'])


def __get_img_blob(url):
    """
    Loads a puzzle image from the Guardian and converts it to blob format for
    storage in the database.

    I realize that there are some latency downsides to storing images in databses, but it
    seemed appropriate here because:
     - the image files are small (under 40kb)
     - no longer reliant on retrieving new copies from the Guardian who could change
       their url schema or what's available
     - we won't be serving the live image to users
     - the images will be used in a pipeline which needs to access the db anyway
     - want to keep images in line with their metadata

     :param url: string url of the image's location
     :returns: image as a series of bytes
    """
    img_request = requests.get(url)
    return img_request.content


def __get_img_metadata(image_bytes):
    """
    Extracts metadata from the image
    :param image_bytes: raw bytes making up the image
    :returns: named tuple with image width, height and format (jpg/gif/png/etc)
    :raises ValueError: if image bytes are unparseable
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        width = img.width
        height = img.height
        img_format = img.format
        return ImageMetadata(width, height, img_format)
    except OSError:
        raise ValueError("Cannot parse puzzle image")


if __name__ == "__main__":
    find()
