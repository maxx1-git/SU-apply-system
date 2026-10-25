import json
from unittest import mock
from urllib.parse import parse_qs, urlparse

import requests
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

DISCORD_SETTINGS = {
    "discord": {
        "APP": {"client_id": "test-client", "secret": "test-secret", "key": ""},
        "SCOPE": ["identify"],
    }
}

DISCORD_PROFILE = {
    "id": "123456789012345678",
    "username": "tester",
    "global_name": "Test Officer",
    "avatar": "abcdef123456",
    "discriminator": "0",
}


def _json_response(payload, status=200):
    resp = requests.Response()
    resp.status_code = status
    resp._content = json.dumps(payload).encode()
    resp.headers["Content-Type"] = "application/json"
    return resp


def fake_discord_request(self, method, url, *args, **kwargs):
    if url.endswith("/oauth2/token"):
        return _json_response({"access_token": "tok", "token_type": "Bearer"})
    if url.endswith("/users/@me"):
        return _json_response(DISCORD_PROFILE)
    raise AssertionError(f"Unexpected outbound request: {method} {url}")


@override_settings(SOCIALACCOUNT_PROVIDERS=DISCORD_SETTINGS)
class DiscordLoginFlowTests(TestCase):
    def _login(self, next_url="/"):
        """Run the whole OAuth dance against a mocked Discord."""
        resp = self.client.get("/accounts/discord/login/", {"next": next_url})
        self.assertEqual(resp.status_code, 302)
        state = parse_qs(urlparse(resp["Location"]).query)["state"][0]
        with mock.patch.object(requests.Session, "request", fake_discord_request):
            return self.client.get(
                "/accounts/discord/login/callback/", {"code": "abc", "state": state}
            )

    def test_logged_out_navbar_links_to_discord(self):
        for url in ("/", "/apply/"):
            html = self.client.get(url).content.decode()
            self.assertIn("btn--discord", html)
            self.assertIn("/accounts/discord/login/", html)
            self.assertNotIn("data-user-menu-toggle", html)

    def test_login_link_redirects_straight_to_discord(self):
        resp = self.client.get("/accounts/discord/login/")
        self.assertEqual(resp.status_code, 302)
        loc = urlparse(resp["Location"])
        self.assertEqual(loc.netloc, "discord.com")
        qs = parse_qs(loc.query)
        self.assertEqual(qs["client_id"], ["test-client"])
        self.assertEqual(qs["scope"], ["identify"])

    def test_allauth_login_and_signup_pages_go_to_discord(self):
        for url in ("/accounts/login/", "/accounts/signup/"):
            resp = self.client.get(url)
            self.assertRedirects(resp, "/accounts/discord/login/", fetch_redirect_response=False)

    def test_new_user_is_registered_and_logged_in_without_signup_form(self):
        resp = self._login(next_url="/apply/")
        self.assertRedirects(resp, "/apply/", fetch_redirect_response=False)

        user = get_user_model().objects.get(socialaccount__uid=DISCORD_PROFILE["id"])
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

        # Same auth UI on both pages
        for url in ("/", "/apply/"):
            html = self.client.get(url).content.decode()
            self.assertIn("data-user-menu-toggle", html)
            self.assertIn("Test Officer", html)
            self.assertIn("cdn.discordapp.com/avatars/123456789012345678/abcdef123456", html)
            self.assertIn("/accounts/logout/", html)
            self.assertNotIn("btn--discord", html)

    def test_returning_user_does_not_create_duplicate(self):
        self._login()
        self.client.post("/accounts/logout/")
        self._login()
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_logout_returns_to_logged_out_navbar(self):
        self._login()
        resp = self.client.post("/accounts/logout/")
        self.assertRedirects(resp, "/", fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertIn("btn--discord", self.client.get("/").content.decode())
