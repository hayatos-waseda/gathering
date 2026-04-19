# environment/field_view.py

class FieldView:
    def __init__(self, field):
        self._field = field

    def get_pos_status(self, x, y, act=None):
        return self._field.get_pos_status(x, y, act)

    def get_event(self, x, y):
        return self._field.get_event(x, y)

    def is_path(self, x, y):
        return self._field.is_path(x, y)
    
    @property
    def grid_size(self):
        return self._field.grid_size