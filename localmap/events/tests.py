from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from events.models import Events
from restaurant.models import Restaurant, Categories
from hjd.models import Hjd
import uuid


class EventsAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # 테스트 유저와 관리자 생성
        self.test_user = User.objects.create_user(
            name='testuser',
            email='user@test.com',
            password='testpassword')
        self.test_admin = User.objects.create_superuser(
            name='testadmin',
            email='admin@test.com',
            password='testpassword')

        # JWT 토큰 생성
        self.test_user_token = str(AccessToken.for_user(self.test_user))
        self.test_admin_token = str(AccessToken.for_user(self.test_admin))

        # JWT 토큰에 기반한 헤더 생성
        self.user_header = {"HTTP_AUTHORIZATION": f"Bearer {self.test_user_token}"}
        self.admin_header = {"HTTP_AUTHORIZATION": f"Bearer {self.test_admin_token}"}

        self.sample_categories = Categories.objects.create(
            category_name="한식"  # 카테고리에 맞는 값을 적어주세요.
        )

        self.sample_hjd = Hjd.objects.create(
            adm_nm="서울특별시 강남구 역삼1동",  # 예: 유니크한 행정동 이름
            sidonm="서울특별시",  # 예: 시/도 이름
            temp="강남구",  # 예: 시/군/구 이름
            sggnm="역삼1동",  # 예: 읍/면/동 이름
            latitude=37.498085,  # 예: 위도
            longitude=127.027840  # 예: 경도
            # 추가로 필요한 필드가 있다면 채우실 수 있습니다.
        )

        self.sample_restaurant = Restaurant.objects.create(
            area_id=self.sample_hjd,   # area_id 값 설정 (이 부분은 Hjd 모델에 따라 조절해야 함)
            category_name=self.sample_categories,  # category_name 값 설정 (이 부분은 Categories 모델에 따라 조절해야 함)
            user=self.test_user,  # Restaurant에 user 할당 (test_user 사용)
            name="샘플 레스토랑",
            address="서울특별시 강남구 어딘가",  # Restaurant의 주소 설정
            contents="레스토랑 설명",
            latitude=37.498085,  # 위도 설정
            longitude=127.027840  # 경도 설정
        )

        # 이벤트 생성을 위한 정보
        self.event_data = {
            "event_no": uuid.uuid4(),
            'rest_id': 'some_restaurant_id',
            'name': '샘플 이벤트',
            'amount': 100,
            'content': '샘플 이벤트 설명',
            'url': 'https://example.com/sample_image.png',
        }

        self.event = Events.objects.create(
            event_no=self.event_data["event_no"],
            rest_id=self.sample_restaurant,
            name=self.event_data["name"],
            amount=self.event_data["amount"],
            content=self.event_data["content"],
            url=self.event_data["url"],
        )

    def create_event(self, headers=None):
        if headers:
            response = self.client.post(reverse('event_create'), self.event_data, **headers)
        else:
            response = self.client.post(reverse('event_create'), self.event_data)
        return response

    def test_event_create_as_admin(self):
        response = self.create_event(headers=self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Events.objects.filter(name=self.event_data['name']).exists())

    def test_event_create_as_user(self):
        response = self.create_event(headers=self.user_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_create_unauthenticated(self):
        response = self.create_event()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_list(self):
        self.create_event(headers=self.admin_header)

        # GET API 호출
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data), 1)

    def test_event_detail(self):
        self.create_event(headers=self.admin_header)
        response = self.client.get(reverse('event_detail', args=[self.event.event_no]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.event_data['name'])

    def test_event_update_as_admin(self):
        self.create_event(headers=self.admin_header)

        update_data = {'name': '새로운 이벤트'}
        response = self.client.put(reverse('event_update', args=[self.event.event_no]), update_data, **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_event_update_as_user(self):
        self.create_event(headers=self.admin_header)

        update_data = {'name': '새로운 이벤트'}
        response = self.client.put(reverse('event_update', args=[self.event.event_no]), update_data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_update_unauthenticated(self):
        self.create_event(headers=self.admin_header)
        update_data = {'name': '새로운 이벤트'}
        response = self.client.put(reverse('event_update', args=[self.event.event_no]), update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_delete_as_admin(self):
        self.create_event(headers=self.admin_header)
        response = self.client.delete(reverse('event_delete', args=[self.event.event_no]), **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Events.objects.filter(name=self.event_data['name']).exists())

    def test_event_delete_as_user(self):
        self.create_event(headers=self.admin_header)
        response = self.client.delete(reverse('event_delete', args=[self.event.event_no]), **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Events.objects.filter(name=self.event_data['name']).exists())

    def test_event_delete_unauthenticated(self):
        self.create_event(headers=self.admin_header)
        response = self.client.delete(reverse('event_delete', args=[self.event.event_no]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Events.objects.filter(name=self.event_data['name']).exists())

