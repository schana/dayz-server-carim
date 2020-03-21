import math
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


def type_rates(ratio):
    change_min = False
    tree = ET.parse('original/types.xml')
    root = tree.getroot()
    for child in root:
        if 'Zmb' not in child.get('name'):
            # print(child.get('name'))
            if change_min:
                min_element = child.find('min')
                if min_element is not None:
                    min_element.text = str(0)
            nominal = child.find('nominal')
            if nominal is not None:
                n = int(nominal.text)
                nominal.text = str(max(min(n, 1), math.floor(n * ratio)))
    tree.write('dayzOffline.chernarusplus/db/types.xml')


def modify_globals():
    tree = ET.parse('original/globals.xml')
    root = tree.getroot()
    for child in root.findall('.//var'):
        if child.get('name') in ('ZombieMaxCount', 'AnimalMaxCount'):
            child.set('value', str(10000))
        if child.get('name') in ('TimeLogin', 'TimeLogout'):
            child.set('value', str(3))
    tree.write('dayzOffline.chernarusplus/db/globals.xml')


def event_animal_rates(ratio):
    tree = ET.parse('original/events.xml')
    root = tree.getroot()
    for child in root.findall('.//event'):
        if 'Animal' in child.get('name'):
            print(child.get('name'))
            active = child.find('active')
            active.text = str(1)
            nominal = child.find('nominal')
            nominal.text = str(math.floor(max(1, int(nominal.text)) * ratio))
    tree.write('dayzOffline.chernarusplus/db/events.xml')


def main():
    modify_globals()
    type_rates(1.0)
    zed_rates(1)
    bear_rates(1)
    event_animal_rates(3)


if __name__ == '__main__':
    main()
