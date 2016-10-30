from django.test import TestCase

#from django.contrib.auth
from api.models import *

class UserTests(TestCase):
    
    def test_username_field(self):
        user = User(username="username")
        profile = UserProfile(user=user)
        self.assertEquals(profile.username, user.username)


    def test_queue_owner(self):
        user = User()
        user.save()
    
        profile = UserProfile(user=user)
        profile.save()

        queue = Queue(owner=profile)
        queue.save()

        self.assertEquals(queue.owner, profile)
        self.assertIs(queue in profile.queues.all(), True)
