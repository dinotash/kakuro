"""
Tests the index_scanner script.
"""

import unittest
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

    def test_is_puzzle_section_with_id(self):
        section = bs4.BeautifulSoup("", "html.parser").new_tag("section", id="123")
        self.assertTrue(index_scanner.is_puzzle(section))

    def test_is_puzzle_section_no_id(self):
        section = bs4.BeautifulSoup("", "html.parser").new_tag("section")
        self.assertFalse(index_scanner.is_puzzle(section))

    def test_is_puzzle_othertag_with_id(self):
        section = bs4.BeautifulSoup("", "html.parser").new_tag("div", id="123")
        self.assertFalse(index_scanner.is_puzzle(section))

    def test_parse_section_all_fields(self):
        expected = IndexPuzzle(self.puzzle_id, self.timestamp, self.page_url, self.difficulty)
        section = self.make_test_section_tag()
        result = index_scanner.parse_section(section)
        self.assertEqual(result, expected)

    def test_parse_section_no_titletag(self):
        section = self.make_test_section_tag()
        section.find("h1").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_no_titletext(self):
        section = self.make_test_section_tag()
        section.find("h1").string = ""
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_without_id(self):
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.difficulty.lower()}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nonnumericid(self):
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro abc {self.difficulty.lower()}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_notimetag(self):
        section = self.make_test_section_tag()
        section.find("time").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_notimeattr(self):
        section = self.make_test_section_tag()
        del section.find("time").attrs['data-timestamp']
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nonumerictimestamp(self):
        section = self.make_test_section_tag()
        section.find("time").attrs['data-timestamp'] = "abc"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nopagelink(self):
        section = self.make_test_section_tag()
        section.find("a").extract()
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_nohref(self):
        section = self.make_test_section_tag()
        del section.find("a").attrs['href']
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_without_difficulty(self):
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.puzzle_id}"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_section_invalid_difficulty(self):
        section = self.make_test_section_tag()
        section.find("h1").string = f"Kakuro {self.puzzle_id} okayish"
        with self.assertRaises(ValueError):
            index_scanner.parse_section(section)

    def test_parse_real_index_page(self):
        real_index_file = open("test_index_page.html")
        content = real_index_file.read()
        real_index_file.close()
        expected = (
            IndexPuzzle(id=1583, timestamp_millis=1513900898000, page_url='https://www.theguardian.com/lifeandstyle/2017/dec/22/kakuro-1583-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1582, timestamp_millis=1513296062000, page_url='https://www.theguardian.com/lifeandstyle/2017/dec/15/kakuro-1582-hard', difficulty='HARD'),
            IndexPuzzle(id=1581, timestamp_millis=1512691287000, page_url='https://www.theguardian.com/lifeandstyle/2017/dec/08/kakuro-1581-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1580, timestamp_millis=1512086487000, page_url='https://www.theguardian.com/lifeandstyle/2017/dec/01/kakuro-1580-hard', difficulty='HARD'),
            IndexPuzzle(id=1579, timestamp_millis=1511481675000, page_url='https://www.theguardian.com/lifeandstyle/2017/nov/24/kakuro-1579-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1578, timestamp_millis=1510876869000, page_url='https://www.theguardian.com/lifeandstyle/2017/nov/17/kakuro-1578-hard', difficulty='HARD'),
            IndexPuzzle(id=1577, timestamp_millis=1510272063000, page_url='https://www.theguardian.com/lifeandstyle/2017/nov/10/kakuro-1577-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1576, timestamp_millis=1509667269000, page_url='https://www.theguardian.com/lifeandstyle/2017/nov/03/kakuro-1576-hard', difficulty='HARD'),
            IndexPuzzle(id=1575, timestamp_millis=1509058873000, page_url='https://www.theguardian.com/lifeandstyle/2017/oct/27/kakuro-1575-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1574, timestamp_millis=1508454098000, page_url='https://www.theguardian.com/lifeandstyle/2017/oct/20/kakuro-1574-hard', difficulty='HARD'),
            IndexPuzzle(id=1573, timestamp_millis=1507849276000, page_url='https://www.theguardian.com/lifeandstyle/2017/oct/13/kakuro-1573-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1572, timestamp_millis=1507281989000, page_url='https://www.theguardian.com/lifeandstyle/2017/oct/06/kakuro-1572-hard', difficulty='HARD'),
            IndexPuzzle(id=1571, timestamp_millis=1506639669000, page_url='https://www.theguardian.com/lifeandstyle/2017/sep/29/kakuro-1571-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1570, timestamp_millis=1506034891000, page_url='https://www.theguardian.com/lifeandstyle/2017/sep/22/kakuro-1569-medium', difficulty='HARD'), 
            IndexPuzzle(id=1569, timestamp_millis=1505430077000, page_url='https://www.theguardian.com/lifeandstyle/2017/sep/15/kakuro-1569-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1568, timestamp_millis=1504825282000, page_url='https://www.theguardian.com/lifeandstyle/2017/sep/08/kakuro-1568-hard', difficulty='HARD'),
            IndexPuzzle(id=1567, timestamp_millis=1504220487000, page_url='https://www.theguardian.com/lifeandstyle/2017/sep/01/kakuro-1567-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1566, timestamp_millis=1503615692000, page_url='https://www.theguardian.com/lifeandstyle/2017/aug/25/kakuro-1566-hard', difficulty='HARD'),
            IndexPuzzle(id=1565, timestamp_millis=1503073147000, page_url='https://www.theguardian.com/lifeandstyle/2017/aug/18/kakuro-1565-medium', difficulty='MEDIUM'),
            IndexPuzzle(id=1564, timestamp_millis=1502406102000, page_url='https://www.theguardian.com/lifeandstyle/2017/aug/11/kakuro-1564-hard', difficulty='HARD'))
        self.assertEqual(index_scanner.parse_index(content), expected)

    def make_test_section_tag(self):
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
