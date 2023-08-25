from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Categories
from registration.models import Registration
from accounts.models import User

class RegistrationAPITestCase(APITestCase):

    def setUp(self):
        # 사용할 테스트용 유저와 카테고리를 생성합니다.
        self.user = User.objects.create_user(
            email='test@example.com', password='1234', name='testuser')
        self.category = Categories.objects.create(category_name='Test Category')

    def test_reg_create(self):
        # 등록 API의 URL을 생성합니다.
        url = reverse('reg_create')
        # 등록할 레스토랑 정보를 데이터로 준비합니다.
        data = {
            'name': 'Test Restaurant',
            'address': 'Test Address',
            'latitude': 37.123456,
            'longitude': 126.654321,
            'category_name': self.category.category_name,
        }
        # 로그인한 사용자로 인증 설정합니다.
        self.client.force_authenticate(user=self.user)
        # POST 요청을 보내어 레스토랑 등록을 시도합니다.
        response = self.client.post(url, data)
        # 응답 상태 코드가 201 Created 여야 합니다.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 등록된 레스토랑 객체를 가져옵니다.
        registration = Registration.objects.get(name='Test Restaurant')
        # 등록된 레스토랑의 소유자는 위에서 생성한 유저여야 합니다.
        self.assertEqual(registration.user, self.user)

    def test_reg_list(self):
        # 레스토랑 목록 조회 API의 URL을 생성합니다.
        url = reverse('reg_list')
        # GET 요청을 보내어 레스토랑 목록을 조회합니다.
        response = self.client.get(url)
        # 응답 상태 코드가 200 OK 여야 합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reg_detail(self):
        # 테스트용 레스토랑 객체를 생성합니다.
        registration = Registration.objects.create(
            category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address',
            latitude=37.123456, longitude=126.654321
        )
        # 상세 조회 API의 URL을 생성합니다.
        url = reverse('reg_detail', args=[registration.regist_id])
        # GET 요청을 보내어 특정 레스토랑의 상세 정보를 조회합니다.
        response = self.client.get(url)
        # 응답 상태 코드가 200 OK 여야 합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reg_update(self):
        # 테스트용 레스토랑 객체를 생성합니다.
        registration = Registration.objects.create(
            category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address',
            latitude=37.123456, longitude=126.654321
        )
        # 업데이트 API의 URL을 생성합니다.
        url = reverse('reg_update', args=[registration.regist_id])
        # 수정할 레스토랑 정보를 데이터로 준비합니다.
        data = {
            'name': 'Updated Restaurant',
            'address': 'Updated Address',
            'latitude': 37.654321,
            'longitude': 126.123456,
            'category_name': self.category.category_name,
        }
        # 로그인한 사용자로 인증 설정합니다.
        self.client.force_authenticate(user=self.user)
        # PUT 요청을 보내어 레스토랑 정보를 수정합니다.
        response = self.client.put(url, data)
        # 응답 상태 코드가 200 OK 여야 합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 수정된 레스토랑 정보를 확인합니다.
        updated_registration = Registration.objects.get(pk=registration.pk)
        self.assertEqual(updated_registration.name, 'Updated Restaurant')
        self.assertEqual(updated_registration.address, 'Updated Address')
        self.assertEqual(updated_registration.latitude, 37.654321)
        self.assertEqual(updated_registration.longitude, 126.123456)

    def test_reg_delete(self):
        # 테스트용 레스토랑 객체를 생성합니다.
        registration = Registration.objects.create(
            category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address',
            latitude=37.123456, longitude=126.654321
        )
        # 삭제 API의 URL을 생성합니다.
        url = reverse('reg_delete', args=[registration.regist_id])
        # 로그인한 사용자로 인증 설정합니다.
        self.client.force_authenticate(user=self.user)
        # DELETE 요청을 보내어 레스토랑 정보를 삭제합니다.
        response = self.client.delete(url)
        # 응답 상태 코드가 200 OK 여야 합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 삭제 후 해당 객체가 더 이상 존재하지 않아야 합니다.
        with self.assertRaises(Registration.DoesNotExist):
            Registration.objects.get(pk=registration.pk)