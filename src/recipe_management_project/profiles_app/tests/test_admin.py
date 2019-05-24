# This file holds the unit test code for the admin page
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # Client means admin panel of the website
        # self inside the method makes the varible as data member of the class
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@arbisoft.com",
            name="Admin",
            password="password123"
        )
        # allows to user login using django authentication
        self.client.force_login(self.admin_user)
        # create regular user to test in the list in our app
        self.user = get_user_model().objects.create_user(
            email='test@arbisoft.com',
            name='Test User',
            password='password123'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generate the url for our list user page from the admin using reverse
        # method
        # In future if we change the url for the list user page then reverse
        #  method automatically generate the the url for thr user list page
        # TODO: Reference how to prepare constat(should be in lower case) for
        # the reverse function
        # https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#reversing-admin-urls
        url = reverse('admin:profiles_app_userprofile_changelist')
        # perform http request and get the response
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # test that the chage page renders correctly
    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse(
            'admin:profiles_app_userprofile_change',
            args=[self.user.id]
            )
        # reverse method generate the url like the following example
        # /admin/profiles_app/user_profile/1
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    # Test that the page to add the new user renders correctly
    def test_create_user_page(self):
        """Test the the create user page works"""
        url = reverse('admin:profiles_app_userprofile_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
