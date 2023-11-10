import json

def FetchAttributes(auctions, items):
    attributes_found = {', '.join(item): [] for item in items}
    not_wanted_items = ["Helmet"]
    wanted_items = ["Crimson","Terror","Aurora","Fervor","Hollow","Molten","Implosion","Lava Shell","Contagion","Attribute Shard"]
    for auction_item in auctions:
        if any(item in auction_item["item_name"] for item in not_wanted_items):
            continue
        if not any(item in auction_item["item_name"] for item in wanted_items):
            continue
        for attribute in items:
            if all(attr in auction_item["item_lore"] for attr in attribute):
                #print(auction_item["item_name"])#Here
                attribute_lines = []
                for line in auction_item["item_lore"].split('\n'):
                    if any(attr in line for attr in attribute):
                        filtered_line = remove_section_symbol(line).replace("✖", "")
                        attribute_lines.append(filtered_line)
                if attribute_lines:
                    attributes_found[', '.join(attribute)].append({
                        "item_name": auction_item["item_name"],
                        "price": auction_item["price"],
                        "uuid": auction_item["uuid"],
                        "attributes": attribute_lines
                    })

    for key, value in attributes_found.items():
        if "," in key:
            attributes_found[key] = sorted(value, key=lambda x: x["price"])
            continue
        for attribute_dict in value:
            level = get_attribute_level(attribute_dict)
            new_price = attribute_dict["price"] / (2 ** (level-1))
            attribute_dict["price"] = new_price
            
    for key, value in attributes_found.items():
        if "," not in key:
            attributes_found[key] = sorted(value, key=lambda x: x["price"])
    for attribute_group in attributes_found:
        convert_dict_to_format(attributes_found, attribute_group)

    return attributes_found


def get_sort_key(attribute_dict):
    level = get_attribute_level(attribute_dict)
    print(level)
    print(attribute_dict["price"])
    print(attribute_dict["price"] / (2 ** level-1))
    return attribute_dict["price"] / (2 ** level-1)

def get_attribute_level(attribute_dict):
    attribute_lines = attribute_dict["attributes"]
    for line in attribute_lines:
        level = extract_roman_numeral(line)
        if level:
            return roman_to_decimal(level)
    return 1

def extract_roman_numeral(text):
    words = text.split()
    if words:
        last_word = words[-1]
        if last_word.isalpha() and last_word.isupper():
            return last_word
    return None

def roman_to_decimal(roman_numeral):
    roman_dict = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    return roman_dict.get(roman_numeral, 1)

def remove_section_symbol(line):
    filtered_line = ''
    skip_next_char = False
    for char in line:
        if skip_next_char:
            skip_next_char = False
            continue
        if char == '§':
            skip_next_char = True
            continue
        filtered_line += char
    return filtered_line

def convert_dict_to_format(dictionary, dict_key):
    max_length = max(len(str(item[key])) for item in dictionary[dict_key] for key in item)

    with open(f"items/{dict_key}.txt", "w", encoding="utf-8") as file:
        file.write(f"{dict_key}:\n")
        for i in dictionary[dict_key]:
            line = " " * (len(dict_key) + 2)
            for key, value in i.items():
                line += f"{key}: {value}" + " " * (max_length - len(str(value))) + "   |"
            file.write(line + "\n")
