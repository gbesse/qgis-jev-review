from __future__ import annotations

import json

from qgis.PyQt.QtWidgets import QAction, QMessageBox

from .client import decide
from .core import FeatureRecord, build_request, parse_response


class JevFeatureReviewPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):  # noqa: N802
        self.action = QAction("Review selected features with Jev", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToVectorMenu("Jev Feature Review", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginVectorMenu("Jev Feature Review", self.action)
            self.iface.removeToolBarIcon(self.action)

    def run(self):
        layer = self.iface.activeLayer()
        selected = list(layer.selectedFeatures()) if layer else []
        if not selected:
            QMessageBox.information(self.iface.mainWindow(), "Jev Feature Review", "Select one or more vector features first.")
            return
        field_names = [field.name() for field in layer.fields()]
        records = [FeatureRecord(str(feature.id()), {name: feature[name] for name in field_names}) for feature in selected]
        try:
            request = build_request(records, field_names, ["consistent", "needs_review", "out_of_scope"], "Classify attribute evidence for manual data-quality review. Do not infer from geometry.")
            results = parse_response(decide(request), records, ["consistent", "needs_review", "out_of_scope"])
        except Exception as error:  # QGIS surfaces provider errors without credentials or payload contents.
            QMessageBox.critical(self.iface.mainWindow(), "Jev Feature Review", str(error))
            return
        preview = "\n".join(f"Feature {item['featureId']}: {item['category']} ({item['confidence']:.0%})" for item in results)
        QMessageBox.information(self.iface.mainWindow(), "Jev review preview — no edits applied", preview)
        self.iface.messageBar().pushInfo("Jev Feature Review", json.dumps({"reviewed": len(results), "edited": 0}))
