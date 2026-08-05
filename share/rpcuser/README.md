RPC Tools
---------------------

### [RPCUser](/share/rpcuser) ###

Create an RPC user login credential.

Usage:

    # Show rpcauth line and password
    ./rpcuser.py <username>

    # Only print the rpcauth=... line (no password)
    ./rpcuser.py <username> --only-line

    # Append the rpcauth line to your dogecoin.conf
    ./rpcuser.py <username> --append ~/.dogecoin/dogecoin.conf

Options:

- `--salt-bytes N`    Number of random bytes used for the salt (default: 16)
- `--password-bytes N` Number of random bytes used to generate the password (default: 32)

Security notes:

- Only add the `rpcauth=...` line to `dogecoin.conf`; do NOT store the plaintext password in configuration files.
- Ensure `dogecoin.conf` permissions are restrictive (e.g. `chmod 600 ~/.dogecoin/dogecoin.conf`).
- The script by default uses the hex-encoded salt string as the HMAC key to preserve compatibility with the original script; if you prefer raw salt bytes as the HMAC key, update the implementation accordingly.
