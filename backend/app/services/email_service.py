import logging
import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from app.core.config import settings


logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "email"

class EmailService:
    def __init__(
            self,
    ):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME

        self.template_env = Environment(
            loader = FileSystemLoader(TEMPLATES_DIR),
            autoescape = True
        )

    async def _send_raw_email(
            self,
            recipient: str,
            subject: str,
            text_content: str,
            html_content: str
    ) -> bool:
        
        """
        Assemble the email's MIME parts and send it via the SMTP server.

        Args:
            recipient: The recipient's email address.
            subject: The subject of the email.
            text_content: The plain-text version of the email body.
            html_content: The HTML version of the email body.

        Returns:
            True if the email was sent successfully.

        Raises:
            aiosmtplib.SMTPException: If an SMTP error occurs while
                sending the email.
            OSError: If a network or connection error occurs.
                """

        message = MIMEMultipart("alternative")

        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = recipient
        message["Subject"] = subject

        # Plain text must be attached first, HTML second
        # Email clients prioritize the last attached part
        message.attach(MIMEText(text_content, "plain", "utf-8"))
        message.attach(MIMEText(html_content, "html", "utf-8"))

        try:
            await aiosmtplib.send(
                message,
                hostname = self.host,
                port = self.port,
                username = self.username,
                password = self.password,
                start_tls = True
            )

            logger.info(
                "Email successfully send to %s",
                recipient
            )

            return True
        
        except aiosmtplib.SMTPException as exc:
            logger.exception(
                "SMTP error while sending to %s",
                recipient
            )

            raise RuntimeError(f"SMTP delivery failed: {exc}") from exc
        
        except OSError as exc:
            logger.exception(
                "Network error while sending email to %s",
                recipient
            )

            raise RuntimeError(f"Unnable to connect to mail server: {exc}") from exc
        
    async def send_verification_email(
            self,
            email: str,
            verification_url: str
    ) -> bool:
        
        """
        Sends the user verfication link.

        Args:
            email: The recipient's email address.
            verification_url: The URL the user should visit to verify their email address.
        
        Returns:
            True if the email was sent successfully.

        Raises:
            aiosmtplib.SMTPException: If an SMTP error occurs
                while sending the email.
            OSError: If a network or connection error occurs.
        """

        subject = f"Verify your {self.from_name} account"

        context = {
            "project_name": self.from_name,
            "verification_url": verification_url
        }

        text_template = self.template_env.get_template("verify_email.txt")
        html_template = self.template_env.get_template("verify_email.html")

        text_content = text_template.render(context)
        html_content = html_template.render(context)

        return await self._send_raw_email(
            recipient=email,
            subject=subject,
            text_content=text_content,
            html_content=html_content
        )

    async def send_password_reset_email(
            self,
            email: str,
            reset_url: str,
    ) -> bool:

        subject = f"Reset your {self.from_name} password"

        context = {
            "project_name": self.from_name,
            "reset_url": reset_url
        }

        text_template = self.template_env.get_template("password_reset.txt")
        html_template = self.template_env.get_template("password_reset.html")

        text_content = text_template.render(context)
        html_content = html_template.render(context)

        return await self._send_raw_email(
            recipient=email,
            subject=subject,
            text_content=text_content,
            html_content=html_content
        )
