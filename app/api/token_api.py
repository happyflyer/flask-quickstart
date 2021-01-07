from flask import jsonify, g
from .. import db
from . import bp
from .auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """获取token

    @@@
    ### 请求头
    - [HTTP Basic Authentication认证](https://www.cnblogs.com/yuqiangli0616/p/9389273.html)
    - 携带 `Authorization` 字段：`Authorization: Basic <auth>`

    ### 响应示例
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
    ### 请求头
    - 携带 `Authorization` 字段：`Authorization: Bearer <token>`

    ### 响应示例
    ```json
    {
        "token": null
    }
    ```
    @@@
    """
    g.current_user.revoke_token()
    db.session.commit()
    return jsonify({'token': None})
