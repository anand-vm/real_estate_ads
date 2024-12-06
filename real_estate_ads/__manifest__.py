{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://www.catalisterp.com",
    "author": "Anand",
    "description": "Real Estate Module to List Properties",
    "category": "Sales",
    "depends": ["base","mail"],

    "assets": {
    "web.assets_backend": [
        "real_estate_ads/static/src/js/my_custom_tag.js",
        "real_estate_ads/static/src/xml/my_custom_tag.xml",
            ],
        },



    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "security/model_access.xml",
        "views/property_tag_view.xml",
        "views/property_type_view.xml",
        "views/property_offer_view.xml",
        "views/property_view.xml",
        "views/menu_items.xml",

        # Data files
        # "data/property_type.xml",
        "data/estate.property.type.csv",
        "reports/report_template.xml",
        "reports/property_report.xml",
    ],
    "demo": [
        "demo/property_tag.xml",
    ],

    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
