from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from hjd.models import Hjd

class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='1234', name='testuser')
        self.location = Hjd.objects.create(
            adm_nm='Test Adm_nm', sidonm='Test Sidonm', temp='Test Temp', sggnm='Test Sggnm', latitude=123.456,
            longitude=789.012)
        self.user_token = str(AccessToken.for_user(self.user))
        self.user_header = {"HTTP_AUTHORIZATION": f"Bearer {self.user_token}"}

    def test_signup(self):
        url = reverse('signup')
        data = {
            'email': 'new@example.com',
            'password': 'newpassword',
            'pw_confirm': 'newpassword',
            'name': 'New User',
            'location': self.location.adm_nm,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        data = {
            'email': self.user.email,
            'password': '1234',
        }
        response = self.client.post(url, data)
        # 사용자의 is_active가 False인 경우(이메일 인증실패)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 사용자의 is_active를 True로 변경(이메일 인증성공)
        self.user.is_active = True
        self.user.save()

        # 다시 로그인을 시도하면 성공으로 인한 상태 코드 200 OK를 확인합니다.
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_logout(self):
        # 로그인을 시도합니다.
        self.user.is_active = True
        self.user.save()

        url_login = reverse('login')
        login_data = {
            'email': self.user.email,
            'password': '1234',
        }
        response_login = self.client.post(url_login, login_data)

        # 로그인 성공 후 토큰을 가져옵니다.
        access_token = response_login.data['access_token']

        # 로그아웃을 시도합니다.
        url_logout = reverse('logout')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        response_logout = self.client.post(url_logout, **headers)

        # 로그아웃에 성공한 경우 상태 코드 200 OK를 확인합니다.
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('delete')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        url = reverse('update')
        data = {
            'email': 'updated@example.com',
            'password': 'newpassword',
            'name': 'Updated User',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated User')

    def test_pw_change(self):
        url = reverse('pw_change')
        data = {
            'password': '1234',
            'new_pw': 'newpassword',
            'pw_confirm': 'newpassword',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        self.user.is_active = True
        self.user.save()

        url_login = reverse('login')
        login_data = {
            'email': self.user.email,
            'password': '1234',
        }
        response_login = self.client.post(url_login, login_data)
        # 로그인 성공 후 토큰을 가져옵니다.

        url = reverse('refresh_token')
        data = {
            'refresh_token': response_login.data['refresh_token'],
        }
        response = self.client.post(url, data)

        # refresh_token을 넣었을 때 200 OK 상태 코드를 반환하는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터에 'access_token'과 'refresh_token'이 포함되어 있는지 확인합니다.
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_check_email_duplication(self):
        url = reverse('check_email_duplication')
        data = {
            'email': self.user.email,
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], '이미 사용 중인 이메일입니다.')

    def test_check_name_duplication(self):
        url = reverse('check_name_duplication')
        data = {
            'name': self.user.name,
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['message'], '이미 사용 중인 이름입니다.')