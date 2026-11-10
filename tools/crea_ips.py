#!/usr/bin/env python3
"""Crea un parche IPS con las diferencias entre dos ficheros.

Uso: python3 crea_ips.py original destino parche.ips

El destino puede ser más largo que el original (los bytes nuevos van en
registros al final). El IPS no sabe acortar ficheros, así que el destino no
puede ser más corto.
"""
import sys

MAX_REG = 0xFFFF
EOF_OFS = 0x454F46  # "EOF": un registro no puede empezar aquí


def crea_ips(orig, dest):
    if len(dest) < len(orig):
        raise ValueError("el destino es más corto que el original")
    if len(dest) > 0x1000000:
        raise ValueError("IPS solo admite ficheros de hasta 16 MB")
    out = bytearray(b"PATCH")
    i = 0
    while i < len(dest):
        if i < len(orig) and orig[i] == dest[i]:
            i += 1
            continue
        ini = i
        if ini == EOF_OFS:
            ini -= 1
        fin = i
        while fin < len(dest) and fin - ini < MAX_REG:
            if fin < len(orig) and orig[fin] == dest[fin]:
                # cortar solo si vienen varios bytes iguales seguidos
                j = fin
                while j < len(orig) and j < len(dest) and orig[j] == dest[j] and j - fin < 6:
                    j += 1
                if j - fin >= 6 or j >= len(dest):
                    break
                fin = j
            else:
                fin += 1
        out += ini.to_bytes(3, "big") + (fin - ini).to_bytes(2, "big") + dest[ini:fin]
        i = fin
    out += b"EOF"
    return bytes(out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    orig = open(sys.argv[1], "rb").read()
    dest = open(sys.argv[2], "rb").read()
    open(sys.argv[3], "wb").write(crea_ips(orig, dest))
