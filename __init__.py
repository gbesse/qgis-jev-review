def classFactory(iface):  # noqa: N802
    from jev_qgis_review.plugin import JevFeatureReviewPlugin

    return JevFeatureReviewPlugin(iface)
