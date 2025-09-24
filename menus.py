class Menu:
  def number_menu_input(prompt, option_list):
    for option in option_list:
      print(f"{option_list.index(option) + 1}- {option.replace("_", " ").capitalize()}")
    selected_option = int(input(prompt))
    while (selected_option < 0) or (selected_option > len(option_list)):
      selected_option = int(input("Invalid option. Please select a valid number: "))
    return selected_option
  
  def menu_with_exit_clause(prompt, option_list):
    for option in option_list:
      print(f"{option_list.index(option) + 1}- {option.replace("_", " ").capitalize()}")
      selected_option = input(prompt)
      while (selected_option < 0) or (selected_option > len(option_list)):
        if isinstance(selected_option, str) and selected_option.capitalize() == "Q":
          return selected_option
        selected_option = int(input("Invalid option. Please select a valid number: "))

    