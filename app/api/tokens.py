# -*- coding: utf-8 -*-

from flask import jsonify, g, request, current_app

from .. import db
from . import bp, basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """获取token
    @@@
    #### 请求头
    > 参考：[HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)\n
    > 携带 `Authorization` 字段。\n
    ```properties
    Authorization: Basic <auth>
    ```
    #### 响应示例
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
    #### 请求头
    > 携带 `Authorization` 字段。\n
    ```properties
    Authorization: Bearer <token>
    ```
    #### 响应示例
    ```json
    {
        "message": "ok"
    }
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
    #### 响应示例
    ```json
    {
        "message": "success in test_request"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success in test_request'})


@bp.route('/test_with_auth', methods=['GET', 'POST'])
@basic_auth.login_required
def test_with_auth():
    """测试Basic认证请求
    @@@
    #### 请求头
    > 参考：[HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)\n
    > 携带 `Authorization` 字段。\n
    ```properties
    Authorization: Basic <auth>
    ```
    #### 响应示例
    ```json
    {
        "message": "success in test_with_auth"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success in test_with_auth'})


@bp.route('/test_with_token', methods=['GET', 'POST'])
@token_auth.login_required
def test_with_token():
    """测试Token认证请求
    @@@
    #### 请求头
    > 携带 `Authorization` 字段。\n
    ```properties
    Authorization: Bearer <token>
    ```
    #### 响应示例
    ```json
    {
        "message": "success in test_with_token"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success in test_with_token'})
