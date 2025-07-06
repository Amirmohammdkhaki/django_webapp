from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class HomePageTests(TestCase):
    def setUp(self):
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_home_page_status_code(self):
        """بررسی بارگذاری صحیح صفحه اصلی"""
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_template(self):
        """بررسی استفاده از تمپلیت صحیح"""
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_page_content(self):
        """بررسی محتوای صفحه اصلی"""
        self.assertContains(self.response, '<h1>home</h1>')
        self.assertContains(self.response, 'Home Page')

    def test_home_page_links(self):
        """بررسی وجود لینک‌های ورود و ثبت‌نام"""
        self.assertContains(self.response, f'href="{reverse("login")}"')
        self.assertContains(self.response, f'href="{reverse("signup")}"')

    def test_home_page_for_authenticated_users(self):
        """بررسی نمایش پیام خوشآمد برای کاربران لاگین کرده"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'welcome {user.username}')


class CustomUserModelTests(TestCase):
    def test_create_user(self):
        """تست ایجاد کاربر جدید"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            age=25
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.age, 25)

    def test_create_superuser(self):
        """تست ایجاد سوپر یوزر"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


class SignupPageTests(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_signup_page_status_code(self):
        """بررسی بارگذاری صفحه ثبت‌نام"""
        self.assertEqual(self.response.status_code, 200)

    def test_signup_form(self):
        """تست فرم ثبت‌نام"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'age': 30,
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'newuser')


class AuthTests(TestCase):
    def test_login_functionality(self):
        """تست عملکرد ورود به سیستم"""
        user = User.objects.create_user(
            username='testlogin',
            password='testpass123'
        )
        response = self.client.post(reverse('login'), {
            'username': 'testlogin',
            'password': 'testpass123'
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_logout_functionality(self):
        """تست عملکرد خروج از سیستم"""
        user = User.objects.create_user(
            username='testlogout',
            password='testpass123'
        )
        self.client.login(username='testlogout', password='testpass123')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Login')  # بررسی نمایش دکمه لاگین پس از خروج

    def test_invalid_login(self):
        """تست ورود با اطلاعات نادرست"""
        User.objects.create_user(
            username='validuser',
            password='validpass123'
        )
        response = self.client.post(reverse('login'), {
            'username': 'validuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')