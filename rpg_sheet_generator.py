from menus import Menu
import os, csv, re

def add_attr(system_folder, attribute):
  if os.path.isfile(os.path.join(system_folder, f"{attribute}.csv")):
    stat_list = open_file({},os.path.join(system_folder,f"{attribute}.csv"),attribute)
    return set_att(stat_list)
  elif os.path.isdir(os.path.join(system_folder, attribute)):
    if attribute == 'classes':
      return select_classes(os.path.join(system_folder, 'classes'), rules[0])
    else:
      return select_option(os.path.join(system_folder, attribute), attribute)
  else:
    return input(f"Please type your character's {attribute}: ")

def set_att(stat_list):
  attributes = {}
  print("Now you will set the following characteristics:")
  distribution_method = stat_list[1]['value_distribution']
  if distribution_method == 'point_distribution':
    point_cost = stat_list[1]['point_cost']

  valid_values = dict(val.split('-') for val in stat_list[1]['valid_values'].split(';'))
  
  for stat in stat_list:
    print(f"-{stat['attribute'].replace("_", " ").capitalize()}")
  if distribution_method == 'value_list':
    print(f'You can select one of the following values for each attribute:')
    for key in valid_values.keys():
      valid_values[key] = int(valid_values[key])
      print(f'{key} that can be used {valid_values[key]} times.')
    for stat in stat_list:
      selected_val = ''
      while selected_val not in valid_values.keys() or (valid_values.get(selected_val,0) == 0):
        selected_val = input(f'Please type the desired value for {stat['attribute'].replace("_", " ").capitalize()}: ')
      attributes[stat['attribute']] = selected_val
      valid_values[selected_val] = valid_values[selected_val] - 1
  return attributes

def select_option(file_path, attr):
  option_list_path = os.path.join(file_path, 'list.txt')
  option_list = open_file([], option_list_path)
  print(f'Here is the list of available {attr}:')

  selected_option_index = Menu.number_menu_input(f"Please select the desired {attr} by typing it's correspondent number: ", system_list)

  selected_option = option_list[selected_option_index - 1]
  return selected_option

def select_classes(file_path, rules):
  starter_level = int(rules['starter_level'])
  class_list_path = os.path.join(file_path, 'list.txt')
  class_list = open_file([], class_list_path,'list')
  class_levels = {}
  for level in range(1, starter_level+1):
    selected_class_index = Menu.number_menu_input(f"Please select the desired class for level {level} by typing it's correspondent number: ", class_list)
    selected_class = class_list[selected_class_index - 1]
    if selected_class in class_levels:
      class_levels[selected_class] += 1
    else:
      class_levels[selected_class] = 1
    print(f'current levels: {class_levels}')
  return class_levels

def calc_bonus_att(file_path, character_classes):
  bonus_attr = {}
  for char_class in character_classes.keys():
    class_attr = open_file({}, os.path.join(file_path, f'{char_class}.csv'),'class attributes')[0]
    bonus_attr[class_attr['attr_name']] = bonus_attr.get(class_attr['attr_name'], 0) + int(class_attr['attr_bonus'])
  return bonus_attr


def calc_hp(rules, attributes):
  cal_formula = rules['health_calc']
  if attributes.get('stats'):
    pattern = r'\b(?:' + '|'.join(re.escape(attr) for attr in attributes['stats'].keys()) + r')\b'
    relevant_attribute = re.search(pattern, cal_formula).group(0)
    base_hp = eval(cal_formula.replace(relevant_attribute, re.findall(r'\d+',attributes['stats'][relevant_attribute])[0]))
  else:
    base_hp = 0
  bonus_hp = attributes.get('bonus_stats', {}).get('hp', 0)
  return base_hp + bonus_hp + sum(attributes.get('classes', {}).values())

def calc_mp(rules, attributes):
  cal_formula = rules['mana_calc']
  if attributes.get('stats'):
    pattern = r'\b(?:' + '|'.join(re.escape(attr) for attr in attributes['stats'].keys()) + r')\b'
    relevant_attribute = re.search(pattern, cal_formula).group(0)
    base_mp = eval(cal_formula.replace(relevant_attribute, re.findall(r'\d+',attributes['stats'][relevant_attribute])[0]))
  else:
    base_mp = 0
  bonus_mp = attributes.get('bonus_stats', {}).get('mp', 0)
  return base_mp + bonus_mp + sum(attributes.get('classes', {}).values())

      
def open_file(attr,file,attr_name: None):
  if isinstance(attr,list):
    try:
      with open(file,'r') as f:
        for line in f:
          if not line.strip():
            continue
          attr.append(line.strip())
    except Exception as e:
      print(f"File not found. Please add the {attr_name} file and try again")
      exit()
  elif isinstance(attr,dict):
    try:
      with open(file, 'r') as f:
        attr = list(csv.DictReader(f))
    except Exception as e:
      print(e)
      print(f"Rules file not found. Please add a {attr_name} file and try again")
      exit()
  else:
    print("Variable type not supported")
    exit()
  return attr

# def write_attr(attr):
#   print(f'Name: {attr['name']}')
#   print(f'HP: {attr['hp']}')
#   for keys in attr.keys():


cur_folder = os.path.dirname(os.path.abspath(__file__))
rpg_system_root_folder = os.path.join(cur_folder, 'systems')
print(rpg_system_root_folder)
print("Welcome to the Rpg Character sheet generator.")
system_list = []

for item in os.listdir(rpg_system_root_folder):
  system_list.append(item.split('.')[0])

print('Here is the list of available systems:')

selected_system_index = Menu.number_menu_input("Please select the desired system by typing it's correspondent number: ", system_list)

selected_system = system_list[selected_system_index - 1]
print(f'Selected system: {selected_system.replace("_", " ").capitalize()}')

rpg_system_folder = os.path.join(rpg_system_root_folder, selected_system)
attribute_file = os.path.join(rpg_system_folder,'attribute_list.txt')
attribute_list = open_file([],attribute_file,'attributes')

rules_file = 'systems/' + selected_system + '/rules.csv'
rules = open_file({}, rules_file,'rules')
character_attr = {} 
element_list = []
for item in os.listdir(rpg_system_folder):
  element_list.append(item.split('.')[0])

print('Now we need to set the following characteristics you need to check for your character.')
select_option_index = 0
while select_option_index != "q" and select_option_index != "Q":
  for attribute in attribute_list:
    print(f"{attribute_list.index(attribute) + 1}- {attribute.replace("_", " ").capitalize()}")
  select_option_index = input("Please select the characteristic to change, You can press r/R to review and q/Q to finish: ")
  if not select_option_index.isdigit() and select_option_index.capitalize() == 'R':
      print(character_attr)
  if not select_option_index.isdigit():
    continue
  while (int(select_option_index) < 0) or (int(select_option_index) > len(attribute_list)):
    select_option_index = input("Invalid option. Please select a valid number: ")
    if not select_option_index.isdigit():
      break
  attribute = attribute_list[int(select_option_index)-1]

  character_attr[attribute] = add_attr(rpg_system_folder, attribute)
  if character_attr.get('classes'):
    character_attr['bonus_stats'] = calc_bonus_att(os.path.join(rpg_system_folder, 'classes', 'attributes'), character_attr['classes'])
    # character_attr['class_skills'] = set_class_skills(os.path.join(rpg_system_folder, 'classes', 'skills'), character_attr['classes'])

  character_attr['hp'] = calc_hp(rules[0], character_attr)
  if rules[0].get('mana_calc', False):
    character_attr['mp'] = calc_mp(rules[0], character_attr)
print('Thanks for using the Rpg Character sheet generator.')