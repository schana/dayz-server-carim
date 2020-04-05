import re


class Fields:
    NAME = 'name'
    LIFETIME = 'lifetime'
    NOMINAL = 'nominal'
    RESTOCK = 'restock'
    MIN = 'min'
    CATEGORY = 'category'
    VALUE = 'value'
    FLAGS = 'flags'
    OPERATOR = 'operator'
    USAGE = 'usage'


class Match:
    def __init__(self, matching):
        self.fields = {Fields.OPERATOR: all}
        if Fields.NAME in matching:
            self.fields[Fields.NAME] = re.compile(matching.get(Fields.NAME))
        for f in (Fields.LIFETIME, Fields.NOMINAL, Fields.RESTOCK, Fields.MIN):
            if f in matching:
                self.fields[f] = re.compile(matching.get(f))
        if Fields.CATEGORY in matching:
            self.fields[Fields.CATEGORY] = re.compile(matching.get(Fields.CATEGORY).get('name'))
        if Fields.VALUE in matching:
            self.fields[Fields.VALUE] = []
            for value in matching.get(Fields.VALUE):
                self.fields[Fields.VALUE].append(re.compile(value.get('name')))
        if Fields.USAGE in matching:
            self.fields[Fields.USAGE] = []
            for usage in matching.get(Fields.USAGE):
                self.fields[Fields.USAGE].append(re.compile(usage.get('name')))
        if Fields.FLAGS in matching:
            self.fields[Fields.FLAGS] = {}
            for flag in matching.get(Fields.FLAGS):
                self.fields[Fields.FLAGS][flag.get('name')] = flag.get('value')
        if Fields.OPERATOR in matching:
            self.fields[Fields.OPERATOR] = any if matching.get(Fields.OPERATOR).lower() == 'any' else all

    def match(self, t):
        match_result = MatchResult(self.fields[Fields.OPERATOR])
        if Fields.NAME in self.fields:
            match_result.add_interim(self.fields[Fields.NAME].match(t.attrib.get(Fields.NAME)))
        for f in (Fields.LIFETIME, Fields.NOMINAL, Fields.RESTOCK, Fields.MIN):
            if f in self.fields:
                field_value = t.find(f)
                if field_value is None:
                    match_result.add_interim(False)
                else:
                    match_result.add_interim(self.fields[f].match(field_value.text))
        if Fields.CATEGORY in self.fields:
            category = t.find(Fields.CATEGORY)
            if category is None:
                match_result.add_interim(False)
            else:
                match_result.add_interim(self.fields[Fields.CATEGORY].match(category.attrib.get('name')))
        if Fields.VALUE in self.fields:
            if len(self.fields[Fields.VALUE]) == 0:
                if t.find(Fields.VALUE) is None:
                    match_result.add_interim(True)
                else:
                    match_result.add_interim(False)
            for value_match in self.fields[Fields.VALUE]:
                r = False
                for value in t.findall(Fields.VALUE):
                    m = value_match.match(value.attrib.get('name'))
                    if m:
                        r = True
                        match_result.add_interim(m)
                if not r:
                    match_result.add_interim(r)
        if Fields.USAGE in self.fields:
            if len(self.fields[Fields.USAGE]) == 0:
                if t.find(Fields.USAGE) is None:
                    match_result.add_interim(True)
                else:
                    match_result.add_interim(False)
            for usage_match in self.fields[Fields.USAGE]:
                r = False
                for usage in t.findall(Fields.USAGE):
                    m = usage_match.match(usage.attrib.get('name'))
                    if m:
                        r = True
                        match_result.add_interim(m)
                if not r:
                    match_result.add_interim(r)
        if Fields.FLAGS in self.fields:
            type_flags = t.find(Fields.FLAGS)
            if len(self.fields[Fields.FLAGS]) == 0:
                if type_flags is None:
                    match_result.add_interim(True)
                else:
                    match_result.add_interim(False)
            for flag_name, flag_value in self.fields[Fields.FLAGS].items():
                expected_flag = '1' if flag_value else '0'
                if type_flags.get(flag_name) == expected_flag:
                    match_result.add_interim(True)
                else:
                    match_result.add_interim(False)
        return match_result


class MatchResult:
    def __init__(self, operator):
        self.groups = dict()
        self.interim_results = list()
        self.operator = operator

    def add_interim(self, result):
        if result:
            self.interim_results.append(bool(result))
            if not isinstance(result, bool) and result.groupdict():
                self.groups = dict(**self.groups, **result.groupdict())
        else:
            self.interim_results.append(False)

    def get_result(self):
        return self.operator(self.interim_results)

    def __bool__(self):
        return self.get_result()
