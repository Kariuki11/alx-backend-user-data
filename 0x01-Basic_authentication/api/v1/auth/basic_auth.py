#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  02 15:00:00 2024

@Author: Kenneth Kariuki
"""
import base64
from models.user import User
from typing import TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract base64 authorization header

        Args:
            authorization_header (str): Authorization header

        Returns:
            str: Base64 authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode base64 authorization header

        Args:
            base64_authorization_header (str): Base64 authorization header

        Returns:
            str: Decoded base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials

        Args:
            decoded_base64_authorization_header (str):
                Decoded base64 authorization header

        Returns:
            tuple: User credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user, password = decoded_base64_authorization_header.split(':', 1)

        return user, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        User object from credentials

        Args:
            user_email (str): User email
            user_pwd (str): User password

        Returns:
            User: User object
        """
        if user_email is None or user_pwd is None:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current user

        Args:
            request (flask.Request): Request object

        Returns:
            User: User object
        """
        if request is None:
            return None

        base64_authorization_header = self.authorization_header(request)

        if base64_authorization_header is None:
            return None

        encoded_base64 = self.extract_base64_authorization_header(
            base64_authorization_header
        )

        if encoded_base64 is None:
            return None

        decoded_base64 = self.decode_base64_authorization_header(
            encoded_base64
        )

        if decoded_base64 is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64
        )

        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)
        return user