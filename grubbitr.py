from gi.repository import Gtk
from backend import read_grub, write_grub
import settings


class GrubbitrMainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Grubbitr")
        self.connect("delete-event", Gtk.main_quit)        

        self.create_os_view()
        self.create_buttons()
        self.bulk_attach()

       
    def create_os_view(self):
        self.os_names = [140 * " " for i in xrange(6)]
        self.os_list = Gtk.ListStore(str)
        for os_name in self.os_names: self.os_list.append([os_name])
        
        self.os_view = Gtk.TreeView(model=self.os_list)

        renderer_os_text = Gtk.CellRendererText()
        renderer_os_text.set_property("editable", True)
        renderer_os_text.connect("edited", self.rename)
        
        self.os_names_column = Gtk.TreeViewColumn("Operating Systems", 
                                                   renderer_os_text, text=0)
        self.os_view.append_column(self.os_names_column)
    
        # Allows multiple rows to be selected.
        self.selection = self.os_view.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.BROWSE)
    
    def create_buttons(self):
        # Read grub.cfg button.
        self.read_button = Gtk.Button(label="Read grub.cfg")
        self.read_button.connect("clicked", self.read_button_click)
        # Write grub.cfg button.
        self.write_button = Gtk.Button(label="Save Changes")
        self.write_button.connect("clicked", self.write_button_click)
            
        # Switch Buttons
        self.up_switch_button = Gtk.Button(label="Move Up")
        self.up_switch_button.connect("clicked", self.switch_up)
        self.down_switch_button = Gtk.Button(label="Move Down")
        self.down_switch_button.connect("clicked", self.switch_down)

   
        # Cancel Button
        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", Gtk.main_quit)

    def set_default_spacing(self):
        # Maximum margins for Grid.

        self.grid.set_property("row_spacing", 10)
        self.grid.set_margin_left(50)
        self.grid.set_margin_top(20)

        # Settings for buttons
        # Write button
        self.write_button.set_margin_top(60)
        self.write_button.set_margin_right(10)
        self.cancel_button.set_margin_top(60)
        self.cancel_button.set_margin_left(10)
        #up and down switches

        self.up_switch_button.set_margin_left(30)
        self.down_switch_button.set_margin_left(30)

    def bulk_attach(self):
        # Placing everything in a self.grid.
        self.grid = Gtk.Grid()
        self.grid.attach(self.read_button, 0, 0, 2, 1)
        self.grid.attach(self.os_view, 0, 1, 2, 4)
        
        self.grid.attach(self.write_button, 0, 6, 1, 1)
        self.grid.attach(self.cancel_button, 1, 6, 1, 1)    
        self.add(self.grid)

        self.grid.attach(self.up_switch_button, 5, 2, 1, 1)
        self.grid.attach(self.down_switch_button, 5, 3, 1, 1)
   
         
        self.set_default_spacing()

    def read_button_click(self, widget):
        # A quick clear to ensure no funny behaviour if 
        # the button is pressed multiple times.

        if len(self.os_list) != 0:
            self.os_list.clear()
            self.os_names = []
            self.os_lines = []
            self.os_dictionary = {}

        os_token = read_grub.get_full_info(settings.grub_directory + "grub.cfg")
        self.os_lines, self.os_names, self.os_dictionary = os_token

        # Updating self.os_view to display changes.
        for os_name in self.os_names: self.os_list.append([os_name])

    def rename(self, widget, path, text):
        old_name = self.os_list[path][0]
        self.os_list[path][0] = text
        self.os_names[int(path)] = text 
        # For some reason, path is a string of the index, not ana int.

        self.os_dictionary[text] = self.os_dictionary.pop(old_name)
        self.os_dictionary[text].change_name(text)
         
    def write_button_click(self, widget):
        # Whether to overwrite grub.cfg or not.
        if settings.grub_overwrite:
            file_name = "grub.cfg"
        elif not settings.grub_overwrite:
            file_name = "test.cfg"

        write_grub.write_to_file(self.os_lines, self.os_names,
                 self.os_dictionary, settings.grub_directory + file_name)

    def switch_up(self, widget):
        currently_selected = self.selection.get_selected_rows()
        current_path = currently_selected[1][0]
        
        # To see if it's already at the top.
        if str(current_path) != "0":
            # Get iterator objects, and find above position.
            above_path = int(str(current_path)) - 1
            above_iter = self.os_list.get_iter(above_path) 
            current_iter = self.os_list.get_iter(current_path)

            # Swaps the positions with the Gtk.Iter objects as indices.
            self.os_list.swap(current_iter, above_iter)
            # These objects can only be converted first to strings,
            # then to integers.
            i, j = int(str(current_path)), int(str(above_path)) 
            self.os_names[i], self.os_names[j] = self.os_names[j], self.os_names[i]

        else:
            print "At Top."

    def switch_down(self, widget):
        currently_selected = self.selection.get_selected_rows()
        current_path = currently_selected[1][0]

        bottom_position = str(len(self.os_names) - 1)
        
        if str(current_path) != bottom_position:
            below_path = int(str(current_path)) + 1
            below_iter = self.os_list.get_iter(below_path)
            current_iter = self.os_list.get_iter(current_path)

            self.os_list.swap(current_iter, below_iter)
            i, j = int(str(current_path)), int(str(below_path))
            self.os_names[i], self.os_names[j] = self.os_names[j], self.os_names[i]

        else:
            print "At Bottom."
    
if __name__ == "__main__":
    main_window = GrubbitrMainWindow()
    main_window.show_all()
    Gtk.main()
