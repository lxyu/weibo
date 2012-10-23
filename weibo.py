# -*- coding: utf-8 -*-

"""
Python sina weibo sdk.

Rely on `requests` to do the dirty work, so it's much simpler and cleaner
than the official SDK.

For more info, refer to:
http://lxyu.github.com/weibo/
"""

import json
import time
import urllib

import requests


class Client(object):
    def __init__(self, api_key, api_secret, redirect_uri,
                 access_token=None, expires_at=None):
        # const define
        self.site = 'https://api.weibo.com/'
        self.authorization_url = self.site + 'oauth2/authorize'
        self.token_url = self.site + 'oauth2/access_token'
        self.api_url = self.site + '2/'

        # init basic info
        self.client_id = api_key
        self.client_secret = api_secret
        self.redirect_uri = redirect_uri

        self.access_token = None
        self.expires_at = None
        self.session = None

        # activate client directly if given acccess_token and expires_at
        if access_token and expires_at:
            self.set_token(access_token, expires_at)

    @property
    def authorize_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        return '%s?%s' % (self.authorization_url, urllib.urlencode(params))

    @property
    def token_info(self):
        """
        This token_info can be stored to directly activate client at next time.
        """
        return {
            'access_token': self.access_token,
            'expires_at': self.expires_at
        }

    @property
    def alive(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return False

    def set_code(self, authorization_code):
        """
        Activate client by authorization_code.
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(self.token_url, data=params)
        tk = json.loads(response.content)

        self._assert_error(tk)
        self.set_token(tk['access_token'], time.time() + int(tk['expires_in']))

    def set_token(self, access_token, expires_at):
        """
        Directly activate client by access_token.
        """
        self.access_token = access_token
        self.expires_at = expires_at
        self.session = requests.session(
            params={'access_token': self.access_token})

    def _assert_error(self, d):
        if 'error_code' in d and 'error' in d:
            raise RuntimeError("[%s] %s, %s" % (
                d['error_code'], d['error'], d['error_description']))

    def get(self, uri, **kwargs):
        """
        Request resource by get method.
        """
        url = "%s%s.json" % (self.api_url, uri)
        res = json.loads(self.session.get(url, params=kwargs).text)
        self._assert_error(res)
        return res

    def post(self, uri, **kwargs):
        """
        Request resource by post method.
        """
        url = "%s%s.json" % (self.api_url, uri)
        res = json.loads(self.session.post(url, data=kwargs).text)
        self._assert_error(res)
        return res
