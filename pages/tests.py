from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class PagesTests(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_home_page_loads(self):
        """تست بارگذاری صحیح صفحه اصلی"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_has_basic_content(self):
        """تست وجود محتوای اصلی صفحه"""
        response = self.client.get(self.home_url)
        self.assertContains(response, '<h1>home</h1>')
        self.assertContains(response, 'Home Page')

    def test_home_page_links_for_guest_users(self):
        """تست لینک‌های صفحه برای کاربران مهمان"""
        response = self.client.get(self.home_url)
        self.assertContains(response, 'href="/accounts/login/"')
        self.assertContains(response, 'href="/accounts/signup/"')
        self.assertNotContains(response, 'action="/accounts/logout/"')

    def test_home_page_welcome_for_logged_in_users(self):
        """تست پیام خوشآمد برای کاربران وارد شده"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.home_url)
        self.assertContains(response, 'welcome testuser')
        self.assertContains(response, 'action="/accounts/logout/"')
        self.assertNotContains(response, 'href="/accounts/login/"')