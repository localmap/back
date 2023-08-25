from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from hjd.models import Hjd
from restaurant.models import Categories, Restaurant

class BkAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='1234', name='testuser',)
        self.area = Hjd.objects.create(adm_nm='Test Adm_nm', sidonm='Test Sidonm', temp='Test Temp', sggnm='Test Sggnm',
                                       latitude=123.456, longitude=789.012)
        self.category = Categories.objects.create(category_name='Test Category')
        self.restaurant = Restaurant.objects.create(
            area_id=self.area, category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address', contents='Test Contents',
            latitude=123.456, longitude=789.012)


    def test_bk_toggle(self):
        rest_id = str(self.restaurant.rest_id)
        self.client.force_authenticate(user=self.user)

        toggle_value = True
        response = self.client.post(reverse('bk_toggle'), {'rest_id': rest_id, 'toggle_value': toggle_value})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['rest_id'], rest_id)

        toggle_value = False
        response = self.client.post(reverse('bk_toggle'), {'rest_id': rest_id, 'toggle_value': toggle_value})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(rest_id, response.data['rest_id'])

    def test_bk_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('bk_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_bk_count(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('bk_count'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bk_count'], 0)

        # 유저가 해당 레스트랑 북마크 추가후 count 증가하는지 확인
        response = self.client.post(reverse('bk_toggle'), {'rest_id': str(self.restaurant.rest_id), 'toggle_value': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('bk_count'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bk_count'], 1)


    def test_rest_bk_count(self):
        rest_id = str(self.restaurant.rest_id)
        response = self.client.get(reverse('rest_bk_count'), {'rest_id': rest_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bk_count'], 0)

        #유저가 해당 레스트랑 북마크 추가후 count 증가하는지 확인
        self.client.force_authenticate(user=self.user)
        bk_true = self.client.post(reverse('bk_toggle'), {'rest_id': rest_id, 'toggle_value': True})
        self.assertEqual(bk_true.status_code, status.HTTP_200_OK)

        bkt_count = self.client.get(reverse('rest_bk_count'), {'rest_id': rest_id})
        self.assertEqual(bkt_count.status_code, status.HTTP_200_OK)
        self.assertEqual(bkt_count.data['bk_count'], 1)