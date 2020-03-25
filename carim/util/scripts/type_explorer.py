import json
from xml.etree import ElementTree

from carim.util import modify_types

types = ElementTree.parse('generated-output/servers/0/mpmissions/dayzOffline.chernarusplus/db/types.xml')


def get_functions_to_run():
    return [
        # describe_xml,
        # get_class_names_by_tier,
        # get_names_by_cat,
        get_names_by_match,
        # convert_mass_weapon_names_to_regex
    ]


def main():
    for f in get_functions_to_run():
        f()


def convert_mass_weapon_names_to_regex():
    with open('resources/modifications/mass_weapon_class_names.txt') as f:
        lines = f.readlines()
    result = '(' + '|'.join(l.strip() for l in lines) + ')'
    print(result)


def get_names_by_match():
    matching = [
        {
            "name": "(?!.*(Helmet|Sweater|Ushanka|Jacket|[Cc]oat|Vest|Shirt|Pants|Mask|Respirator|Plate|Bag|Hood|Pouch|CPCU5|Multicam|Boots|Gorka|Canteen|Gloves|Balaclava|Bandana|Beanie|Boonie|Backpack|Visor|Belt|Goggles|Cap|BACKPACK|NVG|Knee|Mask|Mack|Beret|Case|6B[24]).*)",
            "category": {
                "name": "(?!weapons)"
            },
            "value": [
                {
                    "name": "Tier4"
                }
            ]
        }
    ]
    for match in matching:
        m = modify_types.Match(match)
        for t in types.getroot():
            if m.match(t) and t.find('nominal') is not None and t.find('flags').get('deloot') == '0':
                # print('"' + t.get('name') + '",')
                print(t.find('nominal').text, t.find('min').text, t.get('name'), sep='\t')


def get_names_by_cat():
    for t in types.getroot():
        cat = t.find('category')
        if cat is not None:
            if cat.get('name') == 'clothes':
                if t.find('nominal').text != '0':
                    print(t.get('name'))


def get_class_names_by_tier():
    results = {'none': set()}
    for i in range(1, 5):
        results['Tier{}'.format(i)] = set()
    for t in types.getroot():
        values = t.findall('value')
        if len(values) > 0:
            for v in values:
                name = v.get('name')
                results[name].add(t.get('name'))
        else:
            results['none'].add(t.get('name'))
    for i in range(4, 0, -1):
        tier = 'Tier{}'.format(i)
        if tier in results:
            results[tier] = sorted(
                list(results[tier].difference(*(results['Tier{}'.format(j)] for j in range(i - 1, 0, -1)))),
                key=lambda item: item.lower()
            )
    print(json.dumps({k: len(results.get(k)) for k in results}, indent=2))


def describe_xml():
    cats = set()
    type_spec = {}
    for t in types.getroot():
        seen_tags = set()
        for child in t:
            if child.tag in seen_tags and child.tag not in ('value', 'usage'):
                print(ElementTree.tostring(t))
            seen_tags.add(child.tag)
            values = set(type_spec.get(child.tag, list()))
            values.update(child.attrib.keys())
            # if child.text is not None:
            #     values.add(child.text)
            type_spec[child.tag] = sorted(list(values))
        c = t.find('category')
        if c is not None:
            cats.add(c.get('name'))
        else:
            print(t.get('name'))
    print(cats)
    print(json.dumps(type_spec, indent=2))


if __name__ == '__main__':
    main()
