# patch function help us to mock the behaviour of the django get a database
# function, and simulate that database is being available or not being
# available.
from unittest.mock import patch

# 'call_command' help to call the command
from django.core.management import call_command
# 'OperationalError' throughts by the django when database is unavailable
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # variable 'gi' is the abrivation of __getitem__ can be change
        # "gi" mocked variable does two things,
        # 1. return the value that we specify.
        # 2. moniter how many times it was called.
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mock the connection handler and just return True when its called
            gi.return_value = True
            # 'wait_for_db' is the management command that help of command
            # allow us to wait for the database to be available before continue
            # and running other commands and use ni docker a composed file when
            # starting the app, because some time postgres database failes to
            # start because of database error. It turns out this because
            # postgres service started it needs to done few some extra set set
            # up task before accepting the connections. On the other hand app
            # will try and connect with the database before its ready so its
            # fails with the exception. In simple it ensure that database is up
            # and ready to accept the connections.
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # check the database 5 times is it available or not
    # 'patch' decorator to remove the delay, and speed up the test while
    # checking the database by mocking the time and return value a paramter as
    # part of the function.
    @patch('time.sleep', return_value=True)
    # 'ts' parameter abbreviated as timesleep if don;t then test return error
    # unexpected arguments.
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # 'side_effect' raise the OperationalError 5 time and then sixth
            # time is won't raise the error and just return True the call
            # should complete.
            # '[OperationalError] * 5' repeat list item five time in the list
            # when we call the '__getitem__' five times.
            gi.side_effect = [OperationalError] * 5 + [True]
            # 'wait_for_db' have a while llop that check to see if the
            # connection raises the operational error if it does then it's
            # going to wait a second and try again. we need to remove that
            # delay in this unit test by adding patch decorator to this
            # function.
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
