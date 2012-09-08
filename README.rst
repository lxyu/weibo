Weibo
=====

新浪微博 python SDK.

使用 `requests` 进行相关网络操作，因而相对于官方的 sdk，极大的简化了代码，并提高了可读性。


包依赖
------

- `requests <http://docs.python-requests.org>`_


安装
----

推荐使用 `pip` 安装。

::

    $ pip install weibo


使用说明
--------
准备工作
~~~~~~~~

- 首先，注册一个新浪开发者帐号，并在 `新浪开发平台 <http://open.weibo.com/apps>`_ 新建一个 app.

- 创建好应用之后在 '应用信息 -> '基本信息' 里面获取 `App Key` 和 `App Secret`.

- 在 '应用信息 -> '高级信息' 里面设置好 '授权回调页'.

示例
~~~~

下面分别用 `API_KEY`, `API_SECRET`, `REDIRECT_URI` 代表准备工作里面的三个参数。

::

    >>> from weibo import Client
    >>> c = Client(API_KEY, API_SECRET, REDIRECT_URI)
    >>> c.authorize_url
    'https://api.weibo.com/oauth2/authorize?redirect_uri=http%3A%2F%2F127.0.0.1%2Fcallback&client_id=123456'

复制链接到浏览器打开，获取 code.

::

    >>> c.set_code('abcdefghijklmn')


至此 client 初始化完成。 参考 `微博开发文档 <http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3_V2>`_ 进行接口调用。

::

    >>> c.get('users/show', uid=1282440983)
    >>> c.post('statuses/update', status='python sdk test, check out http://lxyu.github.com/weibo/')
