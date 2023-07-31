from utils.util import hash_password, verify_hashed_password, AccessToken, RefreshToken
from datetime import timedelta
from unittest import TestCase


class TestUtils(TestCase):
    def test_it_hash_password(self):
        password_example = "12345"
        hashed_password = hash_password(password_example)

        assert hashed_password != password_example
        assert type(hashed_password) is str

    def test_it_verify_hashed_password(self):
        password_example = "12345"
        hashed_password = hash_password(password_example)
        verified = verify_hashed_password(password_example, hashed_password)

        assert verified is True
        assert type(verified) is bool

    def test_it_neg_verify_hashed_password(self):
        password_example = "12345"
        hashed_password = hash_password(password_example)
        verified = verify_hashed_password("123456", hashed_password)

        assert verified is False
        assert type(verified) is bool


class TestUtilsToken(TestCase):
    def test_it_create_access_token(self):
        expired_delta = timedelta(days=3)
        expired_delta_2 = timedelta(days=4)
        subject = "test"
        subject_2 = "test_2"
        assert type(AccessToken().create_token(subject, expired_delta)) is str
        assert AccessToken().create_token(
            subject, expired_delta
        ) != AccessToken().create_token(subject, expired_delta_2)
        assert AccessToken().create_token(
            subject, expired_delta
        ) != AccessToken().create_token(subject_2, expired_delta)

        assert AccessToken().create_token(
            subject, expired_delta
        ) == AccessToken().create_token(subject, expired_delta)

    def test_it_create_refresh_token(self):
        expired_delta = timedelta(days=2)
        expired_delta_2 = timedelta(days=3)
        subject = "test"
        subject_2 = "test_2"
        assert type(RefreshToken().create_token(subject, expired_delta)) is str
        assert RefreshToken().create_token(
            subject, expired_delta
        ) != RefreshToken().create_token(subject, expired_delta_2)
        assert RefreshToken().create_token(
            subject, expired_delta
        ) != RefreshToken().create_token(subject_2, expired_delta)

        assert RefreshToken().create_token(
            subject, expired_delta
        ) == RefreshToken().create_token(subject, expired_delta)
