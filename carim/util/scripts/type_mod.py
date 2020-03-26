import xml.etree.ElementTree as ET


def zone_rates(ratio, file_in, file_out):
    tree = ET.parse(file_in)
    root = tree.getroot()
    for child in root.findall('.//zone'):
        dmin = int(child.get('dmin'))
        dmax = int(child.get('dmax'))
        child.set('dmin', str(dmin * ratio))
        child.set('dmax', str(dmax * ratio))
    tree.write(file_out)


def zed_rates(ratio):
    zone_rates(
        ratio,
        'original/zombie_territories.xml',
        'dayzOffline.chernarusplus/env/zombie_territories.xml')


def bear_rates(ratio):
    zone_rates(
        ratio,
        'original/bear_territories.xml',
        'dayzOffline.chernarusplus/env/bear_territories.xml')


def main():
    zed_rates(1)
    bear_rates(1)


if __name__ == '__main__':
    main()
