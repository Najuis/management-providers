import argon2 as argon

from argon2.exceptions import VerifyMismatchError

ph = argon.PasswordHasher()

def check_password(plain_password, hashed_password):    

    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:

        print("Unverified password {e}")
        return False
