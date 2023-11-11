import logging
from abc import ABC, abstractmethod
import unittest
import smtplib
import ssl


class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str, level_name: str, app_name: str):
        pass


class EmailNotifier(Notifier):
    @staticmethod
    def _send_mail(
        receiver,
        subject,
        message,
        password,
        sender_email,
        smtp_server="smtp.gmail.com",
        port=465,
    ):
        message = f"Subject: {subject}\n\n{message}"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, message)

    def __init__(
        self,
        receivers,
        sender_email,
        password,
        smtp_server="smtp.gmail.com",
        smtp_port=465,
    ) -> None:
        self._receivers = receivers
        self._sender_email = sender_email
        self._password = password
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port

    def notify(self, message, level_name, app_name):
        for receiver in self._receivers:
            EmailNotifier.send_mail(receiver, f"[{app_name}]] {level_name}", message)


class Logger:
    def __init__(
        self,
        app_name,
        notify_level=logging.ERROR,
        notifiers: list[Notifier] = None,
        logger: logging.Logger = None,
    ) -> None:
        self._app_name = app_name
        self._notify_level = notify_level
        self._notifiers = [] if notifiers is None else notifiers
        self._logger = (
            logging.Logger(app_name, logging.INFO) if logger is None else logger
        )

    def log(self, message, level):
        self._logger.log(level, message)

        if level >= self._notify_level:
            for notifier in self._notifiers:
                try:
                    notifier.notify(
                        message, logging.getLevelName(level), self._app_name
                    )
                except Exception as e:
                    self._logger.critical(
                        f"Could not notify with '{notifier.__class__.__name__}': {e}"
                    )

    def info(self, message):
        self.log(message, logging.INFO)

    def error(self, message):
        self.log(message, logging.ERROR)


class Test(unittest.TestCase):
    class ThrowingNotifier(Notifier):
        def notify(self, message: str, level_name: str, app_name: str):
            raise RuntimeError("Exception message")

    class DebugNotifier(Notifier):
        def __init__(self) -> None:
            self.notifications = []

        def notify(self, message: str, level_name: str, app_name: str):
            self.notifications.append(message)

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)

    def test_never_crash(self):
        logger = Logger("app", notifiers=[self.ThrowingNotifier()])
        logger.error("aa")

    def test_send_notification_when_appropriate(self):
        debug_notifier = self.DebugNotifier()
        logger = Logger("app", notify_level=logging.INFO, notifiers=[debug_notifier])

        log_message = "log"
        logger.info(log_message)
        self.assertIn(log_message, debug_notifier.notifications)

        error_message = "error"
        logger.error(error_message)
        self.assertIn(error_message, debug_notifier.notifications)

    def test_dont_send_notification_when_not_appropriate(self):
        debug_notifier = self.DebugNotifier()
        logger = Logger("app", notify_level=logging.ERROR, notifiers=[debug_notifier])
        message = "aaa"
        logger.info(message)
        self.assertNotIn(message, debug_notifier.notifications)


if __name__ == "__main__":
    unittest.main()
