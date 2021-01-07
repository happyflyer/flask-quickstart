from flask import jsonify
from . import bp
from .auth import basic_auth, token_auth


@bp.route('/test_request', methods=['GET', 'POST'])
def test_request():
    """测试普通请求

    @@@
    ### 响应示例
    ```json
    {
        "message": "success"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success'})


@bp.route('/test_http_basic_auth_request', methods=['GET', 'POST'])
@basic_auth.login_required
def test_http_basic_auth_request():
    """测试http基本认证请求

    @@@
    ### 请求头
    - [HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)
    - 携带 `Authorization` 字段：`Authorization: Basic <auth>`

    ### 响应示例
    ```json
    {
        "message": "success"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success'})


@bp.route('/test_token_auth_request', methods=['GET', 'POST'])
@token_auth.login_required
def test_token_auth_request():
    """测试token认证请求

    @@@
    ### 请求头
    - 携带 `Authorization` 字段：`Authorization: Bearer <token>`

    ### 响应示例
    ```json
    {
        "message": "success"
    }
    ```
    @@@
    """
    return jsonify({'message': 'success'})
