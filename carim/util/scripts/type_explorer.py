import json
from xml.etree import ElementTree

types = ElementTree.parse('generated-output/servers/0/mpmissions/dayzOffline.chernarusplus/db/types.xml')


def get_functions_to_run():
    return [
        get_class_names_by_tier
    ]


def main():
    for f in get_functions_to_run():
        f()


def get_class_names_by_tier():
    results = {}
    for t in types.getroot():
        values = t.findall('value')
        for v in values:
            name = v.get('name')
            if name not in results:
                results[name] = set()
            results[name].add(t.get('name'))
    for i in range(4, 0, -1):
        tier = 'Tier{}'.format(i)
        print(tier)
        results[tier] = sorted(
            list(results[tier].difference(*(results['Tier{}'.format(j)] for j in range(i - 1, 0, -1)))))
    print(json.dumps(results, indent=2))
    print(results.keys())


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
    print(cats)
    print(json.dumps(type_spec, indent=2))


if __name__ == '__main__':
    main()
