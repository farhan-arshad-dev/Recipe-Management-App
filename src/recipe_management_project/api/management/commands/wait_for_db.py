# 'time' use for the application sleep for some sec
import time

# get and check the database connection
from django.db import connections
# raise by the django when database is not available and trying to connect with
# with database
from django.db.utils import OperationalError
# User to create the custom management command
from django.core.management.base import BaseCommand


# Management Command to check that database is available or not
class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # Execute when ever managemet command is run.
    def handle(self, *args, **options):
        # Statment to print the output in the console from the command
        self.stdout.write('waiting for database...')
        db_conn = None
        # check 'db_conn' not 'None'
        while not db_conn:
            try:
                # get the database connection if not available then raise
                # 'OperationalError' exception, so catch the exception and wait
                # for 1 sec
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unabailable, waiting 1 second...')
                # Sleep for 1 sec
                time.sleep(1)
        # Output the message in standred green text color.
        self.stdout.write(self.style.SUCCESS('Database available!'))
