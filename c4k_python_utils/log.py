import logging
import smtplib
import ssl


class EmailLogHandler(logging.Handler):
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
        notify_level=logging.ERROR,
        smtp_server="smtp.gmail.com",
        smtp_port=465,
    ) -> None:
        super().__init__()
        self._receivers = receivers
        self._sender_email = sender_email
        self._password = password
        self._notify_level = notify_level
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port

    def handleError(self, record: logging.LogRecord) -> None:
        return super().handleError(record)

    def emit(self, record: logging.LogRecord):
        try:
            if record.levelno < self._notify_level:
                return

            for receiver in self._receivers:
                EmailLogHandler._send_mail(
                    receiver,
                    f"[{record.name}]] {record.levelname}",
                    self.format(record),
                    self._password,
                    self._sender_email
                )
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)
