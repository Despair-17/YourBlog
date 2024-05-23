from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from captcha.models import CaptchaStore


class MainAppTest(TestCase):
    fixtures = ['test_data.json']

    def test_home_page_view(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, 'Главная страница')
        self.assertContains(response, 'Контент главной страницы')
        self.assertIn('main', response.context)

    def test_about_page_view(self):
        path = reverse('about')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'О сайте')
        self.assertContains(response, 'Контент страницы о сайте')
        self.assertIn('about', response.context)

    def test_faq_page_view(self):
        path = reverse('faq')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'main/faq.html')
        self.assertContains(response, 'FAQs')
        self.assertContains(response, 'Контент FAQs страницы')
        self.assertIn('faq', response.context)

    def test_contact_get_view(self):
        path = reverse('contact')
        response = self.client.get(path)

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
        path = reverse('contact')

        captcha_key = CaptchaStore.generate_key()
        captcha_value = CaptchaStore.objects.get(hashkey=captcha_key).response
        form_data = {
            'name': 'TestUser',
            'email': 'test@test.test',
            'message': 'Test message, Test message, Test message, Test message, Test message, Test message, ',
            'captcha_0': captcha_key,
            'captcha_1': captcha_value,
        }

        response = self.client.post(path, data=form_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_contact_form_invalid(self):
        path = reverse('contact')

        captcha_key = CaptchaStore.generate_key()

        form_data = {
            'name': '',
            'email': 'invalid-email',
            'message': 'Test message, ',
            'captcha_0': captcha_key,
            'captcha_1': '1234',
        }

        response = self.client.post(path, data=form_data)
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

        response = self.client.post(path, data=form_data)

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

    def test_health_view(self):
        path = reverse('health')
        response = self.client.get(path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, {'status': 'OK'})
