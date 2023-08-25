from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Review, Photos
from accounts.models import User
from hjd.models import Hjd
from restaurant.models import Restaurant, Categories

class ReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='1234', name='testuser',)

        self.area = Hjd.objects.create(
            adm_nm='Test Adm_nm', sidonm='Test Sidonm', temp='Test Temp', sggnm='Test Sggnm', latitude=123.456, longitude=789.012)

        self.category = Categories.objects.create(category_name='Test Category')

        # Restaurant 객체 생성
        self.restaurant = Restaurant.objects.create(
            area_id=self.area, category_name=self.category, user=self.user,
            name='Test Restaurant', address='Test Address', contents='Test Contents',
            latitude=123.456, longitude=789.012)

    def test_review_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('review_create')
        data = {
            'rest_id': self.restaurant.rest_id,
            'user': self.user.name,
            'title': 'Test Review',
            'contents': 'Test contents',
            'rating': 4.5,
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Photos.objects.count(), 0)

    def test_review_rest(self):
        # 특정 레스토랑의 리뷰 리스트 조회 엔드포인트를 테스트합니다.
        url = reverse('review_rest', args=[self.restaurant.rest_id])
        for i in range(3):
            Review.objects.create(
                rest_id=self.restaurant, user=self.user, title=f'Review {i}', contents=f'Contents {i}', rating=0 + i)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.filter(rest_id=self.restaurant).count(), 3)

    def test_review_user(self):
        # 특정 유저의 리뷰 리스트 조회 엔드포인트를 테스트합니다.
        url = reverse('review_user', args=[self.user.name])
        for i in range(4):
            Review.objects.create(
                rest_id=self.restaurant, user=self.user, title=f'Review {i}', contents=f'Contents {i}', rating=0 + i)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.filter(user=self.user).count(), 4)

    def test_review_delete(self):
        # 리뷰 삭제 엔드포인트를 테스트합니다.
        self.client.force_authenticate(user=self.user)
        review = Review.objects.create(
            rest_id=self.restaurant, user=self.user, title='Test Review', contents='Test contents', rating=4.5)
        url = reverse('review_delete', args=[review.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
        self.assertEqual(Photos.objects.count(), 0)  # 리뷰와 연관된 사진도 함께 삭제되어야 합니다.

    def test_get_avg_rating_rest(self):
        # 특정 레스토랑의 평균 평점 조회 엔드포인트를 테스트합니다.
        url = reverse('get_avg_rating_rest', args=[self.restaurant.rest_id])

        # 5개의 리뷰를 생성하고 평점을 다양하게 설정합니다.
        for i in range(5):
            Review.objects.create(
                rest_id=self.restaurant, user=self.user, title=f'Review {i}', contents=f'Contents {i}', rating=0 + i)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.json()['average_rating'], 2.0, places=2)  # 생성된 리뷰의 평균 평점은 3.5입니다.

    def test_get_avg_rating_user(self):
        # 특정 유저의 평균 평점 조회 엔드포인트를 테스트합니다.
        url = reverse('get_avg_rating_user', args=[self.user.name])

        # 5개의 리뷰를 생성하고 평점을 다양하게 설정합니다.
        for i in range(5):
            Review.objects.create(
                rest_id=self.restaurant, user=self.user, title=f'Review {i}', contents=f'Contents {i}', rating=0 + i)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.json()['average_rating'], 2.0, places=2)  # 생성된 리뷰의 평균 평점은 5.0입니다.