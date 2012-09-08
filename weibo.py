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
    def __init__(self, api_key, api_secret, redirect_uri):
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
        self.expires_in = None
        self.uid = None
        self.session = None

    def _get_token_by_code(self, authorization_code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            }
        response = requests.post(self.token_url, data=params)

        return json.loads(response.content)

    @property
    def authorize_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            }
        return '%s?%s' % (self.authorization_url, urllib.urlencode(params))

    @property
    def alive(self):
        if self.expires_in:
            return self.expires_in > time.time()
        else:
            return False

    def set_code(self, authorization_code):
        """
        Activate client by authorization_code.
        """
        tk = self._get_token_by_code(authorization_code)
        self.uid = tk['uid']
        self.expires_in = time.time() + int(tk['expires_in'])

        self.set_token(tk['access_token'])

    def set_token(self, access_token):
        """
        Directly activate client by access_token.
        """
        self.access_token = access_token
        self.session = requests.session(
            params={'access_token': self.access_token})

    def get(self, uri, **kwargs):
        """
        Request resource by get method.
        """
        url = "%s%s.json" % (self.api_url, uri)
        return self.session.get(url, params=kwargs).text

    def post(self, uri, **kwargs):
        """
        Request resource by post method.
        """
        url = "%s%s.json" % (self.api_url, uri)
        return self.session.post(url, data=kwargs).text
