from ._anvil_designer import GroupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .AddGroup import AddGroup


class Group(GroupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.__update_table__()
    # Any code you write here will run before the form opens.

  def __update_table__(self):
    self.repeating_panel_1.items = get_open_form().group_table
    
  def add_resource_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    adding_form = AddGroup(item=self.item)
    result = alert(content=adding_form, large=True, buttons=[("Accept", True), ("Cancel", False)])
    
    if result:
      group_name        = adding_form.group_name.text
      group_description = adding_form.group_description.text
  
      app_tables.group_table.add_row(group_name = group_name, group_description=group_description)
      self.raise_event('x-refresh-tables')
      self.__update_table__()
      
    else:
      return