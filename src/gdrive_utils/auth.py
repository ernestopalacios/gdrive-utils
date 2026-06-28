"""Google authentication using modern google-auth."""

import logging
from pathlib import Path

import gspread
from google.auth.exceptions import GoogleAuthError
from google.oauth2.service_account import Credentials

from .config import GDriveConfig
from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)


def authorize(config: GDriveConfig | None = None) -> gspread.Client:
    """Authenticate with Google and return an authorised *gspread* client.

    Args:
        config: A :class:`GDriveConfig` instance. If ``None``, default
            configuration is used.

    Raises:
        AuthenticationError: If the credentials file is missing or invalid.

    """
    if config is None:
        config = GDriveConfig()

    creds_path = Path(config.credentials_path)
    if not creds_path.exists():
        raise AuthenticationError(
            f"Credentials file not found: {creds_path.resolve()}"
        )

    try:
        credentials = Credentials.from_service_account_file(
            str(creds_path), scopes=config.scope
        )
        client = gspread.authorize(credentials)
        logger.info("Authentication successful!")
        return client
    except (GoogleAuthError, ValueError, OSError) as exc:
        logger.error("Authentication failed: %s", exc)
        raise AuthenticationError(f"Authentication failed: {exc}") from exc
