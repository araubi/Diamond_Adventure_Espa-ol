#!/usr/bin/env python3
"""Aplica un parche IPS y, si se indica, comprueba el SHA-1 del original y del resultado.

Uso: python3 aplica_ips.py original parche.ips salida [--sha1-orig X] [--sha1-dest Y]
"""
import argparse
import hashlib
import sys


def aplica_ips(datos, parche):
    if parche[:5] != b"PATCH":
        raise ValueError("no es un parche IPS")
    out = bytearray(datos)
    p = 5
    while parche[p:p + 3] != b"EOF":
        ofs = int.from_bytes(parche[p:p + 3], "big")
        tam = int.from_bytes(parche[p + 3:p + 5], "big")
        p += 5
        if tam == 0:  # registro RLE
            tam = int.from_bytes(parche[p:p + 2], "big")
            bloque = parche[p + 2:p + 3] * tam
            p += 3
        else:
            bloque = parche[p:p + tam]
            p += tam
        if len(out) < ofs + tam:
            out.extend(b"\0" * (ofs + tam - len(out)))
        out[ofs:ofs + tam] = bloque
    return bytes(out)


def main():
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("original")
    a.add_argument("parche")
    a.add_argument("salida")
    a.add_argument("--sha1-orig")
    a.add_argument("--sha1-dest")
    o = a.parse_args()
    datos = open(o.original, "rb").read()
    if o.sha1_orig and hashlib.sha1(datos).hexdigest() != o.sha1_orig.lower():
        sys.exit("El original no es el esperado (SHA-1 distinto).")
    res = aplica_ips(datos, open(o.parche, "rb").read())
    if o.sha1_dest and hashlib.sha1(res).hexdigest() != o.sha1_dest.lower():
        sys.exit("El resultado no es el esperado (SHA-1 distinto); no se ha escrito.")
    open(o.salida, "wb").write(res)
    print("Hecho:", o.salida)


if __name__ == "__main__":
    main()
