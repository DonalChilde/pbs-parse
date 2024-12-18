"""messsenger."""

from collections.abc import Sequence
from typing import Any, Protocol


class MessengerProtocol(Protocol):
    """Messenger protocol."""

    def send(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Send a message."""


class NullMessenger(MessengerProtocol):
    """NullMessenger.

    Does nothing.
    """

    def send(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Do nothing."""
        return None


class PrintMessenger(MessengerProtocol):
    """PrintMessenger.

    Prints args.
    """

    def send(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Print args."""
        print(msg, *args)
        return None


class MessageDispatcher(MessengerProtocol):
    """MessageDispatcher.

    Send the same message to a group of messengers.
    """

    def __init__(self, messengers: Sequence[MessengerProtocol]) -> None:
        """MessageDispatcher.

        Args:
            messengers (Sequence[MessengerProtocol]): _description_
        """
        self.messengers = messengers

    def send(self, msg: str, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Send the message to all the messengers."""
        for messenger in self.messengers:
            messenger.send(msg, *args, **kwargs)
