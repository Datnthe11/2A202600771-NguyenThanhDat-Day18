import ssl

# Fix for Windows SSL "ASN1: NOT_ENOUGH_DATA" and circular import
_orig_create_default_context = ssl.create_default_context

def patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    ctx = ssl._create_unverified_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)
    return ctx

ssl.create_default_context = patched_create_default_context
ssl._create_default_https_context = ssl._create_unverified_context

import datasets.utils.logging
