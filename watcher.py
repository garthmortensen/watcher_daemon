import daemon
import requests
from bs4 import BeautifulSoup
from time import sleep
import hashlib


class WebpageMonitorDaemon:
    """
    Class used to represent a webpage monitoring daemon.

    Attributes
    ----------
    url : str
        webpage URL
    log_path : str
        path to the log file to store updates
    old_hash : str
        SHA256 hash of webpage content from the last check
    """

    def __init__(self, url, log_path):
        """
        Constructs necessary attributes for the object.

        Parameters
        ----------
        url : str
            webpage URL
        log_path : str
            path to the log file to store updates
        """
        self.url = url
        self.log_path = log_path
        self.old_hash = ''

    def get_page_title(self, soup):
        """
        Returns webpage title.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            the parsed HTML

        Returns
        -------
        page_title : str
            webpage title or 'No title'
        """
        
        if soup.title:
            page_title = soup.title.string
        else:
            page_title = 'No title'
        
        return page_title


    def send_email_notification(self, content):
        """
        Sends an email notification with the updated content.

        Parameters
        ----------
        content : str
            the updated content

        Note
        ----
        The email sending logic should be implemented here.
        """
        msg = EmailMessage()
        msg['Subject'] = 'Webpage content changed'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg.set_content(content)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
        except Exception as e:
            print(f'Error occurred while sending email: {e}')

    def scrape_webpage(self):
        """
        Scrapes a webpage and checks for changes every n seconds.

        Note
        ----
        If change is detected, content is written to a file and email sends.
        """
        while True:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            current_hash = hashlib.sha256(str(soup).encode('utf-8')).hexdigest()

            if self.old_hash != current_hash:
                title = self.get_page_title(soup)
                content = f'Webpage has changed:\ntitle: {title}\ncontent:\n{str(soup)}\n\n'
                with open(self.log_path, "a") as f:
                    f.write(content)

                self.send_email_notification(content)
                self.old_hash = current_hash

            sleep(10)  # 10 sec

    def run(self):
        """
        Runs the daemon process.

        Note
        ----
        Method designed to be invoked as daemon's entry point.
        """
        with daemon.DaemonContext():
            self.scrape_webpage()

if __name__ == "__main__":
    daemon = WebpageMonitorDaemon('https://www.geartrade.com/hiking-and-camping/tents/four-season-tents', './log/daemon-log.txt')
    daemon.run()
