from django.test import TestCase
from .models import Post, Profile
from django.contrib.auth.models import User

import time

class ProfileTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username="A", password="A")
        u2 = User.objects.create(username="B", password="B")
        Profile.objects.create(user=u1, bio="A")
        Profile.objects.create(user=u2, bio="B")

    def test_profile_can_sub_other_profile(self):
        p1 = User.objects.get(username="A").profile
        p2 = User.objects.get(username="B").profile
        p1.friends.add(p2)
        self.assertEqual(len(p1.friends.all()), 1)
        p2.subs.add(p1)
        self.assertEqual(len(p2.subs.all()), 1)

    def test_profile_can_change_bio(self):
        p1 = User.objects.get(username="A").profile
        before = p1.bio
        p1.bio = "D"
        after = p1.bio
        self.assertTrue(before != after)

    def test_profile_can_change_to_string(self):
        p2 = User.objects.get(username="B").profile
        self.assertTrue('Profile for user {}'.format("B") == str(p2))

class PostTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(username="A", password="A")
        Profile.objects.create(user=u1, bio="A")

    def test_create_post(self):
        p1 = User.objects.get(username="A").profile
        p1.post_set.create(text="A", date=time.time())
        self.assertTrue(len(p1.post_set.all()) == 1)

    def test_multiple_create_post(self):
        p1 = User.objects.get(username="A").profile
        for i in range(10):
            p1.post_set.create(text=str(i), date=time.time())
        self.assertTrue(len(p1.post_set.all()) == 10)

