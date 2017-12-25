#!/usr/local/bin/python3

"""
Tests for img_finder module which updates a database entity with details of the relevant
puzzle image.
"""

import unittest
from unittest import mock
import requests_mock
from google.cloud.datastore.entity import Entity
import img_finder

class ImageFinderTest(unittest.TestCase):
    """
    Unit tests for the img_finder script.
    """

    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_simple_case(self, request_mock, datastore_mock):
        """
        Expect it to update the database with image bytes and metadata
        """
        puzzle_id = 1245
        page_url = "http://page.html"
        img_url = "http://image.jpg&w=100" # Should infer from bytes, not filename
        page_content = "<html><source sizes='400px' srcset='http://image.jpg&amp;w=100 54'/></html>"

        # random small image file, found online (http://png-pixel.com/1x1-png-pixel.png)
        img_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00$\x00\x00\x00$\x08\x06\x00\x00\x00\xe1\x00\x98\x98\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x12$\x00\x00\x12$\x01hSJ\xdb\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00\x7fIDATX\x85\xed\xd81\n\xc0 \x10D\xd1Q\xac\xd6\xde+\xe5\xcc\xb9\x92\x07X\x92\xc6\xa4\r\x01\x1dRH,\xe6\xb7\x82>\xd8j\r\x00.\xac\xd3\x19\xff\x16\xbc\x13\x88%\x10+\xf5\x0ej\xad\xbb\x99\xb5\x19\x8f\xba{,\xa5l\x9f@f\xd6r\xceS@\xa3\x96\x1b\x99@,\x81X\x02\xb1\x04b\t\xc4\x12\x88%\x10K \x96@,\x81X\xdd\xad\xc3\xdd\xa7aGw\x07\xe8\xf7c\x9c@\xac\xe5@\t\xc0\xf97\xe2\xd1q\x03\x0fe\x163\xa1a.O\x00\x00\x00\x00IEND\xaeB`\x82'

        original_entity = Entity()
        original_entity['id'] = puzzle_id
        original_entity['page_url'] = page_url

        datastore_mock.get_index_puzzles.return_value = [original_entity]
        request_mock.get(page_url, text=page_content)
        request_mock.get(img_url, content=img_bytes)

        img_finder.update_puzzle_with_image(datastore_mock, original_entity)

        # Unpack from tuple, see: https://docs.python.org/3/library/unittest.mock.html#call
        result = datastore_mock.update.call_args_list[0][0][0]

        # Compare each field rather than whole object because don't care about order
        self.assertEqual(result['id'], puzzle_id)
        self.assertTrue(result['has_img'])
        self.assertEqual(result['page_url'], page_url)
        self.assertEqual(result['img_url'], img_url)
        self.assertEqual(result['img_width'], 36)
        self.assertEqual(result['img_height'], 36)
        self.assertEqual(result['img_format'], 'PNG')
        self.assertEqual(result['img_blob'], img_bytes)
        self.assertEqual(result.exclude_from_indexes, ('img_blob',))


    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_no_source(self, request_mock, datastore_mock):
        """
        Expect an error if there is no image URL on the page
        """
        puzzle_id = 1245
        page_url = "http://page.html"
        page_content = "<html></html>"

        original_entity = Entity()
        original_entity['id'] = puzzle_id
        original_entity['page_url'] = page_url

        datastore_mock.get_index_puzzles.return_value = [original_entity]
        request_mock.get(page_url, text=page_content)

        with self.assertRaises(ValueError):
            img_finder.update_puzzle_with_image(datastore_mock, original_entity)


    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_multiple_sources(self, request_mock, datastore_mock):
        """
        Expect it to pick the largest version of the image, given the choice
        """
        puzzle_id = 1245
        page_url = "http://page.html"
        img_url = "http://image.jpg&w=600" # Should infer from bytes, not filename
        page_content = """
        <html>
        <source sizes='300px' srcset='http://image.jpg&amp;w=300 77'/>
        <source sizes='400px' srcset='http://image.jpg&amp;w=400 86'/>
        <source sizes='600px' srcset='http://image.jpg&amp;w=600 aa'/>
        </html>"""

        # random small image file, found online (http://png-pixel.com/1x1-png-pixel.png)
        img_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00$\x00\x00\x00$\x08\x06\x00\x00\x00\xe1\x00\x98\x98\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x12$\x00\x00\x12$\x01hSJ\xdb\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00\x7fIDATX\x85\xed\xd81\n\xc0 \x10D\xd1Q\xac\xd6\xde+\xe5\xcc\xb9\x92\x07X\x92\xc6\xa4\r\x01\x1dRH,\xe6\xb7\x82>\xd8j\r\x00.\xac\xd3\x19\xff\x16\xbc\x13\x88%\x10+\xf5\x0ej\xad\xbb\x99\xb5\x19\x8f\xba{,\xa5l\x9f@f\xd6r\xceS@\xa3\x96\x1b\x99@,\x81X\x02\xb1\x04b\t\xc4\x12\x88%\x10K \x96@,\x81X\xdd\xad\xc3\xdd\xa7aGw\x07\xe8\xf7c\x9c@\xac\xe5@\t\xc0\xf97\xe2\xd1q\x03\x0fe\x163\xa1a.O\x00\x00\x00\x00IEND\xaeB`\x82'

        original_entity = Entity()
        original_entity['id'] = puzzle_id
        original_entity['page_url'] = page_url

        datastore_mock.get_index_puzzles.return_value = [original_entity]
        request_mock.get(page_url, text=page_content)
        request_mock.get(img_url, content=img_bytes)

        img_finder.update_puzzle_with_image(datastore_mock, original_entity)

        # Unpack from tuple, see: https://docs.python.org/3/library/unittest.mock.html#call
        result = datastore_mock.update.call_args_list[0][0][0]

        # Compare each field rather than whole object because don't care about order
        self.assertEqual(result['id'], puzzle_id)
        self.assertTrue(result['has_img'])
        self.assertEqual(result['page_url'], page_url)
        self.assertEqual(result['img_url'], img_url)
        self.assertEqual(result['img_width'], 36)
        self.assertEqual(result['img_height'], 36)
        self.assertEqual(result['img_format'], 'PNG')
        self.assertEqual(result['img_blob'], img_bytes)
        self.assertEqual(result.exclude_from_indexes, ('img_blob',))


    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_cannot_parse_image(self, request_mock, datastore_mock):
        """
        Expect it to throw ValueError if image bytes not parseable
        """
        puzzle_id = 1245
        page_url = "http://page.html"
        img_url = "http://image.jpg&w=100" # Should infer from bytes, not filename
        page_content = "<html><source sizes='400px' srcset='http://image.jpg&amp;w=100 54'/></html>"

        img_bytes = b'\x89' # Made up and very small byte string

        original_entity = Entity()
        original_entity['id'] = puzzle_id
        original_entity['page_url'] = page_url

        datastore_mock.get_index_puzzles.return_value = [original_entity]
        request_mock.get(page_url, text=page_content)
        request_mock.get(img_url, content=img_bytes)

        with self.assertRaises(ValueError):
            img_finder.update_puzzle_with_image(datastore_mock, original_entity)


    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_cannot_parse_html(self, request_mock, datastore_mock):
        """
        Expect it to throw ValueError if content of page_url is nonsense
        """
        puzzle_id = 1245
        page_url = "http://page.html"

        original_entity = Entity()
        original_entity['id'] = puzzle_id
        original_entity['page_url'] = page_url

        datastore_mock.get_index_puzzles.return_value = [original_entity]
        request_mock.get(page_url, text="34890u230")

        with self.assertRaises(ValueError):
            img_finder.update_puzzle_with_image(datastore_mock, original_entity)


if __name__ == '__main__':
    unittest.main()
