#!/usr/bin/env python3
"""
Generate rpcauth lines for dogecoin.conf in a safe, configurable way.

Example:
  ./rpcuser.py alice
  ./rpcuser.py alice --salt-bytes 16 --password-bytes 32 --append ~/.dogecoin/dogecoin.conf
"""
from __future__ import annotations

import argparse
import sys
import hmac
import hashlib
from secrets import token_hex, token_urlsafe
from typing import Tuple


def generate_salt(size_bytes: int = 16) -> str:
    """Return a hex-encoded salt representing `size_bytes` of random data."""
    return token_hex(size_bytes)


def generate_password(size_bytes: int = 32) -> str:
    """Return a URL-safe token representing `size_bytes` of random data."""
    return token_urlsafe(size_bytes)


def password_to_hmac(salt: str, password: str) -> str:
    """
    Compute HMAC-SHA256 for the given salt and password.

    Note: preserves the original script behavior of using the hex salt string
    as the HMAC key (encoded as ASCII). If you'd prefer to use the raw salt
    bytes as the key, replace key = salt.encode("ascii") with key = bytes.fromhex(salt).
    """
    key = salt.encode("ascii")
    msg = password.encode("utf-8")
    m = hmac.new(key, msg, hashlib.sha256)
    return m.hexdigest()


def build_rpcauth(username: str, salt: str, password_hmac: str) -> str:
    """Return the rpcauth line to add to dogecoin.conf."""
    return f"rpcauth={username}:{salt}${password_hmac}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate rpcauth entries for dogecoin.conf")
    p.add_argument("username", help="RPC username to create")
    p.add_argument("--salt-bytes", type=int, default=16, help="Number of random bytes for salt (default: 16)")
    p.add_argument("--password-bytes", type=int, default=32, help="Number of random bytes for password (default: 32)")
    p.add_argument("--append", "-a", metavar="FILE", help="Append rpcauth line to FILE")
    p.add_argument("--only-line", action="store_true", help="Only print the rpcauth=... line (no password)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    username = args.username
    salt = generate_salt(args.salt_bytes)
    password = generate_password(args.password_bytes)
    password_hmac = password_to_hmac(salt, password)
    rpcauth_line = build_rpcauth(username, salt, password_hmac)

    # Output
    if args.append:
        try:
            with open(args.append, "a", encoding="utf-8") as f:
                f.write(rpcauth_line + "\n")
        except OSError as e:
            print(f"Failed to append to {args.append}: {e}", file=sys.stderr)
            return 2
        if args.only_line:
            print(rpcauth_line)
        else:
            print("Appended to", args.append)
            print(rpcauth_line)
            print("Your password:")
            print(password)
    else:
        print("String to be appended to dogecoin.conf:")
        print(rpcauth_line)
        if not args.only_line:
            print("Your password:")
            print(password)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
