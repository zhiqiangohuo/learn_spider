from pyDes import *
import binascii
# 秘钥
secret_key ='11111111'
def ens_encrypt(str_msg):
    """
    des
    参数说明：
    secret_key:秘钥必须8位以上
    IV : 偏移量
    str_msg: 需要加密的参数
    """
    iv = secret_key
    k = des(secret_key,CBC,iv,pad=None,padmode=PAD_PKCS5)
    en = k.encrypt(str_msg,padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)
def des_descrypt(str_msg):
    iv = secret_key
    k = des(secret_key,CBC,iv,pad=None,padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(str_msg),padmode=PAD_PKCS5)
    return de
if __name__ == "__main__":
    a = "helloword"
    b = ens_encrypt(a)
    print(b)
    c = des_descrypt(b)
    print(c)

    