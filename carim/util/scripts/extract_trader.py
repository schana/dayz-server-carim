import json

with open('E:/programming/TraderConfig.txt') as f:
    lines = f.readlines()

result = {}

current_category_name = None
current_category = None
for line in lines:
    if line.startswith('<Currency'):
        continue
    if line.startswith('<Trader>'):
        continue
    if line.startswith('<FileEnd'):
        break
    if len(line.strip()) == 0:
        continue
    if line.startswith('<Category>'):
        if current_category is not None:
            result[current_category_name] = sorted(current_category, key=lambda c: c.lower())
        _, _, current_category_name = line.partition(' ')
        current_category_name = current_category_name.strip()
        current_category = list()
    else:
        name, _, _ = line.partition(',')
        current_category.append(name)
result[current_category_name] = sorted(current_category, key=lambda c: c.lower())

print(json.dumps(result, indent=2))
