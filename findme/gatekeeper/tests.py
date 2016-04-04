# -*- coding: utf-8 -*-
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
import tests

from django.contrib.auth import get_user_model
from gatekeeper import models
from gatekeeper import views

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
        # delete the users
        self.created_users = list()
        User.objects.all().delete()
        
        # related profile must have been delete as well
        profiles = models.UserProfile.objects.all()
        self.assertEquals(len(profiles), 0)        

    def create_user_profile(self, p):
        first_name = 'delete'
        last_name = 'me'
        i = self._user_counter
        username = '%s%s%d' % (first_name, last_name, i)
        self._user_counter += 1
        
        # create a userprofile when a user is created
        self.user = User.objects.create_user(
            email='%s@example.com' % username,
            username=username,
            password = p,
            first_name=first_name,
            last_name=last_name,
        )
        self.user.set_password(p)
        self.user.save()
        self.created_users.append(self.user)
        return self.user
        
    def create_superuser_profile(self, p):
        first_name = 'admin'
        last_name = 'me'
        i = self._user_counter
        username = '%s%s%d' % (first_name, last_name, i)
        self._user_counter += 1
        
        # create a admin profile when a admin is created
        self.admin = User.objects.create_superuser(
            email='%s@example.com' % username,
            username=username,
            password = p,
            first_name=first_name,
            last_name=last_name,
        )
        self.admin.set_password(p)
        self.admin.save()  
        self.created_users.append(self.admin)       
        return self.admin

class TestUserProfileModel(tests.TestUserBase):
    
    def setUp(self):
        super(TestUserProfileModel, self).setUp()
        TestUserBase.setUp(self)
        TestUserBase.create_user_profile(self, "password")
        TestUserBase.create_superuser_profile(self, "password")
        self.user = self.created_users.pop(0)
        self.admin = self.created_users.pop(0)
        self.client = Client()
        
    def test_user_profile(self):
        # Check that a Profile instance has been created
        self.assertIsInstance(self.user, models.UserProfile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.is_active)
        self.user.save()
        
    def test_admin_profile(self):
        # Check that a Profile instance has been created
        self.assertIsInstance(self.admin, models.UserProfile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace 
        self.assertTrue(self.admin.is_admin)
        self.assertTrue(self.admin.is_active)
        self.admin.save() 
        
    def test_user_login(self):
        login = self.client.login(username=self.user.username, password="password") 
        self.assertTrue(login)
        
    def test_admin_login(self):
        login = self.client.login(username=self.admin.username, password="password") 
        self.assertTrue(login)
        
    def test_user_logout(self):
        login = self.client.login(username=self.user.username, password="password") 
        logout = self.client.logout()
        self.assertIsNone(logout)  
                
    def test_admin_logout(self):
        login = self.client.login(username=self.admin.username, password="password") 
        logout = self.client.logout()
        self.assertIsNone(logout)  
        
    def test_create_multiple_users(self):
        users = 20
        for num in range(users):
            TestUserBase.create_user_profile(self, "password")
        created_users = len(self.created_users)
        self.assertEqual(users, created_users)
        
    def tearDown(self):
        self._user_counter = 0
        # delete the users
        self.created_users = list()
        User.objects.all().delete()
        self.client.logout()
        self.user.delete()
        self.admin.delete()
        
        # related profile must have been delete as well
        profiles = models.UserProfile.objects.all()
        self.assertEquals(len(profiles), 0)                

class TestUserRegistrationView(tests.TestUserBase):
    
    def setUp(self):  
        self.client = Client()
        TestUserBase.setUp(self)
        TestUserBase.create_user_profile(self, "password")
        self.user = self.created_users.pop(0)
        self.client = Client()
        
    def test_user_register(self):
        # Get login page
        response = self.client.get(reverse('login')) 
        self.assertTrue(response, 'Register' in response.content)
        self.assertEquals(response.status_code, 200) 
        
        # Check response code
        response = self.client.post(reverse('register'), 
                                    {'username' : self.user.username,
                                     'password' : "password",
                                     'email'    : self.user.email
                                    })
        self.assertEqual(response.status_code, 200)
        
    def test_user_login(self):
        # Check 'Log in' in response
        response = self.client.get(reverse('login')) 
        self.assertTrue('Log in' in response.content)  
        
        # Check if logged in
        response = self.client.post(reverse('login'), 
                                    { 'username': self.user.username, 
                                      'password': "password"
                                    }
                                    )
        self.assertTrue(self.user.is_authenticated)
        
    def test_user_logout(self):        
        # Check if logged in
        response = self.client.post(reverse('logout'))
        self.assertIsNone(response.context)   
        self.assertRedirects(response, '/')     