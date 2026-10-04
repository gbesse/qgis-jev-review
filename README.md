# QGIS Jev Feature Review

A QGIS plugin that reviews the attributes of selected vector features with finite categories and preserves exact feature IDs. Geometry is not transmitted. Version 0.1.0 is an experimental preview-only plugin: it applies no layer edits.

## Offline proof

```bash
python3 -m unittest discover -s tests
python3 demo.py
```

## Install in QGIS

Run `sh scripts/package.sh`, then use **Plugins → Manage and Install Plugins → Install from ZIP**. Select features on a vector layer and choose **Vector → Jev Feature Review**. Live review reads `TYPESAFE_API_KEY` from the QGIS process environment; the key is never stored in the project or layer.

The first pack routes records to `consistent`, `needs_review`, or `out_of_scope`. Confidence below the threshold is always marked for review. Only explicitly selected attribute fields should be included in a production policy; this MVP uses all fields visible on the active layer, so inspect data sensitivity before running it.

## Boundaries

This is a data-quality triage aid, not a geospatial model or regulatory determination. It does not evaluate geometry, spatial relationships or hidden attributes. Results are previewed and anchored to feature IDs so a human can inspect the source record.

Independent community integration. MIT licensed and compatible with QGIS plugin distribution requirements.
