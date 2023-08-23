from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Restaurant, Categories, Hjd

class RestaurantAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email='test@example.com', password='1234', name='testuser')
        self.area = Hjd.objects.create(adm_nm='Test Adm_nm', sidonm='Test Sidonm', temp='Test Temp', sggnm='Test Sggnm', latitude=123.456, longitude=789.012)
        self.category = Categories.objects.create(category_name='Test Category')

    def test_create_restaurant(self):
        url = reverse('rest_create')
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.pk,
            'area_id': self.area.pk,
            'category_name': self.category.category_name,
            'name': 'New Restaurant',
            'address': 'New Address',
            'contents': 'New Contents',
            'latitude': 37.123,
            'longitude': 126.456,
            'introduce': 'New Introduce'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_list_restaurants(self):
        Restaurant.objects.create(
            user=self.user,
            area_id=self.area,
            category_name=self.category,
            name='Restaurant 1',
            address='Address 1',
            contents='Contents 1',
            latitude=38.123,
            longitude=125.456,
            introduce='Introduce 1'
        )
        Restaurant.objects.create(
            user=self.user,
            area_id=self.area,
            category_name=self.category,
            name='Restaurant 2',
            address='Address 2',
            contents='Contents 2',
            latitude=39.123,
            longitude=124.456,
            introduce='Introduce 2'
        )
        url = reverse('rest_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_restaurant(self):
        restaurant = Restaurant.objects.create(
            user=self.user,
            area_id=self.area,
            category_name=self.category,
            name='Test Restaurant',
            address='Test Address',
            contents='Test Contents',
            latitude=123.456,
            longitude=789.012,
            introduce='Test Introduce',
            view=0 # 임의의 초기 조회수 값
        )
        url = reverse('rest_detail', args=[restaurant.rest_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Restaurant')
        # 조회수 증가 확인
        updated_restaurant = Restaurant.objects.get(pk=restaurant.rest_id)
        self.assertEqual(updated_restaurant.view, 1) # 조회수가 1 증가한 값으로 비교

    def test_update_restaurant(self):
        restaurant = Restaurant.objects.create(
            user=self.user,
            area_id=self.area,
            category_name=self.category,
            name='Test Restaurant',
            address='Test Address',
            contents='Test Contents',
            latitude=123.456,
            longitude=789.012,
            introduce='Test Introduce'
        )
        url = reverse('rest_update', args=[restaurant.rest_id])
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.pk,
            'area_id': self.area.pk,
            'category_name': self.category.category_name,
            'name': 'Updated Restaurant',
            'address': 'Updated Address',
            'contents': 'Updated Contents',
            'latitude': 35.678,
            'longitude': 128.901,
            'introduce': 'Updated Introduce'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        restaurant.refresh_from_db()
        self.assertEqual(restaurant.name, 'Updated Restaurant')

    def test_delete_restaurant(self):
        restaurant = Restaurant.objects.create(
            user=self.user,
            area_id=self.area,
            category_name=self.category,
            name='Test Restaurant',
            address='Test Address',
            contents='Test Contents',
            latitude=123.456,
            longitude=789.012,
            introduce='Test Introduce'
        )
        url = reverse('rest_delete', args=[restaurant.rest_id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 0)