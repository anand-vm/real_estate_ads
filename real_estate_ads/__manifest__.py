{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://www.catalisterp.com",
    "author": "Anand",
    "description": "Real Estate Module to List Properties",
    "category": "Sales",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/property_tag_view.xml",
        "views/property_type_view.xml",
        "views/property_offer_view.xml",
        "views/property_view.xml",
        "views/menu_items.xml",

        # Data files
        # "data/property_type.xml",
        "data/estate.property.type.csv",
    ],
    "demo": [
        "demo/property_tag.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
