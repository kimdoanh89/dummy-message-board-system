"""
Problem description:
Using Python (any version), show how the observer behavioral pattern can be
used to implement a mechanism allowing event handlers to react without tight
 coupling to their classes. Use the pattern to implement a dummy message board
 system.
Requirements:
User needs to be able to subscribe the message board.
User needs to be able to unsubscribe from the message board.
The message board can be either public or private. Private message boards
require password to subscribe, public ones don't. If the provided password is
incorrect, an error should be returned back to the user. (Message board has a
pre-determined password. Basic string comparison for password checking is fine,
no need for encryption)
At the time of subscription, user needs to be able to specify how they want to
be notified of new messages. The following channels are available: Email,
WhatApp, SMS.
When a new message is posted to the message board, all subscribers need to be
notified via channels they have indicated.
No user interface is required here. The solution should be implemented
entirely using classes & built in python data types.
Output should be printed to console using built in methods.
Entire solution should be contained within a single python module. No external
communication is required.
Optional extras:
User needs to be able to update their subscription preferences after
registering.
Provide unit tests with your solution.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Board(ABC):
    """
    The Board interface declares a set of methods for managing Users.
    """
    _newPost: str

    _users: List[User] = []
    """
    List of Users.
    """

    _channels: List[Channel] = []
    """
    List of Channels.
    """

    def __init__(self, name):
        self._name = name
        self._users = []

    @property
    def name(self):
        return self._name

    @property
    def new_post(self):
        return self._newPost

    @new_post.setter
    def new_post(self, message):
        self._newPost = message
        print(f"New message has been posted to the {self._name}: {message}")
        self.notify()

    @abstractmethod
    def add(self, user: User):
        """
        Add a user to the Board.
        """
        pass

    @abstractmethod
    def remove(self, user: User):
        """
        Remove a user from the Board.
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all Users about an event.
        """

    @abstractmethod
    def add_channels(self, channels: List[Channel]):
        """
        Add list of notification channels to the Board.
        """
        pass


class PublicBoard(Board):
    """
    The Board notifies all Users when a new message is posted to the board.
    """
    def __init__(self, name):
        super().__init__(name=name)
        self._users = []
        self._channels = []

    def add(self, user: ConcreteUser):
        # If the request notification channel is available at the Board
        if user.request_channel in self._channels:
            # If the user has not been subscribed to this Board.
            if user not in self._users:
                self._users.append(user)
                print(f"User {user.username} has subscribed to the {self._name}")
                return True
            else:
                print(f"Failed to add: {user.username}")
                return False
        else:
            print(f"User {user.username}: channel {user.request_channel.name} is not available at the board!!")
            return False

    def remove(self, user: ConcreteUser):
        try:
            self._users.remove(user)
            print(f"User {user.username} has unsubscribed from the {self._name}!")
            return True
        except ValueError:
            print(f"Failed to remove: {user.username}")
            return False

    def add_channels(self, channels: List[Channel]):
        if channels not in self._channels:
            for channel in channels:
                self._channels.append(channel)
                print(f"Channel {channel.name} has been added to the {self._name}")
            return True
        else:
            for channel in channels:
                print(f"Failed to add: {channel.name}")
            return False

    def notify(self):
        """
        Trigger the notification through Channel in each User.
        """
        print(f"{self._name}: Notifying Users about new message ...")
        for user in self._users:
            user.notify(self)
        print("="*80)


class PrivateBoard(PublicBoard):
    def __init__(self, name, board_password):
        super().__init__(name=name)
        self._board_password = board_password
        self._users = []
        self._channels = []

    @property
    def password(self):
        return self._board_password

    def authenticate(self, user):
        if user.password == self._board_password:
            print(f"User {user.username}: Successfully Authenticated!")
            return True
        else:
            print(f"User {user.username}: The password is not correct!")
            return False


class User(ABC):
    """
    The User interface declares the notify method, used by Boards.
    """

    @abstractmethod
    def subscribe(self, board, channel):
        """
        Subscribe a User to the Board.
        """
        pass

    @abstractmethod
    def unsubscribe(self, board):
        """
        Unsubscribe a User from the Board.
        """
        pass

    @abstractmethod
    def notify(self, board) -> None:
        """
        Receive notify from Board
        """
        pass

    @abstractmethod
    def update(self, board, channel) -> None:
        """
        Update the subscription preferences
        """
        pass


class ConcreteUser(User):
    def __init__(self, name, password):
        super().__init__()
        self._name = name
        self._password = password
        self._boards = {}
        self._request_channel = None
        """
        _boards dictionary to store the boards that this user subscribes to and
        its corresponding notification channels.
        """

    @property
    def username(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def boards(self):
        return self._boards

    @property
    def request_channel(self):
        return self._request_channel

    @request_channel.setter
    def request_channel(self, channel):
        self._request_channel = channel

    def subscribe(self, board, channel):
        """
        Subscribe a User to the Board.
        """
        if isinstance(board, PrivateBoard):
            if board.authenticate(self):
                self._request_channel = channel
                board.add(self)
                self._boards[f"{board.name}"] = channel
        else:
            self._request_channel = channel
            board.add(self)
            self._boards[f"{board.name}"] = channel

    def unsubscribe(self, board):
        """
        Unsubscribe a User from the Board.
        """
        board.remove(self)
        del self._boards[f"{board.name}"]

    def notify(self, board) -> None:
        print(f"Notify to {self._name} about new message!!!!")
        channel = self._boards[f"{board.name}"]
        channel.notify(board)

    def update(self, board, channel):
        """
        Update the subscription preferences
        """
        old_channel = self._boards[f"{board.name}"]
        self._boards[f"{board.name}"] = channel
        print(f"User {self._name} has changed notification channel from {old_channel.name} to {channel.name}")


class Channel(ABC):
    """
    Notification Channel
    """
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

    @abstractmethod
    def notify(self, board):
        pass


class EmailChannel(Channel):
    def __init__(self):
        super().__init__()
        self._name = "EMAIL"

    def notify(self, board):
        print(f"Notify via Email Channel!! New messages: {board.new_post}")


class SmsChannel(Channel):
    def __init__(self):
        super().__init__()
        self._name = "SMS"

    def notify(self, board):
        print(f"Notify via SMS Channel!! New messages: {board.new_post}")


class WhatsAppChannel(Channel):
    def __init__(self):
        super().__init__()
        self._name = "WhatsApp"

    def notify(self, board):
        print(f"Notify via WhatsApp Channel!! New messages: {board.new_post}")


if __name__ == "__main__":
    public_board = PublicBoard(name="Public Board")
    email = EmailChannel()
    sms = SmsChannel()
    whatsApp = WhatsAppChannel()
    # Add notification channels to the board
    public_board.add_channels([email, sms, whatsApp])

    user1 = ConcreteUser(name="Doanh", password="Admin")
    user2 = ConcreteUser(name="Dan", password="admin")
    user3 = ConcreteUser(name="Kim", password="Admin")
    user4 = ConcreteUser(name="Luong", password="Admin")

    user1.subscribe(board=public_board, channel=email)
    user2.subscribe(board=public_board, channel=sms)
    public_board.new_post = "First Post!!!"

    user2.unsubscribe(board=public_board)
    public_board.new_post = "Second Post!!!"

    user1.update(board=public_board, channel=sms)
    public_board.new_post = "Third Post!!!"

    private_board = PrivateBoard(name="Private Board", board_password="Admin")
    # Add notification channels to the board
    private_board.add_channels([email, whatsApp])
    user1.subscribe(board=private_board, channel=whatsApp)
    user2.subscribe(board=private_board, channel=sms)
    user3.subscribe(board=private_board, channel=email)
    user4.subscribe(board=private_board, channel=sms)
    # breakpoint()
    private_board.new_post = "Fourth Post!!!"

    user3.unsubscribe(board=private_board)
    private_board.new_post = "Fifth Post!!!"

    user1.update(board=private_board, channel=sms)
    private_board.new_post = "Sixth Post!!!"

    # breakpoint()
