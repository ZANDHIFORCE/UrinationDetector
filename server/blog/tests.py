from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from .models import Post


class ApiTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings = override_settings(MEDIA_ROOT=self.media.name)
        self.settings.enable()
        self.addCleanup(self.settings.disable)
        self.api = APIClient()

    def test_image_create_list_and_label(self):
        content = BytesIO()
        Image.new('RGB', (2, 2)).save(content, format='JPEG')
        image = SimpleUploadedFile('sample.jpg', content.getvalue(), content_type='image/jpeg')
        response = self.api.post('/api_root/Posts/', {
            'title': 'Person', 'text': 'person, ', 'label': 'UCF', 'image': image,
        }, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(set(response.data), {
            'title', 'text', 'created_date', 'published_date', 'label', 'image',
        })
        post = Post.objects.get()
        self.assertTrue(post.image.storage.exists(post.image.name))
        self.assertEqual(self.api.get('/api_root/Posts/').data[0]['label'], 'UCF')
        self.assertEqual(self.api.get('/api_root/latest-UCF/').data['title'], 'Person')
        response = self.api.put('/api_root/latest-UCF/', {'label': 'URN'}, format='json')
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.label, 'URN')
        self.assertEqual(self.api.get('/').status_code, 200)
        self.assertEqual(self.api.get('/post/'+str(post.pk)).status_code, 200)
        self.assertEqual(self.api.get('/admin/').status_code, 302)

    def test_empty_latest_preserves_response(self):
        response = self.api.get('/api_root/latest-UCF/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], '')
        self.assertEqual(response.data['text'], '')
        self.assertIsNone(response.data['image'])
        self.assertEqual(self.api.put('/api_root/latest-UCF/', {'label': 'URN'}, format='json').status_code, 404)

    def test_latest_keeps_first_record_and_rejects_invalid_label(self):
        first = Post.objects.create(title='first', text='')
        Post.objects.create(title='second', text='')
        self.assertEqual(self.api.get('/api_root/latest-UCF/').data['title'], first.title)
        self.assertEqual(self.api.put('/api_root/latest-UCF/', {'label': 'invalid'}, format='json').status_code, 400)

    def test_local_token_login(self):
        user = get_user_model().objects.create_user(username='local-test', password='test-only-password')
        response = self.api.post('/api-token-auth/', {'username': user.username, 'password': 'test-only-password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['token'])
        response = self.api.post('/api-token-auth/', {'username': user.username, 'password': 'wrong'})
        self.assertEqual(response.status_code, 400)
