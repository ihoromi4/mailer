import sys
import time
import random
import json
import logging
import traceback
import smtplib
from numbers import Number
from email.mime.text import MIMEText


def _init_logging():
    """Initialize logging"""

    logging.basicConfig(
        filename='mail.log',
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # add logs to sys.stdout
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    root.addHandler(ch)

    # catch uncaughted exceptions and write to log
    def excepthook(exctype, value, tb):
        str_tb = '\n'.join(traceback.format_tb(tb))
        logging.error('Uncaught exception.\n%s: %s\nTraceback:\n%s', exctype.__name__, value, str_tb)
    sys.excepthook = excepthook


class Mailer:
    """
    Send email message to all emails addresses from the list

    Args:
        server_url: str
        account: dict {"user": str, "password": str}
        emails_file: str
        message: dict {"file": str, "subject": str, "from": str}
        timeout: float, default 60
    """

    def __init__(self, server_url, account, emails_file, message, timeout=60):
        if not isinstance(server_url, str):
            raise TypeError('type of server_url must be str not %s' % type(server_url))

        if not isinstance(account, dict):
            raise TypeError('type of account must be dict not %s' % type(account))

        if not isinstance(emails_file, str):
            raise TypeError('type of emails_file must be str not %s' % type(emails_file))

        if not isinstance(message, dict):
            raise TypeError('type of message must be dict not %s' % type(message))

        if not isinstance(timeout, Number):
            raise TypeError('type of timeout must be float not %s' % type(timeout))

        self.server_url = server_url
        self.emails_file = emails_file
        self.message_file = message['file']
        self.subject = message['subject']
        self.from_ = message['from']
        self.timeout = timeout  # seconds

        self.user = account['user']
        self.password = account['password']
        self.server = self.login_server()
        logging.debug('Connected to e-mail server')

        with open(self.message_file) as fp:
            self.message = fp.read()
            logging.debug('Message is loaded from file %s' % self.message_file)

    def close(self):
        server.quit()
        server.close()

    def login_server(self):
        """Connect to remote email server and login"""

        server = smtplib.SMTP(self.server_url)

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(self.user, self.password)

        return server

    def get_message(self, email):
        """Create instance of MIMEText and set properties"""

        message = MIMEText(self.message, 'html')

        message['Subject'] = self.subject
        message['From'] = self.from_
        message['To'] = email

        return message

    def send_email(self, email):
        """Send message to email through email server"""

        if not isinstance(email, str):
            raise TypeError('type of email must be str not %s' % type(email))

        message = self.get_message(email)
        self.server.send_message(message)

    def send_emails(self):
        """Send email message to all emails in the list"""

        with open(self.emails_file) as fp:
            emails = fp.readlines()
        logging.debug('%s e-mail addresses are loaded from %s' % (len(emails), self.emails_file))

        emails = map(lambda email: email.strip(), emails)

        for i, email in enumerate(emails):
            try:
                self.send_email(email)
            except Exception as e:
                logging.exception('Can\'t send e-mail to %s (number %s)!' % (email, i))
            else:
                logging.debug('E-mail was sent to %s (number %s)' % (email, i))

            sleep_time = self.timeout * (0.5 + random.random())
            time.sleep(sleep_time)  # timeout

        logging.debug('Done!')


if __name__ == '__main__':
    _init_logging()

    CONFIG_FILE = "config.json"

    with open(CONFIG_FILE) as fp:
        config = json.load(fp)

    mailer = Mailer(**config)
    mailer.send_emails()

