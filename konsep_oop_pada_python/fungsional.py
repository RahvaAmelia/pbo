#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

def input_alas_dan_tinggi():
    alas = float(input('Masukkan alas: '))
    tinggi = float(input('Masukkan tinggi: '))
    return alas, tinggi


def hitung_luas_segitiga(alas, tinggi):
    return 0.5 * alas * tinggi


"""Kalau fungsional, kita sendiri yang mengelola
hasil kembaliannya"""

# satu fungsi bisa dipanggil secara independen
print(hitung_luas_segitiga(5, 10))

# contoh dengan inputan alas dan tinggi
alas, tinggi = input_alas_dan_tinggi()
print(hitung_luas_segitiga(alas, tinggi))
