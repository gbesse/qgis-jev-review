import unittest

from jev_qgis_review.core import FeatureRecord, build_request, parse_response, sanitize_features


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.features = [FeatureRecord("7", {"name": "Exact", "secret": "not sent"})]

    def test_only_selected_fields_are_sent(self):
        self.assertEqual(sanitize_features(self.features, ["name"]), [{"id": "7", "attributes": {"name": "Exact"}}])

    def test_question_is_anchored_to_feature_id(self):
        request = build_request(self.features, ["name"], ["ok", "review"], "Check evidence")
        self.assertIn("feature id 7", request["questions"]["feature_0"]["instructions"])

    def test_low_confidence_routes_to_review(self):
        response = {"answers": {"feature_0": {"type": "choice", "choice": "ok", "confidence": 0.4}}}
        self.assertTrue(parse_response(response, self.features, ["ok", "review"])[0]["reviewRequired"])

    def test_unknown_category_is_rejected(self):
        response = {"answers": {"feature_0": {"type": "choice", "choice": "invented", "confidence": 1}}}
        with self.assertRaises(ValueError):
            parse_response(response, self.features, ["ok", "review"])

    def test_explicit_review_category_forces_review(self):
        response = {"answers": {"feature_0": {"type": "choice", "choice": "needs_review", "confidence": 0.99}}}
        self.assertTrue(parse_response(response, self.features, ["ok", "needs_review"])[0]["reviewRequired"])


if __name__ == "__main__":
    unittest.main()
