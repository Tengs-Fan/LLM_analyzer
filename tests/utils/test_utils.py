import unittest
from MediaMined.utils.utils import extract_id_from_url

class TestUrlExtractor(unittest.TestCase):

    def test_extract_reddit_id(self):
        reddit_url = 'https://www.reddit.com/r/fpgagaming/comments/17a1ph8/any_interest_in_a_lowcost_open_source_fpga/'
        self.assertEqual(extract_id_from_url(reddit_url), '17a1ph8')

    def test_extract_youtube_id(self):
        youtube_url = 'https://www.youtube.com/watch?v=B2NkjV-hSwk'
        self.assertEqual(extract_id_from_url(youtube_url), 'B2NkjV-hSwk')

    # def test_extract_short_youtube_id(self):
    #     short_youtube_url = 'https://youtu.be/B2NkjV-hSwk'
    #     self.assertEqual(extract_id_from_url(short_youtube_url), 'B2NkjV-hSwk')
    # # Test
    # url = 'https://www.reddit.com/r/fpgagaming/comments/17a1ph8/any_interest_in_a_lowcost_open_source_fpga/'
    # print(extract_reddit_post_id(url))  # Expected: 17a1ph8

    # def test_invalid_url(self):
    #     invalid_url = 'https://www.someotherwebsite.com/watch?v=someId'
    #     self.assertIsNone(extract_id_from_url(invalid_url))

if __name__ == '__main__':
    unittest.main()
