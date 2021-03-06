from django.test import TestCase
import accounts.views
from unittest.mock import patch, call
from accounts.models import Token

class SendLoginEmailViewTestCase(TestCase):
    
    def post_send_login_email(self, follow=False):
        return self.client.post('/accounts/send_login_email', data={
           'email': 'edith@example.com'
        }, follow=True)

   
    def test_redirects_to_home_page(self):
        response = self.post_send_login_email()
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.post_send_login_email()

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlist')
        self.assertEqual(to_list, ['edith@example.com']) 

    def test_adds_success_message(self):
        response = self.post_send_login_email(follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, 'success')

    def test_creates_token_token_associated_with_email(self):
        self.post_send_login_email()
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.post_send_login_email()

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_rediercts_to_home_page(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')


    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)

  

class LogoutiewTest(TestCase):

    def test_rediercts_to_home_page(self):
        token = Token.objects.create(email='edith@example.com')
        self.client.get(f'/accounts/login?token={token.uid}', follow=True)
        response = self.client.get(f'/accounts/login', follow=True)
        self.assertRedirects(response, '/')

    def test_does_not_displa_email_when_logout(self):
        token = Token.objects.create(email='edith@example.com')
        response = self.client.get(f'/accounts/login?token={token.uid}', follow=True)
        self.assertContains(response, 'edith@example.com')
        response = self.client.get(f'/accounts/logout', follow=True)
        self.assertNotContains(response, 'edith@example.com')

    @patch('accounts.views.auth.logout')
    def test_call_logout(self, mock_logout):
        token = Token.objects.create(email='edith@example.com')
        self.client.get(f'/accounts/login?token={token.uid}')
        response = self.client.get(f'/accounts/logout')
        self.assertEqual(
            mock_logout.call_args,
            call(response.wsgi_request)
        )
        
    @patch('accounts.views.auth')
    def test_does_not_logout_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)
        response = self.client.get(f'/accounts/logout', follow=True)
        self.assertEqual(mock_auth.logout.called, False)
