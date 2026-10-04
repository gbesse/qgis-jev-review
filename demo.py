import json

from jev_qgis_review.core import FeatureRecord, build_request, fake_response, parse_response

features = [
    FeatureRecord("12", {"site": "École Nord", "status": "verified"}),
    FeatureRecord("19", {"site": "Gymnase", "status": "unknown"}),
]
categories = ["consistent", "needs_review", "out_of_scope"]
request = build_request(features, ["site", "status"], categories, "Route records by documented attribute quality.")
print(json.dumps(parse_response(fake_response(features, categories), features, categories), indent=2, ensure_ascii=False))
assert request["state"]["features"][0]["id"] == "12"
