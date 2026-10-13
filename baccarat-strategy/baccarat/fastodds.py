"""Exact next-hand odds from the cards left in the shoe, computed in C.

The C source (native/odds.c) is compiled on first use with the system C compiler.
"""

from __future__ import annotations

import ctypes
import os
import subprocess
import tempfile

_HERE = os.path.dirname(__file__)
_SRC = os.path.join(_HERE, "native", "odds.c")
_lib = None


def _load():
    global _lib
    if _lib is None:
        out_dir = os.path.join(tempfile.gettempdir(), "baccarat-native")
        os.makedirs(out_dir, exist_ok=True)
        so = os.path.join(out_dir, f"odds-{int(os.path.getmtime(_SRC))}.so")
        if not os.path.exists(so):
            subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, _SRC], check=True)
        _lib = ctypes.CDLL(so)
        _lib.probabilities.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
        _lib.probabilities.restype = None
    return _lib


def probabilities(counts) -> tuple[float, float, float]:
    """(banker, player, tie) probabilities for the next hand dealt from ``counts`` (cards of value 0-9)."""
    lib = _load()
    c = (ctypes.c_int * 10)(*counts)
    out = (ctypes.c_double * 3)()
    lib.probabilities(c, out)
    return out[0], out[1], out[2]
