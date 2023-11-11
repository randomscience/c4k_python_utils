# c4k_python_utils

## Installation
```bash
pip install git+https://github.com/randomscience/c4k_python_utils
```
## Logging
Basic logger setup:
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
