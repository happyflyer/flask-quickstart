# -*- coding: utf-8 -*-

from flask import jsonify, g, request, current_app

from .. import db
from . import bp, basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """获取token
    @@@
    #### args
    > 参考：[HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)\n
    > 在 request 请求头中携带 `Authorization` 字段。\n
    ```properties
    Authorization: Basic <auth>
    ```
    #### return
    ```json
    {
        "token": "e4YEcn05B4lbWYqrAqLUTf9KWPlHHdb2"
    }
    ```
    @@@
    """
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """失效token
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    ```properties
    Authorization: Bearer <token>
    ```
    #### return
    ```json
    {"message": "ok"}
    ```
    @@@
    """
    g.current_user.revoke_token()
    db.session.commit()
    return jsonify({'message': 'ok'})


@bp.route('/test_request', methods=['GET', 'POST'])
def test_request():
    """测试请求
    @@@
    #### return
    ```json
    {"message": "success in test_request"}
    ```
    @@@
    """
    return jsonify({'message': 'success in test_request'})


@bp.route('/test_with_auth', methods=['GET', 'POST'])
@basic_auth.login_required
def test_with_auth():
    """测试Basic认证请求
    @@@
    #### args
    > 参考：[HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)\n
    > 在 request 请求头中携带 `Authorization` 字段。\n
    ```properties
    Authorization: Basic <auth>
    ```
    #### return
    ```json
    {"message": "success in test_with_auth"}
    ```
    @@@
    """
    return jsonify({'message': 'success in test_with_auth'})


@bp.route('/test_with_token', methods=['GET', 'POST'])
@token_auth.login_required
def test_with_token():
    """测试Token认证请求
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    ```properties
    Authorization: Bearer <token>
    ```
    #### return
    ```json
    {"message": "success in test_with_token"}
    ```
    @@@
    """
    return jsonify({'message': 'success in test_with_token'})
