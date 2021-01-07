from flask import jsonify
from ...modules import MODULES
from ...permission import PERMISSIONS
from .. import bp


@bp.route('/api/modules', methods=['GET'])
def get_modules_api():
    """获取注册模块
    """
    return jsonify(MODULES)


@bp.route('/api/permission', methods=['GET'])
def get_permissions_api():
    """获取权限级别
    """
    return jsonify(PERMISSIONS)
