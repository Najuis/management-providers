from argon2 import PasswordHasher

def hasher(hashed):
    
    ph = PasswordHasher()
    
    hasher = ph.hash(hashed)

    return hasher 