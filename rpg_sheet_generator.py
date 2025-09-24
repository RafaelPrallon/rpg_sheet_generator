from menus import Menu
import os, csv

def add_attr(system_folder, attribute):
  if os.path.isfile(os.path.join(system_folder, f"{attribute}.csv")):
    stat_list = open_file({},os.path.join(system_folder,f"{attribute}.csv"),attribute)
    return set_att(stat_list)
  elif os.path.isdir(os.path.join(system_folder, attribute)):
    print("implementing")
  else:
    return input(f"Please type your character's {attribute}: ")

def set_att(stat_list):
  print("Now you will set the following characteristics")
  for stat in stat_list:
    print(f"-{stat['attribute'].replace("_", " ").capitalize()}")
  

    
def open_file(attr,file,attr_name):
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
        attr = csv.DictReader(f)
        for row in attr:
          print(row)
    except Exception as e:
      print(e)
      print(f"Rules file not found. Please add a {attr_name} file and try again")
      exit()
  else:
    print("Variable type not supported")
    exit()
  return attr

cur_folder = os.path.dirname(os.path.abspath(__file__))
print(cur_folder)
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
print(element_list)

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
print('Thanks for using the Rpg Character sheet generator.')