"""
Provides client wrapping access to Google Cloud Datastore for use with kakuro puzzles.
"""

import logging
from google.cloud import datastore

class DatastoreClient:
    """
    DAO for access to Google Cloud Datastore for use with kakuro puzzles.
    """

    CLOUD_PROJECT = "kakurizer"
    CLOUDSTORE_TYPE = "kakuro"
    MAX_PUT_SIZE = 500 # Maximum supported mutations in same transaction (Google-imposed limit)
    DATASTORE_MAX_INT = 9223372036854775807

    def __init__(self):
        self.client = datastore.Client(project=self.CLOUD_PROJECT)

    def get_ids(self, min_id=-DATASTORE_MAX_INT, max_id=DATASTORE_MAX_INT):
        """
        Return a tuple of puzzle IDs which have been saved (in any state) to the database.
        Used to check if a puzzle already exists or not.

        :param min_id: If set, only look for IDs greater than or equal to this
        :param max_id: If set, only look for IDs less than or equal to this
        :returns: tuple of IDs of puzzles which exist in the database
        """
        query = self.client.query(kind=self.CLOUDSTORE_TYPE, projection=("id",))
        query.add_filter('id', '>=', min_id)
        query.add_filter('id', '<=', max_id)
        return (puzzle['id'] for puzzle in query.fetch())

    def put_index_puzzles(self, index_puzzles):
        """
        Saves a set of puzzles to Google Cloud Datastore. This is used with puzzle
        metadata extracted from index pages, so only a limited number of fields are
        set.

        :param index_puzzles: List or tuple of kakurizer_types.IndexPuzzle
        """
        partial_key = self.client.key(self.CLOUDSTORE_TYPE)
        for chunk_start in range(0, len(index_puzzles), self.MAX_PUT_SIZE):
            puzzles = index_puzzles[chunk_start: chunk_start + self.MAX_PUT_SIZE]
            size = len(puzzles)
            keys = self.client.allocate_ids(partial_key, size)
            entities = tuple(make_index_puzzle(puzzles[p], keys[p]) for p in range(size))
            self.client.put_multi(entities)
            logging.getLogger().info("Saved %s puzzles from index", size)

def make_index_puzzle(index_puzzle, final_key):
    """
    Converts puzzle representation output from index_scanner script to Entity format
    used by Google Cloud Datastore.

    :param index_puzzle: kakurizer_types.IndexPuzzle of a single puzzle's metadata from index page
    :param final_key: google.cloud.datastore.key.Key to uniquely identify this puzzle
    :returns: Puzzle represented as google.cloud.datastore.entity.Entity for saving into database.
    """
    entity = datastore.entity.Entity(key=final_key)
    entity['id'] = index_puzzle.id
    entity['timestamp_millis'] = index_puzzle.timestamp_millis
    entity['difficulty'] = index_puzzle.difficulty
    entity['page_url'] = index_puzzle.page_url
    return entity
