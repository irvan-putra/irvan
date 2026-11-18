#!/usr/bin/env python3
"""Launcher icon generator: Irvan's photo plus the shared version badge.

Same convention as the other com.vanipy.* apps: numbers-only version on a
full-width strip across the bottom of the icon, one consistent corner radius.
The photo is his own (assets/irvan-photo.png), used at his request.

Deterministic. Same version in, same PNGs out. Inputs are pinned: Pillow
PILLOW_PIN and DejaVu Sans Bold with sha256 FONT_SHA256. The script fails
instead of falling back to another font or Pillow version, because a
different rasterizer or font changes the pixels.
    pip install pillow==12.3.0   (fonts-dejavu-core provides the font)
"""
import hashlib
import os
import re
import sys

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFont

PILLOW_PIN = "12.3.0"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SHA256 = "d1c3ff99f1e1ce1827a33efd4dad81f40babda06bff9e43bd7591c86662a287b"
DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
S = 768
STRIP_TOP = 0.76      # strip covers 76%..100% of the icon height
TEXT_SIZE = 0.115     # numeral size, fraction of icon size
SAFE_R = 0.485        # version text must stay inside this radius (fraction)

STRIP = (16, 20, 24, 255)
WHITE = (255, 255, 255, 255)

if PIL.__version__ != PILLOW_PIN:
    sys.exit("Pillow %s required, found %s" % (PILLOW_PIN, PIL.__version__))


def font(px):
    if not os.path.exists(FONT_PATH):
        sys.exit("missing font " + FONT_PATH)
    if hashlib.sha256(open(FONT_PATH, "rb").read()).hexdigest() != FONT_SHA256:
        sys.exit("unexpected font file " + FONT_PATH)
    return ImageFont.truetype(FONT_PATH, px)


def circle_mask(size, r=SAFE_R):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse([size * (.5 - r), size * (.5 - r), size * (.5 + r), size * (.5 + r)], fill=255)
    return m


def assert_inside_circle(layer, what, size=S, r=SAFE_R):
    alpha = layer.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    outside = ImageChops.multiply(alpha, ImageChops.invert(circle_mask(size, r)))
    box = outside.getbbox()
    if box:
        sys.exit("%s leaves the round-mask safe circle at %s" % (what, box))


def irvan(version):
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    photo = Image.open(os.path.join(root, "assets", "irvan-photo.png")).convert("RGBA")
    side = min(photo.size)
    photo = photo.crop(((photo.width - side) // 2, (photo.height - side) // 2,
                        (photo.width + side) // 2, (photo.height + side) // 2))
    base = photo.resize((S, S), Image.LANCZOS)
    d = ImageDraw.Draw(base)
    y0 = int(S * STRIP_TOP)
    d.rectangle([0, y0, S, S], fill=STRIP)
    text = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(text).text((S / 2, (y0 + S) / 2), version, font=font(int(S * TEXT_SIZE)),
                              fill=WHITE, anchor="mm")
    assert_inside_circle(text, "version text")
    base.alpha_composite(text)
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=0.2 * S, fill=255)
    base.putalpha(ImageChops.multiply(base.getchannel("A"), m))
    return base


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else None
    if not version or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit("version must be X.Y.Z")
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    res = os.path.join(root, "app", "src", "main", "res")
    img = irvan(version)
    for dens, px in DENSITIES.items():
        out = os.path.join(res, "mipmap-" + dens)
        os.makedirs(out, exist_ok=True)
        img.resize((px, px), Image.LANCZOS).save(os.path.join(out, "ic_launcher.png"), optimize=True)
    print("wrote icons for", version)


if __name__ == "__main__":
    main()
