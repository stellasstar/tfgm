# -*- coding: utf-8 -*-
from django.test import TestCase, Client
import tests

from django.contrib.auth import get_user_model
from gatekeeper import models

#import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
class TestUserBase(TestCase):

    def setUp(self):
        super(TestUserBase, self).setUp()
        self._user_counter = 0
        self.created_users = list()
        # delete the users
        User.objects.all().delete()
        
        # related profile must have been delete as well
        profiles = UserProfile.objects.all()
        self.assertEquals(len(profiles), 0)        

    def create_user(self):
        first_name = 'delete'
        last_name = 'me'
        i = self._user_counter
        username = '%s%s%d' % (first_name, last_name, i)
        self._user_counter += 1

        user = User.objects.create(
            email='%s@example.com' % username,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        self.created_users.append(user)
        return user    

class TestUserProfileModel(tests.TestUserBase):
    
    def setUp(self):
        super(TestUserProfileModel, self).setUp()
        TestUserBase.setUp(self)
        self.user = self.create_user()
        
    def test_user_profile(self):
        # Check that a Profile instance has been crated
        self.assertIsInstance(self.user.UserProfile, models.UserProfile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        self.user.save()

class TestUserRegistrationView(tests.TestUserBase):
    
    def setUp(self):  
        self.client = Client()
        TestUserBase.setUp(self)
        self.user = self.create_user()
        
    def test_user_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register Your Account')

        response = self.client.post('/register/', (self.user))
        self.assertEqual(response.status_code, 200)
