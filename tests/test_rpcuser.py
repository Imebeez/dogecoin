import importlib.util
import hashlib
import hmac
from pathlib import Path


def load_rpcuser_module():
    path = Path(__file__).resolve().parents[1] / "share" / "rpcuser" / "rpcuser.py"
    spec = importlib.util.spec_from_file_location("rpcuser", str(path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_password_to_hmac_deterministic():
    rpc = load_rpcuser_module()
    salt = "a1b2c3d4"
    password = "hunter2"
    expected = hmac.new(salt.encode("ascii"), password.encode("utf-8"), hashlib.sha256).hexdigest()
    assert rpc.password_to_hmac(salt, password) == expected


def test_rpcauth_format():
    rpc = load_rpcuser_module()
    salt = rpc.generate_salt(8)
    password = "p@ssw0rd"
    h = rpc.password_to_hmac(salt, password)
    line = rpc.build_rpcauth("alice", salt, h)
    assert line.startswith("rpcauth=alice:")
    assert "$" in line
