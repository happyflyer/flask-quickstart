# -*- coding: utf-8 -*-

from flask import jsonify

from . import bp, basic_auth, token_auth


@bp.route('/test_request', methods=['GET', 'POST'])
def test_request():
    """测试普通请求

    @@@
    ## 响应示例

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
    """测试http基本认证请求

    @@@
    ## 请求头

    - [HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)
    - 携带 `Authorization` 字段。`Authorization: Basic <auth>`

    ## 响应示例

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
    """测试token认证请求

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。`Authorization: Bearer <token>`

    ## 响应示例

    ```json
    {
        "message": "success in test_with_token"
    }
    ```

    @@@
    """
    return jsonify({'message': 'success in test_with_token'})
