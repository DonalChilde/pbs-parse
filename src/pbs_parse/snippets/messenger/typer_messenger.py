"""TyperMessenger."""

from typing import Any

from typer import echo

from .messenger import MessengerProtocol


class TyperMessenger(MessengerProtocol):
    """TyperMessenger."""

    def send(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Print the message to the stdout via typer."""
        echo(msg)
