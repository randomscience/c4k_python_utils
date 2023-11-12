# c4k_python_utils

## Installation
```bash
pip install git+https://github.com/randomscience/c4k_python_utils
```
## Logging
Discord:
```python
from c4k_python_utils.log import DiscordLogHandler
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        DiscordLogHandler(
            "App name",
            channel_id=1173021520763826236,
            token="token"
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    logging.error("log message")

main()
```

Email:
```python
import logging
from c4k_python_utils.log import EmailLogHandler

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        EmailLogHandler(
            "App name",
            ["mateuszkojro@outlook.com"], # Recivers emails
            "email@email.com", # Sender email
            "password", # Sender password
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```
