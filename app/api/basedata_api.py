from flask import jsonify
from ..modules import MODULES
from ..permission import PERMISSIONS
from . import bp


@bp.route('/modules', methods=['GET'])
def get_modules_api():
    """获取注册模块

    @@@
    @@@
    """
    return jsonify(MODULES)


@bp.route('/permissions', methods=['GET'])
def get_permissions_api():
    """获取权限级别

    @@@
    @@@
    """
    return jsonify(PERMISSIONS)
