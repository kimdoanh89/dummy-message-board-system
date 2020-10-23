import unittest
from unittest import TestCase
from main import PublicBoard, ConcreteUser, PrivateBoard, EmailChannel, SmsChannel


class TestPublicBoard(TestCase):
    def test_name(self):
        public_board = PublicBoard(name="Public Board")
        self.assertEqual(public_board.name, "Public Board")

    def test_new_post(self):
        public_board = PublicBoard(name="Public Board")
        public_board.new_post = "Second Post!!!"
        self.assertEqual(public_board.new_post, "Second Post!!!")

    def test_add(self):
        public_board = PublicBoard(name="Public Board")
        user1 = ConcreteUser(name="Doanh", password="Admin")
        sms = SmsChannel()
        public_board.add_channels([sms])
        user1.request_channel = sms
        public_board.add(user1)
        self.assertIn(user1, public_board._users)

    def test_remove(self):
        public_board = PublicBoard(name="Public Board")
        user1 = ConcreteUser(name="Doanh", password="Admin")
        user2 = ConcreteUser(name="Kim", password="Admin")
        sms = SmsChannel()
        public_board.add_channels([sms])
        user1.request_channel = sms
        public_board.add(user1)
        result1 = public_board.remove(user1)
        self.assertTrue(result1)
        result2 = public_board.remove(user2)
        self.assertFalse(result2)

    def test_notify(self):
        pass


class TestPrivateBoard(TestCase):
    def test_password(self):
        private_board = PrivateBoard(name="Private Board", board_password="Admin")
        self.assertEqual(private_board.password, "Admin")

    def test_authenticate(self):
        user1 = ConcreteUser(name="Doanh", password="Admin")
        user2 = ConcreteUser(name="Dan", password="admin")
        private_board = PrivateBoard(name="Private Board", board_password="Admin")
        result1 = private_board.authenticate(user1)
        self.assertTrue(result1)
        result2 = private_board.authenticate(user2)
        self.assertFalse(result2)


class TestConcreteUser(TestCase):
    def test_username(self):
        user1 = ConcreteUser(name="Doanh", password="Admin")
        self.assertEqual(user1.username, "Doanh")

    def test_password(self):
        user1 = ConcreteUser(name="Doanh", password="Admin")
        self.assertEqual(user1.password, "Admin")

    def test_boards(self):
        pass

    def test_subscribe(self):
        pass

    def test_unsubscribe(self):
        pass

    def test_notify(self):
        pass

    def test_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
