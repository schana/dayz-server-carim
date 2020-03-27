"""
<type name="AK74">
    <nominal>10</nominal>
    <lifetime>10800</lifetime>
    <restock>1800</restock>
    <min>5</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="1" count_in_map="1" count_in_player="0" crafted="0" deloot="0" />
    <category name="weapons" />
    <usage name="Military" />
    <value name="Tier2" />
    <value name="Tier3" />
    <value name="Tier4" />
</type>
"""

modification_template = {
    "name": "",
    "nominal": 1,
    "lifetime": 1,
    "restock": 1,
    "min": 1,
    "quantmin": 1,
    "quantmax": 1,
    "cost": 1,
    "flags": [
        {
            "name": "count_in_cargo",
            "value": False
        },
        {
            "name": "count_in_hoarder",
            "value": False
        },
        {
            "name": "count_in_map",
            "value": False
        },
        {
            "name": "count_in_player",
            "value": False
        },
        {
            "name": "crafted",
            "value": False
        },
        {
            "name": "deloot",
            "value": False
        }
    ],
    "category": {
        "name": ""
    },
    "usage": [
        {"name": ""}
    ],
    "value": [
        {"name": ""}
    ],
    "tag": {
        "name": ""
    }
}
