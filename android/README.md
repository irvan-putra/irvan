# irvan app

The interactive world map from https://vanipy.com/irvan/ as an offline
Android app screen: pinch to zoom, drag to pan, tap a place for its card.
No permissions, no network - the whole map is bundled in the app. Links in a
card open in the browser app, never inside the map.

- Package: `com.vanipy.irvan`, launcher name `irvan`
- Version: `android/app/build.gradle.kts` (`appVersionName`, major.minor.revision)

## Map asset

`app/src/main/assets/map.html` is a copy of the repo-root `index.html` (the
map is one self-contained file):

    python3 tools/build_map_asset.py          # regenerate after index.html changes
    python3 tools/build_map_asset.py --check  # CI freshness check

The release workflow fails if the committed asset is stale.

## Icons

    pip install pillow==12.3.0
    python3 tools/badge_icon.py 0.1.0

## Build and release

Debug build and unit tests:

    ./gradlew --no-daemon testDebugUnitTest assembleDebug

Signed release: dispatch the "irvan signed release" workflow. It needs the
`IRVAN_KEYSTORE_B64`, `IRVAN_STORE_PASSWORD`, `IRVAN_KEY_ALIAS` and
`IRVAN_KEY_PASSWORD` repository secrets and publishes a GitHub pre-release
with the APK and its SHA-256.

The "irvan emulator smoke test" workflow runs on pushes to `android/**` and
installs the debug APK on an emulator, verifies the map WebView renders and
uploads screenshots.
