# c4k_python_utils

## Installation
```bash
pip install git+https://github.com/randomscience/c4k_python_utils
```
## Logging
Basic logger setup:
```python
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        EmailLogHandler(
            "App name",
            ["mateuszkojro@outlook.com"],
            SENDER_EMAIL,
            PASSWORD,
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```
