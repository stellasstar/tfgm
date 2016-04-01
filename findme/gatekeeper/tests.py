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
        print User
        User.objects.all().delete()
        
        # related profile must have been delete as well
        profiles = models.UserProfile.objects.all()
        self.assertEquals(len(profiles), 0)        

    def create_user_profile(self):
        first_name = 'delete'
        last_name = 'me'
        i = self._user_counter
        username = '%s%s%d' % (first_name, last_name, i)
        self._user_counter += 1
        
        # create a userprofile when a user is created
        user = User.objects.create(
            email='%s@example.com' % username,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        print user

        # related profile has to exist
        profile = models.UserProfile.objects.get(user) 
        
        self.created_users.append(user)
        return (user, profile)

class TestUserProfileModel(tests.TestUserBase):
    
    def setUp(self):
        super(TestUserProfileModel, self).setUp()
        TestUserBase.setUp(self)
        (self.user, self.profile) = self.create_user_profile()
        
    def test_user_profile(self):
        u = self.user
        p = self.profile
        # Check that a Profile instance has been created
        self.assertEquals(p,u)
        self.assertIsInstance(p, models.UserProfile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        self.user.save()

class TestUserRegistrationView(tests.TestUserBase):
    
    def setUp(self):  
        self.client = Client()
        TestUserBase.setUp(self)
        (self.user, self.profile) = self.create_user_profile()
        self.user.save()
        
    def test_user_register(self):
        # Get login page
        response = self.client.get('/gatekeeper/register/', follow=True)
        self.assertTrue(response, 'Register' in response.content)
        
        # Check response code
        self.assertEquals(response.status_code, 200)       
    
        response = self.client.post('/register/', (self.user))
        self.assertEqual(response.status_code, 200)
        
    def test_user_login(self):
        # Check 'Log in' in response
        response = self.client.get('/gatekeeper/login/', follow=True)
        self.assertTrue('Log in' in response.content)         
