# Watcher-daemon

**this is not currently working! Also, it only works on linux, not Windows, due to daemon.**

This continuously monitors a webpage for changes. If a change is detected, it logs the updated content and emails with the updated content.

## Getting Started

### Prerequisites

Requires the following Python libraries: `python-daemon`, `requests`, `beautifulsoup4` and `hashlib`.

### Installing

```bash
git clone git@github.com:garthmortensen/watcher_daemon.git
cd watcher_daemon
python3 -m venv env
source myenv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python watcher.py
```

Modify the URL:

```python
if __name__ == "__main__":
    daemon = WebpageMonitorDaemon('https://www.coolstuff.com', './log/daemon-log.txt')
    daemon.run()
```

Add email server deets and creds in the `send_email_notification` method for the email to work.

## Run Tests

```bash
pytest .
```

