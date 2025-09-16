import os
cur_folder = os.path.dirname(os.path.abspath(__file__))
print(cur_folder)
rpg_system_root_folder = os.path.join(cur_folder, 'systems')
print(rpg_system_root_folder)
print("Welcome to the Rpg Character sheet generator.")
system_list = []

for item in os.listdir(rpg_system_root_folder):
  system_list.append(item.split('.')[0])

print('Here is the list of available systems:')
for system in system_list:
  print(f"{system_list.index(system) + 1}- {system.replace("_", " ").capitalize()}")

selected_system_index = int(input("Please select the desired system by typing it's correspondent number: "))

while (selected_system_index < 0) or (selected_system_index > len(system_list)):
  selected_system_index = int(input("Invalid option. Please select the desired system by typing it's correspondent number: "))

selected_system = system_list[selected_system_index - 1]
print(f'Selected system: {selected_system.replace("_", " ").capitalize()}')

rpg_system_folder = os.path.join(rpg_system_root_folder, selected_system)
element_list = []

for item in os.listdir(rpg_system_folder):
  element_list.append(item.split('.')[0])
