from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Menu
from restaurant.models import Restaurant, Hjd, Categories
from accounts.models import User

class MenuAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            email='test@example.com', password='1234', name='testuser',)

        self.area = Hjd.objects.create(
            adm_nm='Test Adm_nm', sidonm='Test Sidonm', temp='Test Temp', sggnm='Test Sggnm', latitude=123.456, longitude=789.012)

        self.category = Categories.objects.create(category_name='Test Category')

        # Restaurant 객체 생성
        self.restaurant = Restaurant.objects.create(
            area_id=self.area, category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address', contents='Test Contents',
            latitude=123.456, longitude=789.012)

    def test_menu_create(self):
        url = reverse('menu_create')
        data = {
            'rest_id': self.restaurant.rest_id,
            'name': 'Test Menu',
            'price': 1000
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_menu_list(self):
        url = reverse('menu_list', args=[self.restaurant.rest_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu_detail(self):
        menu = Menu.objects.create(
            rest_id=self.restaurant, name='Test Menu', price=1000)
        url = reverse('menu_detail', args=[menu.menu_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu_update(self):
        menu = Menu.objects.create(
            rest_id=self.restaurant, name='Test Menu', price=1000)
        url = reverse('menu_update', args=[menu.menu_id])
        data = {
            'rest_id': self.restaurant.rest_id,
            'name': 'Updated Test Menu',
            'price': 1500
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu_delete(self):
        menu = Menu.objects.create(
            rest_id=self.restaurant, name='Test Menu', price=1000)
        url = reverse('menu_delete', args=[menu.menu_id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)