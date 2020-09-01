# -*- coding: utf-8 -*-

"""pycrypto模块支持的加密方式:
对称加密方式
    - AES
    - DES
    - ARC4
散列值计算
    - MD5
    - SHA
    - HMAC
公钥加密和签名
    - RSA
    - DSA

以下错误仅见于 Windows

from Crypto import Random 导入包时候发生错误：
ModuleNotFoundError: No module named 'winrandom'

Problem is solved by editing string in crypto/Random/OSRNG/nt.py:
import winrandom
to
from . import winrandom

"""

import base64
import hashlib
import hmac
import random
import string
from abc import ABCMeta, abstractmethod

import jwt
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA

from . import ENCODING


class Coder(metaclass=ABCMeta):
    """加密算法抽象类"""

    @abstractmethod
    def encode(self, text):
        """加密

        Args:
            text (str): 明文
        """
        pass


class Base64Coder(Coder):
    """base64"""

    def encode(self, text):
        """加密

        Args:
            text (str): 明文

        Returns:
            str: 密文

        Examples:
            >>> Base64Coder().encode('hello')
        """
        token = base64.encodebytes(str.encode(text, ENCODING))
        return bytes.decode(token, ENCODING)

    def decode(self, token):
        """解密

        Args:
            token: str

        Returns:
            text str

        Examples:
            >>> token = Base64Coder().encode('hello')
            >>> Base64Coder().decode(token)
        """
        data = base64.decodebytes(str.encode(token, ENCODING))
        return bytes.decode(data, ENCODING)


class HashCoder(Coder):
    """Hash"""

    def __init__(self, algorithm='md5'):
        """初始化

        Args:
            algorithm (str, optional): 算法名，可选：'md5'|'sha1'|'sha224'|'sha256'|'sha384'|'sha512'. Defaults to 'md5'.

        Raises:
            RuntimeError: 未知的算法名
        """
        super().__init__()

        if algorithm.lower() == 'md5':
            self.__hash = hashlib.md5()
        elif algorithm.lower() == 'sha1':
            self.__hash = hashlib.sha1()
        elif algorithm.lower() == 'sha224':
            self.__hash = hashlib.sha224()
        elif algorithm.lower() == 'sha256':
            self.__hash = hashlib.sha256()
        elif algorithm.lower() == 'sha384':
            self.__hash = hashlib.sha384()
        elif algorithm.lower() == 'sha512':
            self.__hash = hashlib.sha512()
        else:
            raise RuntimeError('Unknown encryption algorithm!')

    def encode(self, text, salt=None):
        """加密

        Args:
            text (str): 明文
            salt (object), optional): 加盐值. Defaults to None.

        Returns:
            str: 密文

        Examples:
            >>> HashCoder().encode('hello')
        """
        self.__hash.update(str.encode(text, ENCODING))
        if salt is not None:
            result = self.__hash.hexdigest() + str(salt)
            self.__hash.update(str.encode(result, ENCODING))
        return self.__hash.hexdigest()


class HmacCoder(Coder):
    """Hmac"""

    def __init__(self, key, msg, algorithm='md5'):
        """初始化

        Args:
            key (str): key
            msg (str): msg
            algorithm (str, optional): 算法名，可选：'md5'|'sha1'|'sha224'|'sha256'|'sha384'|'sha512'. Defaults to 'md5'.

        Raises:
            RuntimeError: 未知的算法名
        """
        super().__init__()
        if algorithm.lower() == 'md5':
            self.__digestmod = hashlib.md5
        elif algorithm.lower() == 'sha1':
            self.__digestmod = hashlib.sha1
        elif algorithm.lower() == 'sha224':
            self.__digestmod = hashlib.sha224
        elif algorithm.lower() == 'sha256':
            self.__digestmod = hashlib.sha256
        elif algorithm.lower() == 'sha384':
            self.__digestmod = hashlib.sha384
        elif algorithm.lower() == 'sha512':
            self.__digestmod = hashlib.sha512
        else:
            raise RuntimeError('Unknown encryption algorithm!')
        self.__hmac = hmac.new(
            key=str.encode(key, ENCODING),
            msg=str.encode(msg, ENCODING),
            digestmod=self.__digestmod)

    def encode(self, text):
        """加密

        Args:
            text (str): 明文

        Returns:
            str: 密文

        Examples:
            >>> HmacCoder(key='hh', msg='kk').encode('hello')
        """
        self.__hmac.update(str.encode(text, ENCODING))
        return self.__hmac.hexdigest()


class AESCoder(Coder):
    """AES"""

    def __init__(self, key):
        """初始化

        Args:
            key (str): key，长度必须为 16(AES-128)|24(AES-192)|32(AES-256) Bytes，目前 16 Bytes 已经够用
        """
        self.__key = key
        self.__mode = AES.MODE_CBC

    def encode(self, text):
        """加密

        Args:
            text (str): 明文

        Returns:
            str: 密文

        Examples:
            >>> AESCoder('hellohellohelloo').encode('hello')
        """
        # 如果 text 不是 16 的倍数，那就补足为 16 的倍数
        length = 16
        count = len(text)
        add = length - (count % length if count % length else length)
        text = text + '\0' * add
        self.__cryptor = AES.new(self.__key, self.__mode, self.__key)
        self.ciphertext = self.__cryptor.encrypt(str.encode(text, ENCODING))
        # 因为AES加密时候得到的字符串不一定是 ascii 字符集的
        # 输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        token = b2a_hex(self.ciphertext)
        return bytes.decode(token, ENCODING)

    def decode(self, token):
        """解密

        Args:
            token (str): 密文

        Returns:
            str: 明文

        Examples:
            >>> token = AESCoder('hellohellohelloo').encode('hello')
            >>> AESCoder('hellohellohelloo').decode(token)
        """
        self.__cryptor = AES.new(self.__key, self.__mode, self.__key)
        text = self.__cryptor.decrypt(a2b_hex(str.encode(token, ENCODING)))
        return bytes.decode(text, ENCODING).rstrip('\0')


class RSACoder(Coder):
    """RSA"""

    def __init__(self):
        """初始化"""
        super().__init__()
        rsa = RSA.generate(1024, Random.new().read)
        # 生成秘钥对
        self.__public_key = rsa.publickey().exportKey().decode(ENCODING)
        self.__private_key = rsa.exportKey().decode(ENCODING)

    def encode(self, text):
        """加密

        Args:
            text (str): 明文

        Returns:
            str: 密文

        Examples:
            >>> RSACoder().encode('hello')
        """
        # 导入公钥
        rsakey = RSA.importKey(self.__public_key)
        # 生成对象
        cipher = PKCS1_v1_5.new(rsakey)
        # 通过生成的对象加密text明文，
        # 注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
        token = base64.b64encode(cipher.encrypt(text.encode(ENCODING)))
        # 公钥每次加密的结果不一样跟对数据的padding（填充）有关
        return bytes.decode(token, ENCODING)

    def decode(self, token):
        """解密

        Args:
            token (str): 密文

        Returns:
            str: 明文

        Examples:
            >>> rsa = RSACoder()
            >>> token = rsa.encode('hello')
            >>> rsa.decode(token)
        """
        # 导入私钥
        rsakey = RSA.importKey(self.__private_key)
        # 生成对象
        cipher = PKCS1_v1_5.new(rsakey)
        # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        text = cipher.decrypt(base64.b64decode(token), "ERROR")
        return bytes.decode(text, ENCODING)


class JWTCoder(Coder):
    """JWT"""

    def __init__(self, key):             
        """初始化

        Args:
            key (str): key
        """
        super().__init__()

        self.__key = key

    def encode(self, payload, algorithm='HS256'):
        """加密

        Args:
            payload (dict): 明文
            algorithm (str, optional): 算法. Defaults to 'HS256'.

        Returns:
            str: 密文

        Examples:
            >>> JWTCoder('hello').encode({'hello': 'world'})
        """
        # jwt.encode(payload, key, algorithm='HS256', headers=None, json_encoder=None)
        # token = jwt.encode({'a': 'b'}, 'my-secret', algorithm='HS256')
        token = jwt.encode(payload, key=self.__key, algorithm=algorithm)
        return bytes.decode(token, ENCODING)

    def decode(self, token, algorithms=['HS256']):
        """解密

        Args:
            token (str): 密文
            algorithms (list, optional): 算法. Defaults to ['HS256'].

        Returns:
            dict: 明文

        Examples:
            >>> token = JWTCoder('hello').encode({'hello': 'world'})
            >>> JWTCoder('hello').decode(token)
        """
        # jwt.decode(jwt, key='', verify=True, algorithms=None, options=None, **kwargs)
        # jwt.decode(token, 'my-secret', algorithms=['HS256'])
        text = jwt.decode(token, key=self.__key, algorithms=algorithms)
        return text


def generate_random_string(length, digits=False, punctuation=False):
    """生成随机字符串

    Args:
        length (int): 长度
        digits (bool, optional): 是否包含数字. Defaults to False.
        punctuation (bool, optional): 是否包含符号. Defaults to False.

    Returns:
        str: 随机字符串

    Examples:
        >>> generate_random_string(16)
    """
    s = string.ascii_letters
    if digits:
        s += string.digits
    if punctuation:
        s += string.punctuation
    while len(s) < length:
        s *= 2
    return ''.join(random.sample(s, length))
