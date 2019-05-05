import re
import yaml

abbreviations = yaml.load(open("abbreviations.yaml", "r"), Loader=yaml.BaseLoader)


def parse_addr(addr):
    tokens = split(addr)
    result = {**{k: "" for k in abbreviations.keys()}, 'zip': "", 'note': ""}

    last_state = 'none'
    all_states = set()

    # ZIP as special case
    if re.match('\\d+', tokens[0]):
        if tokens[0].isdigit() and int(tokens[0]) in range(99999, 1000000):
            result['zip'] = tokens[0]
            all_states.add('zip')
            last_state = 'zip'
        tokens = tokens[1:]

    for token in tokens:
        # skip empty
        if not len(token):
            continue

        found = False
        for field, params in abbreviations.items():
            if found:
                break
            if any((x in all_states) for x in params['not']):
                continue
            if not (last_state in params['after']):
                continue
            if match(token, params['match']) or field == 'house' and not match(token, abbreviations['building']['match']):
                last_state = field
                all_states.add(field)
                found = True
                append(result, field, token)
                continue

            # a/я as special case
            if field == 'street' and last_state in {'region', 'city', 'street'} and 'building' not in all_states and match(token, ('а/я',)):
                last_state = 'note'
                all_states.add('note')
                all_states.add('building')
                result['building'] = token
                found = True

        # note as special case
        if not found:
            if last_state in {'city', 'building', 'street', 'house', 'office'}:
                last_state = 'note'
            append(result, 'note', token)

    return result


def split(addr):
    return re.split('\\s*,\\s+', addr)


def match(real, pattern):
    return bool(re.search('\\b({})\\.?\\b'.format('|'.join(pattern)), real, re.IGNORECASE))


def replace(real, pattern):
    return re.sub('\\b{}\\.?\\b'.format(pattern), real, '', re.IGNORECASE)


def append(result, field, data):
    if result.get(field):
        result[field] += ', ' + data
    else:
        result[field] = data
