from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestLoginUserView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

        self.user_data = {
            'username': 'user1',
            'password': 'password',
        }

        self.user1 = self.user_model.objects.create_user(**self.user_data)

        self.path = reverse('users:login')

    def test_view_render_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_view_login_user_valid(self):
        response = self.client.post(self.path, data=self.user_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/')
        self.assertEquals(self.user1.pk, int(self.client.session['_auth_user_id']))

    def test_view_login_user_invalid(self):
        login_data = {
            'username': 'user1',
            'password': 'invalid',
        }

        response = self.client.post(self.path, data=login_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)


class RegisterUserView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user_data_valid = {
            'username': 'user1',
            'email': 'test@test.test',
            'password1': '$password123A',
            'password2': '$password123A'
        }
        self.user_data_invalid1 = {
            'username': 'user1',
            'email': 'invalid',
            'password1': 'invalid1',
            'password2': 'invalid2'
        }
        self.user_data_invalid2 = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }

        self.path = reverse('users:register')
        self.path_register_done = reverse('users:register_done')

    def test_view_render_template(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_view_register_user_valid(self):
        response = self.client.post(self.path, data=self.user_data_valid)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:register_done'))

    def test_view_register_user_invalid(self):
        response = self.client.post(self.path, data=self.user_data_invalid1)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            'form',
            'email',
            'Введите правильный адрес электронной почты.'
        )
        self.assertFormError(
            response,
            'form',
            'password2',
            'Введенные пароли не совпадают.'
        )

        response = self.client.post(self.path, data=self.user_data_invalid2)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            'form',
            'username',
            'Это поле обязательно для заполнения.'
        )
        self.assertFormError(
            response,
            'form',
            'email',
            'Это поле обязательно для заполнения.'
        )
        self.assertFormError(
            response,
            'form',
            'password1',
            'Это поле обязательно для заполнения.'
        )
        self.assertFormError(
            response,
            'form',
            'password2',
            'Это поле обязательно для заполнения.'
        )


class ProfileUserView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user_data = {
            'username': 'user1',
            'password': 'password',
            'email': 'test@test.test',
            'first_name': 'first_name',
            'last_name': 'second_name',
        }
        self.user_data2 = {
            'username': 'user2',
            'password': 'password',
            'email': 'test2@test.test',
            'first_name': 'first_name',
            'last_name': 'second_name',
        }
        self.user1 = self.user_model.objects.create_user(**self.user_data)
        self.user2 = self.user_model.objects.create_user(**self.user_data2)

        self.path = reverse('users:profile')

    def test_view_render_template_login_user(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_view_render_template_anonymous(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        path_redirect = f'{reverse("users:login")}?next={self.path}'
        self.assertRedirects(response, path_redirect)

    def test_view_form_valid(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        from_data = {
            'email': 'test@test.test',
        }

        response = self.client.post(self.path, data=from_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

        from_data = {
            'email': 'test0@test.test',
            'date_birth': '2010-10-10',
            'first_name': 'first_name_new',
            'last_name': 'second_name_new',
        }

        response = self.client.post(self.path, data=from_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

    def test_view_form_invalid(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        from_data = {
            'email': 'test2@test.test',
        }

        response = self.client.post(self.path, data=from_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            'form',
            'email',
            'Email уже занят.'
        )

        from_data = {
            'email': '',
        }

        response = self.client.post(self.path, data=from_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            'form',
            'email',
            'Это поле обязательно для заполнения.'
        )


class PasswordChangeUserView(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

        self.user_data = {
            'username': 'user1',
            'password': 'password',
            'email': 'test@test.test',
            'first_name': 'first_name',
            'last_name': 'second_name',
        }

        self.user1 = self.user_model.objects.create_user(**self.user_data)

        self.path = reverse('users:password_change')

    def test_view_render_template_login_user(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_change.html')

    def test_view_render_template_anonymous(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        path_redirect = f'{reverse("users:login")}?next={self.path}'
        self.assertRedirects(response, path_redirect)

    def test_view_form_valid(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        form_data = {
            'old_password': 'password',
            'new_password1': 'c03%49mn5yn23#',
            'new_password2': 'c03%49mn5yn23#',
        }

        response = self.client.post(self.path, data=form_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:password_change_done"))

    def test_view_form_invalid(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        form_data = {
            'old_password': 'invalid_password',
            'new_password1': 'password',
            'new_password2': 'invalid_password',
        }

        response = self.client.post(self.path, data=form_data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response,
            'form',
            'old_password',
            'Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.'
        )
        self.assertFormError(
            response,
            'form',
            'new_password2',
            'Введенные пароли не совпадают.'
        )
