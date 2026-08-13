#!/usr/bin/env python3
"""Genera los iconos PNG de la PWA sin depender de Pillow ni ImageMagick.

El entorno donde se montó la app no tenía ninguna librería de imagen, así que el
PNG se escribe a mano (zlib + chunks). Se deja aquí para poder regenerar los
iconos si cambia la paleta, en vez de arrastrar dos binarios sin origen.

Uso: python3 generar-iconos.py
"""

import struct
import zlib

# Fondo: degradado en diagonal del rosa de la ciudad rosa al mango de las especias.
COLOR_A = (226, 62, 107)
COLOR_B = (247, 157, 46)
CORAZON = (255, 255, 255)

SUPERMUESTREO = 3  # suaviza los bordes del corazón y de las esquinas redondeadas


def dentro_del_corazon(x, y):
    """Ecuación implícita del corazón, con el eje Y invertido (en imagen crece hacia abajo)."""
    y = -y
    return (x * x + y * y - 1) ** 3 - x * x * y * y * y < 0


def dentro_del_cuadrado(x, y, radio):
    """Cuadrado de lado 2 centrado en el origen, con las esquinas redondeadas."""
    dx = abs(x) - (1 - radio)
    dy = abs(y) - (1 - radio)
    if dx <= 0 or dy <= 0:
        return abs(x) <= 1 and abs(y) <= 1
    return dx * dx + dy * dy <= radio * radio


def color_de_fondo(t):
    """Interpola el degradado; t va de 0 (esquina superior izquierda) a 1 (inferior derecha)."""
    return tuple(round(a + (b - a) * t) for a, b in zip(COLOR_A, COLOR_B))


def render(lado):
    filas = []
    escala = 2.0 / lado
    for py in range(lado):
        fila = bytearray()
        for px in range(lado):
            r = g = b = a = 0
            for sy in range(SUPERMUESTREO):
                for sx in range(SUPERMUESTREO):
                    x = (px + (sx + 0.5) / SUPERMUESTREO) * escala - 1
                    y = (py + (sy + 0.5) / SUPERMUESTREO) * escala - 1
                    if not dentro_del_cuadrado(x, y, 0.45):
                        continue
                    # El corazón ocupa poco más de la mitad del icono para que se
                    # siga leyendo a 60 px en la pantalla de inicio.
                    if dentro_del_corazon(x / 0.62, (y + 0.06) / 0.62):
                        cr, cg, cb = CORAZON
                    else:
                        cr, cg, cb = color_de_fondo(max(0.0, min(1.0, (x + y + 2) / 4)))
                    r += cr
                    g += cg
                    b += cb
                    a += 255
            muestras = SUPERMUESTREO * SUPERMUESTREO
            if a == 0:
                fila += bytes(4)
                continue
            cubiertas = a / 255
            fila += bytes((round(r / cubiertas), round(g / cubiertas),
                           round(b / cubiertas), round(a / muestras)))
        filas.append(bytes(fila))
    return filas


def escribir_png(ruta, filas):
    lado = len(filas)
    crudo = b"".join(b"\x00" + fila for fila in filas)

    def chunk(tipo, datos):
        return (struct.pack(">I", len(datos)) + tipo + datos
                + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", lado, lado, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(crudo, 9))
    png += chunk(b"IEND", b"")
    with open(ruta, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    for lado, nombre in ((512, "icono-512.png"), (192, "icono-192.png"), (180, "icono-180.png")):
        escribir_png(nombre, render(lado))
        print(f"{nombre} — {lado}×{lado}")
