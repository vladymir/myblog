"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from posts.models import Post

class SimpleTest(TestCase):
    def test_creating_new_post_and_saving_to_database(self):
        #start creating a new post
        post = Post()
        post.title = "My first post"
        post.pub_date = timezone.now()
        
        post.save()
        
        all_posts_in_database = Post.objects.all()
        self.assertEquals(len(all_posts_in_database),1)
        only_post_in_database = all_posts_in_database[0]
        self.assertEquals(only_post_in_database, post)
        
        self.assertEquals(only_post_in_database.title, "My first post")
        self.assertEquals(only_post_in_database.pub_date, post.pub_date)