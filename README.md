# Dummy Message Board System

- This repo contains the source code for a dummy message board system.

## Requirements
- The system should be implemented with loose coupling to their classes.
- The system should follow the observer behavioral pattern.
- User needs to be able to subscribe the message board.
- User needs to be able to unsubscribe from the message board.
- The message board can be either public or private. Private message boards
require password to subscribe, public ones don't. If the provided password is
incorrect, an error should be returned back to the user. (Message board has a
pre-determined password. Basic string comparison for password checking is fine,
no need for encryption)
- At the time of subscription, user needs to be able to specify how they want to
be notified of new messages. The following channels are available: Email,
WhatApp, SMS.
- When a new message is posted to the message board, all subscribers need to be
notified via channels they have indicated.

## Solutions
- The source codes include the `main.py` functions that contains the following classes:
  - Abstract Class `Board`: The Board interface declares a set of methods for managing Users.
  - Concrete Class `PublicBoard` which implements Abstract Class `Board` to Add/Remove Users and call Notify, which
  will invoke when there is a new message is posted on the message board. This class also supports `add_channels` 
  functions to define which notification channels are available.
    - The `Add` function also checks the request notification channel from User when it subscribes to the Board.
    If the channel is not available at the Board, the subscription will be denied.
  - Concrete Class `PrivateBoard` is inherited from `PublicBoard` class and have an extra function for authentication
  when the user subscribes to this `PrivateBoard`.
  - Abstract Class `User`: The User interface declares the notify method, used by Boards.
  - Concrete Class `ConcreteUser` which implements Abstract Class `User` to Subscribe/Unsubscribe to/from a Board,
  and a Notify function to notify on the registered notification channel. The `Update` function is used when the
  user wants to change the subscription preference.
  - Abstract Class `Channel`: Notification Channel.
  - There Concrete Classes for Email, WhatsApp, and SMS notification channels.
- The source codes also include the `test_main.py` for some basic unit tests.

## Run the codes
- The system is implemented using Python 3.8.
- To run this, simply using:

```bash
python main.py
python test_main.py
```

