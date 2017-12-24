#!/usr/local/bin/python3

"""
Tests the index_scanner script.
"""

import unittest
from unittest import mock
import requests_mock
import bs4
import index_scanner
from kakurizer_types import IndexPuzzle

class IndexScannerTest(unittest.TestCase):
    """
    Unit tests for the index_scanner script.
    """

    puzzle_id = 123
    timestamp = 98765
    page_url = "puzzle.html"
    difficulty = "HARD"

    real_puzzles = {
        1583: IndexPuzzle(
            id=1583,
            timestamp_millis=1513900898000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/dec/22/kakuro-1583-medium',
            difficulty='MEDIUM'),
        1582: IndexPuzzle(
            id=1582,
            timestamp_millis=1513296062000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/dec/15/kakuro-1582-hard',
            difficulty='HARD'),
        1581: IndexPuzzle(
            id=1581,
            timestamp_millis=1512691287000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/dec/08/kakuro-1581-medium',
            difficulty='MEDIUM'),
        1580: IndexPuzzle(
            id=1580,
            timestamp_millis=1512086487000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/dec/01/kakuro-1580-hard',
            difficulty='HARD'),
        1579: IndexPuzzle(
            id=1579,
            timestamp_millis=1511481675000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/nov/24/kakuro-1579-medium',
            difficulty='MEDIUM'),
        1578: IndexPuzzle(
            id=1578,
            timestamp_millis=1510876869000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/nov/17/kakuro-1578-hard',
            difficulty='HARD'),
        1577: IndexPuzzle(
            id=1577,
            timestamp_millis=1510272063000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/nov/10/kakuro-1577-medium',
            difficulty='MEDIUM'),
        1576: IndexPuzzle(
            id=1576,
            timestamp_millis=1509667269000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/nov/03/kakuro-1576-hard',
            difficulty='HARD'),
        1575: IndexPuzzle(
            id=1575,
            timestamp_millis=1509058873000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/oct/27/kakuro-1575-medium',
            difficulty='MEDIUM'),
        1574: IndexPuzzle(
            id=1574,
            timestamp_millis=1508454098000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/oct/20/kakuro-1574-hard',
            difficulty='HARD'),
        1573: IndexPuzzle(
            id=1573,
            timestamp_millis=1507849276000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/oct/13/kakuro-1573-medium',
            difficulty='MEDIUM'),
        1572: IndexPuzzle(
            id=1572,
            timestamp_millis=1507281989000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/oct/06/kakuro-1572-hard',
            difficulty='HARD'),
        1571: IndexPuzzle(
            id=1571,
            timestamp_millis=1506639669000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/sep/29/kakuro-1571-medium',
            difficulty='MEDIUM'),
        1570: IndexPuzzle(
            id=1570,
            timestamp_millis=1506034891000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/sep/22/kakuro-1569-medium',
            difficulty='HARD'),
        1569: IndexPuzzle(
            id=1569,
            timestamp_millis=1505430077000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/sep/15/kakuro-1569-medium',
            difficulty='MEDIUM'),
        1568: IndexPuzzle(
            id=1568,
            timestamp_millis=1504825282000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/sep/08/kakuro-1568-hard',
            difficulty='HARD'),
        1567: IndexPuzzle(
            id=1567,
            timestamp_millis=1504220487000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/sep/01/kakuro-1567-medium',
            difficulty='MEDIUM'),
        1566: IndexPuzzle(
            id=1566,
            timestamp_millis=1503615692000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/aug/25/kakuro-1566-hard',
            difficulty='HARD'),
        1565: IndexPuzzle(
            id=1565,
            timestamp_millis=1503073147000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/aug/18/kakuro-1565-medium',
            difficulty='MEDIUM'),
        1564: IndexPuzzle(
            id=1564,
            timestamp_millis=1502406102000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/aug/11/kakuro-1564-hard',
            difficulty='HARD'),
        1563: IndexPuzzle(
            id=1563,
            timestamp_millis=1501801287000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/aug/04/kakuro-1563-medium',
            difficulty='MEDIUM'),
        1562: IndexPuzzle(
            id=1562,
            timestamp_millis=1501196470000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jul/28/kakuro-1562-hard',
            difficulty='HARD'),
        1561: IndexPuzzle(
            id=1561,
            timestamp_millis=1500591662000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jul/21/kakuro-1561-medium',
            difficulty='MEDIUM'),
        1560: IndexPuzzle(
            id=1560,
            timestamp_millis=1499986867000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jul/14/kakuro-1560-hard',
            difficulty='HARD'),
        1559: IndexPuzzle(
            id=1559,
            timestamp_millis=1499382070000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jul/07/kakuro-1559-medium',
            difficulty='MEDIUM'),
        3006: IndexPuzzle(
            id=3006,
            timestamp_millis=1498777263000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jun/30/kakuro-3006-hard',
            difficulty='HARD'),
        1557: IndexPuzzle(
            id=1557,
            timestamp_millis=1498172468000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jun/23/kakuro-1557-medium',
            difficulty='MEDIUM'),
        1556: IndexPuzzle(
            id=1556,
            timestamp_millis=1497567712000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jun/16/kakuro-1556-hard',
            difficulty='HARD'),
        1555: IndexPuzzle(
            id=1555,
            timestamp_millis=1496962900000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jun/09/kakuro-1555-medium',
            difficulty='MEDIUM'),
        1554: IndexPuzzle(
            id=1554,
            timestamp_millis=1496358068000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/jun/02/kakuro-1554-hard',
            difficulty='HARD'),
        1553: IndexPuzzle(
            id=1553,
            timestamp_millis=1495753302000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/may/26/kakuro-1553-medium',
            difficulty='MEDIUM'),
        1552: IndexPuzzle(
            id=1552,
            timestamp_millis=1495148499000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/may/19/kakuro-1552-hard',
            difficulty='HARD'),
        1551: IndexPuzzle(
            id=1551,
            timestamp_millis=1494923034000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/may/16/kakuro-1551-medium',
            difficulty='MEDIUM'),
        1550: IndexPuzzle(
            id=1550,
            timestamp_millis=1493938882000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/may/05/kakuro-1550-hard',
            difficulty='HARD'),
        1549: IndexPuzzle(
            id=1549,
            timestamp_millis=1493334091000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/apr/28/kakuro-1549-medium',
            difficulty='MEDIUM'),
        1548: IndexPuzzle(
            id=1548,
            timestamp_millis=1492729262000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/apr/21/kakuro-1548-hard',
            difficulty='HARD'),
        1547: IndexPuzzle(
            id=1547,
            timestamp_millis=1492124417000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/apr/13/kakuro-1547-medium',
            difficulty='MEDIUM'),
        1546: IndexPuzzle(
            id=1546,
            timestamp_millis=1491519676000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/apr/07/kakuro-1546-hard',
            difficulty='HARD'),
        1545: IndexPuzzle(
            id=1545,
            timestamp_millis=1490914899000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/mar/31/kakuro-1545-medium',
            difficulty='MEDIUM'),
        1544: IndexPuzzle(
            id=1544,
            timestamp_millis=1490313677000,
            page_url='https://www.theguardian.com/lifeandstyle/2017/mar/24/kakuro-1544-hard',
            difficulty='HARD'),
    }

    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_filter_datastore_results(self, request_mock, datastore_mock):
        """
        Check that we don't return puzzles as new if already in the database.
        """
        url = "https://www.theguardian.com/lifeandstyle/series/kakuro?page=1"
        real_index_file = open("test_index_page.html")
        content = real_index_file.read()
        real_index_file.close()
        request_mock.get(url, text=content)

        datastore_ids = tuple([1564, 1565, 1579]) # Includes last ID so won't load next page
        datastore_mock.get_ids.return_value = datastore_ids
        expected = tuple([p for p in self.real_puzzles.values()
                          if p.id >= 1564 and p.id != 3006 and p.id not in datastore_ids])
        self.assertEqual(index_scanner.get_new_puzzles(datastore_mock), expected)

    @requests_mock.mock()
    @mock.patch("datastore_client.DatastoreClient")
    def test_search_next_page_if_needed(self, request_mock, datastore_mock):
        """
        Check that we load the next page of results if the last entry was a new puzzle.
        """
        url = "https://www.theguardian.com/lifeandstyle/series/kakuro?page="

        real_index_file_1 = open("test_index_page.html")
        content_1 = real_index_file_1.read()
        real_index_file_1.close()
        request_mock.get(url + "1", text=content_1)

        real_index_file_2 = open("test_index_page_2.html")
        content_2 = real_index_file_2.read()
        real_index_file_2.close()
        request_mock.get(url + "2", text=content_2)

        datastore_ids = tuple([1565, 1557, 1544]) # Won't load third page
        datastore_mock.get_ids.return_value = datastore_ids
        expected = tuple([p for p in self.real_puzzles.values() if p.id not in datastore_ids])
        self.assertEqual(index_scanner.get_new_puzzles(datastore_mock), expected)

    def test_parse_real_index_page(self):
        """
        Check we get expected results from a saved real page.
        """
        real_index_file = open("test_index_page.html")
        content = real_index_file.read()
        real_index_file.close()
        expected = tuple([p for p in self.real_puzzles.values()
                          if p.id >= 1564 and p.id != 3006])
        self.assertEqual(index_scanner.parse_index(content), expected)

    def test_is_puzzle_section_with_id(self):
        """
        Identify puzzles on index page as <section> with ID
        """
        section = bs4.BeautifulSoup("", "html.parser").new_tag("section", id="123")
        self.assertTrue(index_scanner.is_puzzle(section))

    def test_is_puzzle_section_no_id(self):
        """
        Not a puzzle if it doesn't have an ID
        """
        section = bs4.BeautifulSoup("", "html.parser").new_tag("section")
        self.assertFalse(index_scanner.is_puzzle(section))

    def test_is_puzzle_othertag_with_id(self):
        """
        Not a puzzle if it isn't a section element
        """
        section = bs4.BeautifulSoup("", "html.parser").new_tag("div", id="123")
        self.assertFalse(index_scanner.is_puzzle(section))

    def test_parse_section_all_fields(self):
        """
        Successfully parse a puzzle where all metadata populated
        """
        expected = IndexPuzzle(self.puzzle_id, self.timestamp, self.page_url, self.difficulty)
        section = self.make_test_section_tag()
        result = index_scanner.parse_section(section)
        self.assertEqual(result, expected)

    def test_parse_section_no_titletag(self):
        """
        Throw error on parsing puzzle with no title text.
        """
        section = self.make_test_section_tag()
        section.find("h1").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_no_titletext(self):
        """
        Throw error on parsing puzzle with blank title text.
        """
        section = self.make_test_section_tag()
        section.find("h1").string = ""
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_without_id(self):
        """
        Throw error on parsing puzzle with title text lacking ID.
        """
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.difficulty.lower()}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nonnumericid(self):
        """
        Throw error on parsing puzzle where ID in title text isn't a number.
        """
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro abc {self.difficulty.lower()}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_notimetag(self):
        """
        Throw error on parsing puzzle with no time tag.
        """
        section = self.make_test_section_tag()
        section.find("time").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_notimeattr(self):
        """
        Throw error on parsing puzzle with no timestamp in time tag.
        """
        section = self.make_test_section_tag()
        del section.find("time").attrs['data-timestamp']
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_nonumeric_timestamp(self):
        """
        Throw error on parsing puzzle where timestamp is not a number.
        """
        section = self.make_test_section_tag()
        section.find("time").attrs['data-timestamp'] = "abc"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nopagelink(self):
        """
        Throw error on parsing puzzle with no link to puzzle page.
        """
        section = self.make_test_section_tag()
        section.find("a").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nohref(self):
        """
        Throw error on parsing puzzle with missing link to puzzle page.
        """
        section = self.make_test_section_tag()
        del section.find("a").attrs['href']
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_without_difficulty(self):
        """
        Throw error on parsing puzzle where title text is missing difficulty.
        """
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.puzzle_id}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_invalid_difficulty(self):
        """
        Throw error on parsing puzzle with unknown difficulty.
        """
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.puzzle_id} okayish"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def make_test_section_tag(self):
        """
        Make a standard <section> element with all attributes populated to be used in tests.
        """
        section = bs4.BeautifulSoup("", "html.parser").new_tag("section", id=self.puzzle_id)

        time_tag = bs4.BeautifulSoup("", "html.parser").new_tag("time")
        time_tag["class"] = "fc-item__timestamp"
        time_tag["data-timestamp"] = self.timestamp
        section.append(time_tag)

        a_tag = bs4.BeautifulSoup("", "html.parser").new_tag("a", href=self.page_url)
        a_tag["class"] = "fc-item__link"
        section.append(a_tag)

        h1_tag = bs4.BeautifulSoup("", "html.parser").new_tag("h1")
        h1_tag["class"] = "fc-item__title"
        h1_tag.string = f"Kakuro {self.puzzle_id} {self.difficulty.lower()}"
        section.append(h1_tag)

        return section

if __name__ == '__main__':
    unittest.main()
