import os
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status
from PIL import Image
from hjd.models import Hjd
from accounts.models import User
from restaurant.models import Restaurant, Categories


class EditorCreateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # 필요한 테스트 데이터를 생성합니다.

        self.admin_user = User.objects.create_superuser(
            name='admin',
            email='admin@test.com',
            password='testpassword'
        )

        self.hjd_instance = Hjd.objects.create(
            id=1
        )

        self.category_instance = Categories.objects.create(
            category_name='TestCategory'

        )

        self.restaurant1 = Restaurant.objects.create(
            name='Test Restaurant 1',
            user=self.admin_user,
            area_id=self.hjd_instance,
            category_name=self.category_instance,

        )

        # 임시 이미지 파일 생성
        image = Image.new('RGB', (100, 100))
        image.save('test_image.jpg')

    def test_editor_create(self):
        url = reverse('editor_create')

        refresh_token = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh_token.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


        with open('test_image.jpg', 'rb') as img:
            data = {
                'rest_id': [self.restaurant1.pk],
                'user': self.admin_user.name,
                'title': 'Test Title',
                'content': 'Test Content',
                'view': 0,
                'image': img,
            }

            from editor.views import editor_create
            factory = APIRequestFactory()
            request = factory.post(url, data, format='multipart')
            force_authenticate(request, user=self.admin_user)

            response = editor_create(request)

        os.remove('test_image.jpg')  # 테스트가 끝난 후 임시 이미지 파일 삭제

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
