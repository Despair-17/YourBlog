from http import HTTPStatus

from captcha.models import CaptchaStore

from django.test import TestCase
from django.urls import reverse

from .models import About, FAQ, Main


class TestHomePageView(TestCase):

    def setUp(self):
        self.main = Main.objects.create(
            title='Test main title',
            content='Test main content',
        )
        self.path = reverse('home')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/index.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertIn('main', response.context)
        self.assertContains(response, self.main.title)
        self.assertContains(response, self.main.content)


class TestAboutPageView(TestCase):

    def setUp(self):
        self.about = About.objects.create(
            title='Test about title',
            content='Test about content',
        )
        self.path = reverse('about')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/about.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertIn('about', response.context)
        self.assertContains(response, self.about.title)
        self.assertContains(response, self.about.content)


class TestFAQPageView(TestCase):

    def setUp(self):
        self.faq = FAQ.objects.create(
            title='Test faq title',
            content='Test faq content',
        )
        self.path = reverse('faq')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/faq.html')

    def test_view_context(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertIn('faq', response.context)
        self.assertContains(response, self.faq.title)
        self.assertContains(response, self.faq.content)


class TestContactView(TestCase):

    def setUp(self):
        self.path = reverse('contact')

    def test_view_render_correct_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/contact.html')
        self.assertContains(response, 'Обратная связь')

        content = response.content.decode()
        self.assertIn('<form method="POST">', content)
        self.assertIn('<input type="text" name="name"', content)
        self.assertIn('<input type="email" name="email"', content)
        self.assertIn('<textarea name="message"', content)
        self.assertIn('<input type="text" name="captcha_1"', content)
        self.assertIn('<button type="submit"', content)

    def test_contact_form_valid(self):
        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        form_data = {
            'name': 'TestUser',
            'email': 'test@test.test',
            'message': 'Test message, Test message, Test message, Test message, Test message, Test message, ',
            'captcha_0': captcha_key,
            'captcha_1': captcha_value,
        }

        response = self.client.post(self.path, data=form_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_contact_form_invalid(self):
        captcha_key = CaptchaStore.generate_key()

        form_data = {
            'name': '',
            'email': 'invalid-email',
            'message': 'Test message, ',
            'captcha_0': captcha_key,
            'captcha_1': '1234',
        }

        response = self.client.post(self.path, data=form_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response, 'form',
            'name',
            'Это поле обязательно для заполнения.',
        )
        self.assertFormError(
            response, 'form',
            'email',
            'Введите правильный адрес электронной почты.',
        )
        self.assertFormError(
            response, 'form',
            'message',
            'Убедитесь, что это значение содержит не менее 50 символов (сейчас 13).',
        )
        self.assertFormError(
            response, 'form',
            'captcha',
            'Неверный ответ',
        )

        form_data = {
            'name': 'fds',
            'email': '',
            'message': '',
            'captcha_0': captcha_key,
            'captcha_1': '',
        }

        response = self.client.post(self.path, data=form_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response, 'form',
            'name',
            'Убедитесь, что это значение содержит не менее 4 символов (сейчас 3).',
        )
        self.assertFormError(
            response, 'form',
            'email',
            'Это поле обязательно для заполнения.',
        )
        self.assertFormError(
            response, 'form',
            'message',
            'Это поле обязательно для заполнения.',
        )
        self.assertFormError(
            response, 'form',
            'captcha',
            'Это поле обязательно для заполнения.',
        )


class TestMainApp(TestCase):

    def test_health_view(self):
        path = reverse('health')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, {'status': 'OK'})
