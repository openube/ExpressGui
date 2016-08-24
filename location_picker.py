import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread


class Selector:
    server_selected = None

    def __init__(self, express):
        self.express = express
        if self.express.current_server != None:
            self.server_selected = self.express.current_server
        elif self.express.last_server != None:
            self.server_selected = self.express.last_server

    def get_server_text(self):
        return self.server_selected.country + " - " + self.server_selected.location


class CountryComboBox(Gtk.ComboBoxText):

    def __init__(self, express, selector, location_box):
        Gtk.ComboBoxText.__init__(self)
        self.connect("changed", self.country_change)
        self.express = express
        self.selector = selector
        self.location_box = location_box
        self.get_countries()
        self.update_selection()
        self.location_box.update()

    def get_countries(self):
        for item, country in enumerate(self.express.servers['countries']):
            self.append_text(country)
            
    def update_selection(self):
        for item in range(len(self.get_model())):
            if self.get_model()[item][0] in self.selector.server_selected.country:
                self.set_active(item)

    def country_change(self, widget):
        self.selector.server_selected.country = self.get_active_text()
        self.location_box.update()


class LocationComboBox(Gtk.ComboBoxText):

    def __init__(self, express, selector):
        Gtk.ComboBoxText.__init__(self)
        self.connect("changed", self.location_change)
        self.express = express
        self.selector = selector

    def location_change(self, test):
        self.selector.server_selected = self.express.servers[
            self.selector.server_selected.country][self.get_active()]

    def update(self):
        self.get_model().clear()
        country = self.selector.server_selected.country
        for item, server in enumerate(self.express.servers[country]):
            self.append_text(server.location)
            if server.location in self.selector.server_selected.location:
                self.set_active(item)
                self.location_change(self)

class ChangeServerButton(Gtk.Button):

    def __init__(self, express, selector, update_parent):
        Gtk.Button.__init__(self, label="Change Server")
        self.connect("clicked", self.change_server)
        self.selector = selector
        self.express = express
        self.update_parent = update_parent

    def disconnect_connect(self):
        self.express.disconnect()
        self.update_parent()
        connect_thread = Thread(target=self.connectionss)
        connect_thread.start()

    def connectionss(self):
        self.express.connect(self.server)
        self.update_parent()

    def change_server(self, widget):
        self.server = self.selector.server_selected
        status = self.express.connection_status
        if status is False:
            self.express.connect(self.server)
            self.update_parent()
        elif status is True and self.express.current_server.location != self.server.location:
            print("Changing server to " + self.server.location)
            disconnect_thread = Thread(target=self.disconnect_connect)
            disconnect_thread.start()


class RefreshButton(Gtk.Button):

    def __init__(self, express):
        self.express = express
        Gtk.Button.__init__(self, label="Refresh")
        self.connect("clicked", self.refresh)

    def refresh(self, widget):
        self.express.refresh()


class LocationPicker(Gtk.Window):

    def __init__(self, express, selector, update_parent):
        Gtk.Window.__init__(self, title="Choose a server")
        self.update_parent = update_parent  # Updates the label and switch
        self.express = express
        self.selector = selector
        self.create_widgets()
        self.add_widgets()

    def create_widgets(self):
        self.locations_combobox = LocationComboBox(self.express, self.selector)
        self.countries_combobox = CountryComboBox(
            self.express, self.selector, self.locations_combobox)
        self.connect_button = ChangeServerButton(
            self.express, self.selector, self.update_parent)
        self.refresh_button = RefreshButton(self.express)

    def add_widgets(self):
        box = Gtk.VBox(False, 0)
        box.add(self.countries_combobox)
        box.add(self.locations_combobox)
        box.add(self.connect_button)
        box.add(self.refresh_button)
        self.add(box)