"""Utils for cognito authentication."""

import base64
import hashlib
import hmac


def generate_secret_hash(
    username: str,
    client_id: str,
    client_secret: str,
) -> str:
    """Generate a secret hash for AWS Cognito Client."""
    message = username + client_id
    digest = hmac.new(
        client_secret.encode("utf-8"),
        message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(digest).decode("utf-8")
