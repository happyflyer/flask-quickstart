# -*- coding: utf-8 -*-

from flask import jsonify

from ... import read_required, MODULES, PERMISSIONS
from ...api import token_auth
from . import bp


@bp.route('/module', methods=['GET'])
@token_auth.login_required
@read_required(module='main')
def get_modules():
    """获取所有模块

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。

    ## 权限

    - 访问用户对 main 模块有 R 权限。

    ## 响应示例

    ```json
    {
        "main": 0,
        "api": 1
    }
    ```

    @@@
    """
    return jsonify(MODULES)


@bp.route('/permission', methods=['GET'])
@token_auth.login_required
@read_required(module='main')
def get_permissions():
    """获取所有权限

    @@@

    ## 请求头

    - 携带 `Authorization` 字段。

    ## 权限

    - 访问用户对 main 模块有 R 权限。

    ## 响应示例

    ```json
    {
        "0": "N",
        "1": "R",
        "2": "W"
    }
    ```

    @@@
    """
    return jsonify(PERMISSIONS)
