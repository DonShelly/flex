import unittest
from unittest.mock import patch
from main import fetch_all_outages, fetch_site_details, post_filtered_outages, main


class TestOutageProcessing(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_outages(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": "test"}]
        outages = fetch_all_outages()
        self.assertEqual(outages, [{"id": "test"}])

    @patch('main.requests.get')
    def test_get_site_info(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"devices": []}
        site_info = fetch_site_details("test-site")
        self.assertEqual(site_info, {"devices": []})

    @patch('main.requests.post')
    def test_post_site_outages(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}
        response = post_filtered_outages("test-site", [])
        self.assertEqual(response, None)

    @patch('main.fetch_all_outages')
    @patch('main.fetch_site_details')
    @patch('main.post_filtered_outages')
    def test_main(self, mock_post_site_outages, mock_get_site_info, mock_get_outages):
        mock_get_outages.return_value = [
            {"id": "test", "begin": "2022-05-23T12:21:27.377Z", "end": "2022-11-13T02:16:38.905Z"}]
        mock_get_site_info.return_value = {"devices": [{"id": "test", "name": "Test Device"}]}
        mock_post_site_outages.return_value = None
        main()
        mock_post_site_outages.assert_called_once()


if __name__ == '__main__':
    unittest.main()
