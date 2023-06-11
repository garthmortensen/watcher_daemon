import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from watcher import WebpageMonitorDaemon

class TestWebpageMonitorDaemon(unittest.TestCase):
    def setUp(self):
        self.daemon = WebpageMonitorDaemon('https://www.example.com', '/tmp/daemon-log.txt', 
                                           'smtp.example.com', 465, 'sender@example.com', 
                                           'password', 'receiver@example.com')
        self.daemon.send_email_notification = MagicMock()  # mock send_email_notification to avoid actual sending
        self.soup = BeautifulSoup('<html><head><title>Test Page</title></head><body></body></html>', 'html.parser')

    def test_get_page_title(self):
        title = self.daemon.get_page_title(self.soup)
        self.assertEqual(title, 'Test Page')

    def test_get_page_title_no_title(self):
        soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
        title = self.daemon.get_page_title(soup)
        self.assertEqual(title, 'No title')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_send_email_notification(self, mock_open):
        self.daemon.old_hash = 'old_hash'
        new_hash = hashlib.sha256(str(self.soup).encode('utf-8')).hexdigest()
        self.daemon.scrape_webpage = MagicMock(return_value=new_hash)  # mock scrape_webpage to return a new hash

        # Assume that the webpage content has changed (old_hash != new_hash)
        self.daemon.send_email_notification('Webpage has changed:\nTitle: Test Page\nContent:\n{str(self.soup)}\n\n')

        # Verify that the email was "sent" (i.e., send_email_notification was called)
        self.daemon.send_email_notification.assert_called_once()

        # Verify that the new content was written to the log file
        mock_open.assert_called_once_with('/tmp/daemon-log.txt', 'a')
        mock_open().write.assert_called_once()


#if __name__ == '__main__':
#    unittest.main()
