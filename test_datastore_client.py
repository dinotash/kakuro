#!/usr/local/bin/python3

"""
Tests for DatastoreClient() which wraps access to the Google Cloud
Datastore for Kakuro puzzles. These tests use the Cloud Datastore
Emulator which must be installed locally.
"""

import unittest
import os
import pexpect
from datastore_client import DatastoreClient
from kakurizer_types import IndexPuzzle

class IndexScannerTest(unittest.TestCase):
    """
    Unit tests for the datastore_client module.
    """

    def setUp(self):
        """
        Start a local emulated cloud datastore for each test. This is slower (around
        five seconds per test) but should guarantee that each test is hermetic and
        there doesn't seem to be an easy way to reset the database each time (unlike
        with java).
        """
        self.emulator = pexpect.spawn("gcloud beta emulators datastore start --no-store-on-disk")
        self.emulator.expect(".*Dev App Server is now running.*")
        os.environ['DATASTORE_EMULATOR_HOST'] = "localhost:8081"
        os.environ['DATASTORE_PROJECT_ID'] = "kakurizer"

    def tearDown(self):
        """
        Stop the local cloud datastore emulator after each test.
        """
        self.emulator.kill(0)
        del os.environ['DATASTORE_EMULATOR_HOST']
        del os.environ['DATASTORE_PROJECT_ID']

    def test_empty_db(self):
        """
        Check new database is empty.
        """
        db_client = DatastoreClient()
        self.assertEqual(tuple(db_client.get_ids()), tuple())

    def test_put_indexpuzzles(self):
        """
        Check we can get back what we put into the database and that multiple writes are additive.
        """
        db_client = DatastoreClient()

        puzzle_one = IndexPuzzle(id=1, timestamp_millis=123, page_url="link", difficulty="HARD")
        db_client.put_index_puzzles([puzzle_one])
        self.assertEqual(tuple(db_client.get_ids()), (1,))

        puzzle_two = IndexPuzzle(id=2, timestamp_millis=456, page_url="other", difficulty="MEDIUM")
        db_client.put_index_puzzles([puzzle_two])
        self.assertEqual(tuple(db_client.get_ids()), (1, 2))

    def test_get_puzzles(self):
        """
        Check we can get back what we put into the database
        """
        db_client = DatastoreClient()

        puzzle = IndexPuzzle(id=1, timestamp_millis=123, page_url="link", difficulty="HARD")
        db_client.put_index_puzzles([puzzle])

        results = db_client.get_index_puzzles()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], puzzle.id)
        self.assertEqual(results[0]['timestamp_millis'], puzzle.timestamp_millis)
        self.assertEqual(results[0]['page_url'], puzzle.page_url)
        self.assertEqual(results[0]['difficulty'], puzzle.difficulty)

    def test_update(self):
        """
        Check we can get back the updated version after changing an entry in the database.
        """
        db_client = DatastoreClient()

        puzzle = IndexPuzzle(id=1, timestamp_millis=123, page_url="link", difficulty="HARD")
        db_client.put_index_puzzles([puzzle])
        entity = db_client.get_index_puzzles()[0]

        new_id = 678
        new_timestamp = 10000
        img_url = "wheel.jpg"

        entity['id'] = new_id
        entity['timestamp_millis'] = new_timestamp
        entity['img_url'] = img_url
        db_client.update(entity)

        results = db_client.get_index_puzzles()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], new_id)
        self.assertEqual(results[0]['timestamp_millis'], new_timestamp)
        self.assertEqual(results[0]['img_url'], img_url)
        self.assertEqual(results[0]['page_url'], puzzle.page_url)
        self.assertEqual(results[0]['difficulty'], puzzle.difficulty)


if __name__ == '__main__':
    unittest.main()
