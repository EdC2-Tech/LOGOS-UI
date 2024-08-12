from ._anvil_designer import ActivityTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Activity(ActivityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Populate grid panel
    self.repeating_panel_1.items = anvil.server.call('get_activity')

    # Populate drop down panel
    panel = anvil.server.call('get_activity')
    self.edit_res_dropdown.items = {(row["Resource"]) for row in panel}

    self.repeating_panel_1.set_event_handler('x-refresh-dependencies', self.refresh_dependencies)
    # Any code you write here will run before the form opens.
  
  def refresh_dependencies(self, **event_args):
    self.repeating_panel_1.items = anvil.server.call('get_activity')
  
  def pg_size_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    rowPerPage = int(self.text_box_1.text) + 2
    if rowPerPage > 50:
      rowPerPage = 50
      
    self.data_grid_1.rows_per_page = rowPerPage

  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    activity_name        = self.edit_dep_val.text
    activity_description = self.edit_dep_des.text
    resource             = self.edit_res_dropdown.selected_value
    
    anvil.server.call('add_activity',
                      Task = activity_name,
                      Description = activity_description,
                      Resource = resource
                     )
    # refresh grid panel
    self.repeating_panel_1.items = anvil.server.call('get_activity')
    
    # clear after adding new row
    self.edit_dep_val.text = ''
    self.edit_dep_des.text = ''
    self.edit_res_dropdown.selected_value = self.edit_res_dropdown.items[0]
