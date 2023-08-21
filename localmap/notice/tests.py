# tests.py 또는 다른 테스트 모듈에 다음 코드를 추가합니다
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from notice.models import Notice
from notice.serializers import NoticeSerializer
from accounts.models import User
class NoticeListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 테스트 공지사항 생성
        self.user = User.objects.create_user(email='test@example.com', name='testuser')
        Notice.objects.create(title='Test Notice 1', content='Test content 1', user=self.user)
        Notice.objects.create(title='Test Notice 2', content='Test content 2', user=self.user)

    def test_notice_list(self):
        url = reverse('notice_list')
        response = self.client.get(url)

        # 응답 코드가 200인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 데이터베이스에서 공지사항을 불러오고 직렬화합니다.
        notice_list = Notice.objects.all()
        serializer = NoticeSerializer(notice_list, many=True)

        # 응답 데이터가 실제 데이터와 일치하는지 확인합니다.
        self.assertEqual(response.data, serializer.data)
