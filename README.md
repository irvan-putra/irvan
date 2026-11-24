# irvan

An interactive map of Irvan Putra's world: what he builds, where he gathers,
and what he is curious about. Made for other people to explore.

**Everything on the map comes from public sources** - his public repos, his
public profiles, his own words on them. Nothing private.

- The map is one self-contained `index.html`: inline SVG, inline script,
  embedded photo, no external requests. Open it and it works, online or off.
- Pan by dragging, zoom by pinching or the +/- buttons, tap a place for its
  card. Item labels fade in as you zoom, like a real map.
- Deep links: `#place=apps` opens a card, `?z=2&cx=600&cy=400` frames a view.

Website: https://vanipy.com/irvan/ (GitHub Pages from this repo's main branch).

Android app: see `android/` - the same map bundled offline as
`com.vanipy.irvan`, no permissions.

## Editing the map

Content lives in two spots in `index.html`: the SVG districts (positions,
labels) and the `DATA` table (card text and links). After editing, refresh
the Android asset:

    python3 android/tools/build_map_asset.py --check   # or without --check to regenerate

`assets/irvan-photo.png` is his own photo, reused from
[irvan-putra/unggah](https://github.com/irvan-putra/unggah) at his request.

## License

AGPL-3.0. See LICENSE.

---

Built with AI assistance (Instinct and others). Not everything has been reviewed by Irvan.
