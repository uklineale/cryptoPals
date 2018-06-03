import random, os

from python.set1.eight import getBlocks
from python.set2.ten import encryptEcb
from python.set2.nine import pad_pkcs7, unpad_pkcs7
from python.set1.seven import decryptEcb

key = os.urandom(16)

def decode_cookie(str):
    d = {}
    fields = str.split('&')

    for field in fields:
        key_val = field.split('=')
        if len(key_val) == 2:
            d[key_val[0]] = key_val[1]

    return d

def encode_cookie(dict):
    decoded_str = ''

    for i in dict.items():
        decoded_str += i[0] + '=' + str(i[1]) + '&'

    return decoded_str[0:-1]

def profile_for(email):
    email = email.translate({ord(c) : None for c in '&='})
    cookie = {
        'email' : email,
        'uid' : str(10),
        'role' : 'user'
    }

    return encode_cookie(cookie)

def encrypted_profile_for(email):
    return encrypt_profile(profile_for(email))

def encrypt_profile(profile_pt):
    padded_ct = pad_pkcs7(bytes(profile_pt, 'ascii'))
    return encryptEcb(padded_ct, key)

def decrypt_profile(profile_ct):
    encoded_cookie = str(unpad_pkcs7(decryptEcb(profile_ct, key)))
    return decode_cookie(encoded_cookie)

if __name__ == '__main__':
    expose_user_shim = 'EMAILmydudedb' #last block is b'user', we'll replace this block with our own
    admin_block_shim = 'tenChars--admin' + '\x04' * 11 # second block is payload

    admin_block = encrypted_profile_for(admin_block_shim)[16:32] # save payload
    exposed_ct = encrypted_profile_for(expose_user_shim)

    cut_n_paste_ct = exposed_ct[:-16] + admin_block

    print(decrypt_profile(cut_n_paste_ct))


