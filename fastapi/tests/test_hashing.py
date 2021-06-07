import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from core.hashing import Hashing

hash = Hashing.get_password_hash("mypassword")

def test_get_password_hash():
    assert hash.startswith("$2b$12$")

def test_verify_password():
    assert Hashing.verify_password("mypassword", hash)