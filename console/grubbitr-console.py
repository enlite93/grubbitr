### 
# Written by Viktor Chynarov, May 9- 2013
#
#
# A program to edit the grub.cfg file so you have nice
# operating systems listed.
import read_grub
import write_grub
import backend

def switch(temp_names):
	try:
		print "Which number would you like to move?"
		first_position = int(raw_input(" #: ")) - 1
		print "Which number would you like to swap with position {0}?".format(first_position + 1)

		second_position = int(raw_input(" #: ")) - 1

		temp_names = backend.switch(temp_names, first_position, second_position)
		return temp_names
	
	except:
		print "Incorrect values were entered!"
		return temp_names

def rename(temp_names, temp_dictionary):
	try:
		print "What position name would you like to change? "
		choice = int(raw_input("#: ")) - 1
		os_name = temp_names[choice] 
	
		print "What name would you like to change it to? "
		new_name = raw_input("New Name: ")
		temp_names, temp_dictionary = backend.rename(temp_names, temp_dictionary, os_name, new_name)
		return (temp_names, temp_dictionary)	
	
	except:
		print "Incorrect values were entered!"
		return (temp_names, temp_dictionary)

def prompt(modified_lines, os_names, os_dictionary, ):
	state = 1
	temp_names = os_names[:]
	temp_dictionary = os_dictionary.copy()

	while state == 1:

		print "\n"
		print "Your current OS arrangement is: \n"
		
		for position, os_name in enumerate(temp_names):
			print "{0} \t {1}".format(position + 1, os_name)
		
		print "\nYou can either 'save', 'quit', 'switch', or 'rename'"

		choice = raw_input("?: ")
		if choice == "quit": state = 0

		elif choice == "switch":
			temp_names = switch(temp_names)
	
		elif choice == "rename":
			temp_names, temp_dictionary = rename(temp_names, temp_dictionary)

		elif choice == "save":	
			print "What file would you like to save the new configuration to? (default=newgrub.cfg)"
			file_name = raw_input("File Name: ")
			if file_name == "": file_name = "newgrub.cfg"
			
			write_grub.write_to_file_wrapper(modified_lines, temp_names, temp_dictionary, file_name)
			state = 0

		else:
			continue

	return 

### End of writing and modifying function definitions.
os_token = read_grub.get_full_info()
os_names = os_token[0] 
os_dictionary = os_token[1]
modified_lines = os_token[2]

# Modified_lines contains no crud right now.
modified_lines = write_grub.create_clean_config(modified_lines)

if __name__ == "__main__":
	# User input to modify the file.
	prompt(modified_lines, os_names, os_dictionary)

