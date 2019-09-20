from django.test import TestCase
from .forms import AddPostForm

class TestAddPostForm(TestCase):

    def test_post_has_title_and_body(self):
        form = AddPostForm({
            'title': 'Post Title',
            'body': 'Post Body',
            'topic': 'None'
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
        
    def test_post_without_title_or_body(self):
        form = AddPostForm({
            'title': 'Post Title',
            'body': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['body'], ['This field is required.'])
