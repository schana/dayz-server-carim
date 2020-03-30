import json
from xml.etree import ElementTree

from carim.global_resources import matching_model

types = ElementTree.parse('generated-output/servers/0/mpmissions/dayzOffline.chernarusplus/db/types.xml')


def get_functions_to_run():
    return [
        # describe_xml,
        # get_class_names_by_tier,
        # get_names_by_cat,
        # get_names_by_match,
        # convert_mass_weapon_names_to_regex
        # get_items_for_airdrop
        get_stats,
        lambda: print('vanilla'),
        lambda: get_stats(
            (ElementTree.parse('D:/DayZServer/deploy/mpmissions/dayzOffline.chernarusplus/db/types.xml').getroot()))
    ]


def main():
    for f in get_functions_to_run():
        f()


def get_stats(types_et=None):
    if types_et is None:
        types_et = types.getroot()
    sum_nominal = 0
    count_items = 0
    sum_min = 0
    nominals = {}
    mins = {}
    restocks = {}
    matching = [
        {
            "nominal": "^[^0]",
            # "restock": "^0$",
            "flags": [
                {
                    "name": "deloot",
                    "value": False
                }
            ]
        }
    ]
    for match in matching:
        m = matching_model.Match(match)
        for t in types_et:
            if m.match(t) and t.find('nominal') is not None:
                nominal = int(t.find('nominal').text)
                min_value = int(t.find('min').text)
                restock = int(t.find('restock').text)
                # print(t.get('name'), nominal, min_value, restock)
                sum_nominal += nominal
                if nominal not in nominals:
                    nominals[nominal] = 0
                nominals[nominal] += 1
                sum_min += min_value
                if min_value not in mins:
                    mins[min_value] = 0
                mins[min_value] += 1
                if restock not in restocks:
                    restocks[restock] = 0
                restocks[restock] += 1
                count_items += 1
    # print('''vanilla stats
    # items 1285
    # sum nominal 20128
    # avg nominal 15.663813229571984
    # sum min 12571
    # avg min 9.782879377431907''')
    print('items', count_items)
    print('sum nominal', sum_nominal)
    print('avg nominal', sum_nominal / max(1, count_items))
    print('nominal values')
    print(json.dumps([str((k, v)) for k, v in sorted(nominals.items())], indent=2))
    print('sum min', sum_min)
    print('avg min', sum_min / max(1, count_items))
    print('min values')
    print(json.dumps([str((k, v)) for k, v in sorted(mins.items())], indent=2))
    print('restock values')
    print(json.dumps([str((k, v)) for k, v in sorted(restocks.items())], indent=2))
    print()


def convert_mass_weapon_names_to_regex():
    with open('resources/original-mod-files/MasssManyItemOverhaul/mass_weapon_class_names.txt') as f:
        lines = f.readlines()
    result = '(' + '|'.join(l.strip() for l in lines) + ')'
    print(result)


def get_items_for_airdrop():
    matching = [
        {
            "name": "(?!.*(Bu?ttsto?ck|Light|Bayonet|Hndgrd|Knife|Compensator|LRS|Scope|Muzzle|Holo|Binocs|STANAG|Mushroom).*)",
            "category": {
                "name": "weapons"
            },
            "value": [
                {
                    "name": "Tier4"
                }
            ],
            "flags": [
                {
                    "name": "deloot",
                    "value": False
                }
            ]
        },
        {
            "name": ".*(CodeLock|Tent|GhillieSuitBox(?!Winter)|NVG(?!Headstrap)).*"
        },
        {
            "name": "(csmcmillan_mung|MSFC_Barret50BMG_Black|MSFC_OSV96)"
        }
    ]
    for match in matching:
        m = modify_types.Match(match)
        for t in types.getroot():
            if m.match(t):
                print('"' + t.get('name') + '",')


def get_names_by_match():
    matching = [
        {
            "name": "(?!.*(Bu?ttsto?ck|Optic|Light|Suppressor|Goggles|Bayonet|[mM]ag|Hndgrd|Knife|Ammo|Compensator|LRS|Scope|Muzzle|drum|Holo|Binocs|STANAG|Mushroom).*)",
            "category": {
                "name": "weapons"
            },
            "value": [
                {
                    "name": "Tier3"
                }
            ]
        }
    ]
    for match in matching:
        m = modify_types.Match(match)
        for t in types.getroot():
            if m.match(t) and t.find('nominal') is not None:
                print('"' + t.get('name') + '",' + '\t' + str(list(v.get('name') for v in t.findall('value'))))


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
