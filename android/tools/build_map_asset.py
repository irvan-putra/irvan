#!/usr/bin/env python3
"""Bundle the repo-root index.html as the app's offline WebView asset.

The whole map is one self-contained file (inline SVG, inline script, embedded
photo), so bundling is a plain copy. --check verifies the asset is in sync;
the release workflow runs it so a stale asset can never ship.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "index.html")
DST = os.path.join(ROOT, "android", "app", "src", "main", "assets", "map.html")


def main():
    src = open(SRC, "rb").read()
    if "--check" in sys.argv:
        if not os.path.exists(DST):
            sys.exit("asset missing: run tools/build_map_asset.py")
        if open(DST, "rb").read() != src:
            sys.exit("asset is stale: run tools/build_map_asset.py")
        print("asset in sync with index.html")
        return
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    open(DST, "wb").write(src)
    print("wrote", os.path.relpath(DST, ROOT), "(%d bytes)" % len(src))


if __name__ == "__main__":
    main()
