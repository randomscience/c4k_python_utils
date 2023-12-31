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
        app_name,
        receivers,
        sender_email,
        password,
        notify_level=logging.ERROR,
        smtp_server="smtp.gmail.com",
        smtp_port=465,
    ) -> None:
        super().__init__()
        self._app_name = app_name
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
                    f"[{self._app_name}] {record.levelname}",
                    self.format(record),
                    self._password,
                    self._sender_email
                )
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

class DiscordLogHandler(logging.Handler):

    def __init__(self, app_name, channel_id, token, notify_level=logging.ERROR) -> None:
        import discord
        super().__init__()
        self._app_name = app_name
        self._channel_id = channel_id
        self._token = token
        self._notify_level = notify_level

    def _send_message(self, message):
        import discord
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():  #  Called when internal cache is loaded
            channel = client.get_channel(self._channel_id) #  Gets channel from internal cache
            await channel.send(message)
            # result = await channel.send(file=discord.File(open(".env", "r"))) #  Sends message to channel)
            # result = await channel.send(embed=discord.Embed()) #  Sends message to channel)
            await client.close()
        client.run(self._token)  # Starts up the bot
    
    def handleError(self, record: logging.LogRecord) -> None:
        return super().handleError(record)

    def emit(self, record: logging.LogRecord):
        try:
            if record.levelno < self._notify_level:
                return

            message = f"""
# {record.levelname} in {self._app_name}
{record.levelname} occured in `{record.funcName}:{record.module}` with message:
```
{self.format(record)}
```
"""
            self._send_message(message)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)