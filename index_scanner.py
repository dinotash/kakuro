#!/usr/local/bin/python3

"""
Script to identify new Kakuro puzzles published by the Guardian.
"""

import logging
import requests
import bs4
import logger
from datastore_client import DatastoreClient
from kakurizer_types import IndexPuzzle, Difficulty

INDEX_URL = "https://www.theguardian.com/lifeandstyle/series/kakuro?page="

def main():
    """
    Checks the Guardian's index page for new puzzles, extracts the metadata
    and saves the results to Google Cloud datastore.
    """
    logger.setup_logger()
    datastore = DatastoreClient()
    new_puzzles = get_new_puzzles(datastore)
    logging.getLogger().info("Found %s new puzzles", len(new_puzzles))
    datastore.put_index_puzzles(new_puzzles)

def get_new_puzzles(datastore):
    """
    Traverses the Guardian's index page from latest to oldest until it stops
    finding puzzles which are not already present in the database.

    :param datastore: datastore_client.DatastoreClient for accessing Google Cloud datastore.
    :returns: Tuple of kakurizer_types.IndexPuzzle, each representing one new puzzle
    """
    page_number = 1
    page_puzzles = []
    new_page_puzzles = []
    new_puzzles = []

    # Traverse the index until you stop finding new puzzles
    while (page_number == 1 or page_puzzles[-1] in new_page_puzzles):
        logging.getLogger().info("Loading puzzles from page %s", str(page_number))
        page_puzzles = parse_index(get_index(INDEX_URL, page_number))
        min_id = page_puzzles[-1].id
        max_id = page_puzzles[0].id
        existing_ids = datastore.get_ids(min_id, max_id)
        new_page_puzzles = [p for p in page_puzzles if p.id not in existing_ids and p not in new_puzzles]
        new_puzzles += new_page_puzzles
        page_number += 1

    return new_puzzles

def get_index(url, page):
    """
    Load content of specified URL with page number appended at end.

    :param url: String with base url to be loaded
    :param page: Number of page to be loaded
    :returns: HTML content of specified index page
    """
    response = requests.get(url + str(page))
    return response.text

def parse_index(html):
    """
    Extract tuple of puzzle metadata from index page.
    This includes each puzzle's ID, timestamp, difficulty and URL.

    :param html: String containing HTML content of index page
    :returns: Tuple of kakurizer_types.IndexPuzzle, each representing one puzzle from the page
    """
    page = bs4.BeautifulSoup(html, "html.parser")
    all_sections = page.find_all("section")
    puzzle_sections = (section for section in all_sections if is_puzzle(section))
    return tuple(parse_section(section) for section in puzzle_sections)

def is_puzzle(section):
    """
    Determine whether a <section> tag from the index page represents a puzzle or not.

    :param section: bs4.element.Tag representing a <section> element
    :returns: True if and only if this section tag relates to a puzzle
    """
    return (isinstance(section, bs4.element.Tag)
            and section.name == "section"
            and 'id' in section.attrs)

def parse_section(section):
    """
    Parse metadata from a <section> tag that describes a puzzle.

    :param section: bs4.element.Tag representing a <section> element
    :returns: Metadata for this puzzle as a kakurizer_types.IndexPuzzle
    """
    puzzle_id = get_id(section)
    timestamp_millis = get_timestamp(section)
    page_url = get_pageurl(section)
    difficulty = get_difficulty(section)
    return IndexPuzzle(puzzle_id, timestamp_millis, page_url, difficulty)

def get_id(section):
    """
    Extracts the ID number for the puzzle

    :param section: bs4.element.Tag representing a <section> element
    :returns: ID number for the puzzle
    :raises ValueError: if no ID can be parsed from the section
    """
    try:
        header = next(section.find(class_="fc-item__title").stripped_strings)
        header_words = header.split(" ")
        return int(header_words[1].replace(",", ""))
    except AttributeError:
        raise ValueError("Could not find header tag")
    except StopIteration:
        raise ValueError("Could not parse puzzle id from section title")

def get_timestamp(section):
    """
    Extracts the timestamp at which the puzzle was published.

    :param section: bs4.element.Tag representing a <section> element
    :returns: Number of milliseconds since the epoch when puzzle was published
    :raises ValueError: if timestamp cannot be extracted
    """
    try:
        return int(section.find("time", class_="fc-item__timestamp").attrs["data-timestamp"])
    except AttributeError:
        raise ValueError("Could not find timestamp in section")
    except KeyError:
        raise ValueError("Could not find data-timestamp attribute for timestamp")

def get_pageurl(section):
    """
    Extracts the URL for this puzzle's page. Later stages of the pipeline will follow
    this path to load and parse the puzzle itself.

    :param section: bs4.element.Tag representing a <section> element
    :returns: string containing URL to the page with the puzzle's image.
    :raises ValueError: if unable to find link to puzzle
    """
    try:
        return section.find("a", class_="fc-item__link").attrs['href']
    except AttributeError:
        raise ValueError("Cannot find link to puzzle")
    except KeyError:
        raise ValueError("Cannot find href attribute on link to puzzle")

def get_difficulty(section):
    """
    Extracts and validates the difficulty level of the puzzle. If not present
    or not a valid difficulty level, it will throw an error.

    :param section: bs4.element.Tag representing a <section> element
    :returns: Difficulty level of the puzzle (as kakurizer_types.Difficulty)
    :raises ValueError: on unrecognized difficulty levels
    """
    try:
        header = next(section.find(class_="fc-item__title").stripped_strings)
        header_words = header.split(" ")
        difficulty = header_words[2].lower()
        if difficulty == "easy":
            return Difficulty.EASY.name
        elif difficulty == "medium":
            return Difficulty.MEDIUM.name
        elif difficulty == "hard":
            return Difficulty.HARD.name
        else:
            raise ValueError("Unrecognized difficulty level: " + difficulty)
    except:
        raise ValueError("Unable to find difficulty in title text")

if __name__ == "__main__":
    main()
