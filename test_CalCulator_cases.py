
import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{repo_basename}')))


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{safe_repo_name}')))
# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import pytest
from unittest.mock import MagicMock, patch

# Mock tkinter widgets
class MockCTkWidget:
    def __init__(self, *args, **kwargs):
        self._children = []
        self.configure = MagicMock()
        self.pack = MagicMock()
        self.pack_propagate = MagicMock()
        self.destroy = MagicMock()
        self.delete = MagicMock()
        self.insert = MagicMock()
        self.get = MagicMock(return_value="")
        self.winfo_children = MagicMock(return_value=[])
        self.mark_set = MagicMock()
        self.update_idletasks = MagicMock()
        self.update = MagicMock()
        self.focus_set = MagicMock()
        self.focus_get = MagicMock(return_value=None)
        self.focus_next = MagicMock()
        self.focus_prev = MagicMock()
        self.get_children = MagicMock(return_value=[])
        self.configure = MagicMock()

class MockCTkFrame(MockCTkWidget):
    pass

class MockCTkLabel(MockCTkWidget):
    pass

class MockCTkButton(MockCTkWidget):
    pass

class MockCTkEntry(MockCTkWidget):
    pass

class MockCTkTextbox(MockCTkWidget):
    pass

class MockCTkComboBox(MockCTkWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set = MagicMock()
        self.get = MagicMock(return_value="[select]")

class MockCTkFont:
    def __init__(self, *args, **kwargs):
        pass

class MockCTk:
    def __init__(self, *args, **kwargs):
        self.geometry = MagicMock()
        self.title = MagicMock()
        self.mainloop = MagicMock()
        self.CTkLabel = MockCTkLabel
        self.CTkFrame = MockCTkFrame
        self.CTkButton = MockCTkButton
        self.CTkEntry = MockCTkEntry
        self.CTkTextbox = MockCTkTextbox
        self.CTkComboBox = MockCTkComboBox
        self.CTkFont = MockCTkFont
        self.set_appearance_mode = MagicMock()
        self.CTk = MockCTkWidget # For root itself

# Mock the modules used in the calculator code
class MockCalculator:
    def calculate(self, expr, conditions):
        if expr == "2+2":
            return "4"
        elif expr == "error":
            return None
        return "mock_result"

    def post_clean(self, expr):
        return expr

class MockVector:
    def vector_calc(self, oper, a, b=None):
        if oper == 'add':
            return "[3, 5]"
        elif oper == 'dot':
            return "10"
        return "mock_vector_result"

class MockGraph:
    def graph(self, expr):
        pass # Mocking the plotting function

class MockSolverAI:
    def generate(self, problem):
        return "Mock AI Answer"

# Patching the imports
@patch('customtkinter', MagicMock())
@patch('calculator', MockCalculator())
@patch('vector', MockVector())
@patch('graph', MockGraph())
@patch('solver_ai', MockSolverAI())
@patch('ctk', MagicMock())
def test_calc_page_clear_button():
    """Tests if the clear button clears all entry fields."""
    mock_ctk = MagicMock()
    mock_ctk.CTk = MockCTk
    mock_ctk.CTkEntry = MockCTkEntry
    mock_ctk.CTkLabel = MockCTkLabel
    mock_ctk.CTkFrame = MockCTkFrame
    mock_ctk.CTkButton = MockCTkButton
    mock_ctk.CTkFont = MockCTkFont
    mock_ctk.END = "END"

    with patch('customtkinter', mock_ctk):
        from calculator_app import calc_page, main_frame, wrt, lim, integral_l, integral_r, sum_i, sum_n, entrybox

        # Mock the entry widgets
        wrt.delete = MagicMock()
        lim.delete = MagicMock()
        integral_l.delete = MagicMock()
        integral_r.delete = MagicMock()
        sum_i.delete = MagicMock()
        sum_n.delete = MagicMock()
        entrybox.delete = MagicMock()

        calc_page()
        # Simulate clicking the clear button
        click_button_mock = MagicMock()
        click_button_mock('clear')

        assert wrt.delete.called
        assert lim.delete.called
        assert integral_l.delete.called
        assert integral_r.delete.called
        assert sum_i.delete.called
        assert sum_n.delete.called
        assert entrybox.delete.called

@patch('customtkinter', MagicMock())
@patch('calculator', MockCalculator())
@patch('vector', MockVector())
@patch('graph', MockGraph())
@patch('solver_ai', MockSolverAI())
@patch('ctk', MagicMock())
def test_calc_page_calculate_button_valid_input():
    """Tests if the calculate button handles valid input correctly."""
    mock_ctk = MagicMock()
    mock_ctk.CTk = MockCTk
    mock_ctk.CTkEntry = MockCTkEntry
    mock_ctk.CTkLabel = MockCTkLabel
    mock_ctk.CTkFrame = MockCTkFrame
    mock_ctk.CTkButton = MockCTkButton
    mock_ctk.CTkFont = MockCTkFont
    mock_ctk.END = "END"

    with patch('customtkinter', mock_ctk):
        from calculator_app import calc_page, main_frame, entrybox, wrt, lim, integral_l, integral_r, sum_i, sum_n
        from calculator import calculate

        # Mock the entry widgets and the calculate function
        entrybox.get = MagicMock(return_value="2+2")
        entrybox.delete = MagicMock()
        entrybox.insert = MagicMock()
        wrt.get = MagicMock(return_value="")
        lim.get = MagicMock(return_value="")
        integral_l.get = MagicMock(return_value="")
        integral_r.get = MagicMock(return_value="")
        sum_i.get = MagicMock(return_value="")
        sum_n.get = MagicMock(return_value="")

        calc_page()
        # Simulate clicking the calculate button
        click_button_mock = MagicMock()
        click_button_mock('calculate')

        assert entrybox.delete.called
        assert entrybox.insert.called_with("0", "4")

@patch('customtkinter', MagicMock())
@patch('calculator', MockCalculator())
@patch('vector', MockVector())
@patch('graph', MockGraph())
@patch('solver_ai', MockSolverAI())
@patch('ctk', MagicMock())
def test_calc_page_calculate_button_error_input():
    """Tests if the calculate button handles error input correctly."""
    mock_ctk = MagicMock()
    mock_ctk.CTk = MockCTk
    mock_ctk.CTkEntry = MockCTkEntry
    mock_ctk.CTkLabel = MockCTkLabel
    mock_ctk.CTkFrame = MockCTkFrame
    mock_ctk.CTkButton = MockCTkButton
    mock_ctk.CTkFont = MockCTkFont
    mock_ctk.END = "END"

    with patch('customtkinter', mock_ctk):
        from calculator_app import calc_page, main_frame, entrybox, wrt, lim, integral_l, integral_r, sum_i, sum_n
        from calculator import calculate

        # Mock the entry widgets and the calculate function to return None
        entrybox.get = MagicMock(return_value="error")
        entrybox.delete = MagicMock()
        entrybox.insert = MagicMock()
        wrt.get = MagicMock(return_value="")
        lim.get = MagicMock(return_value="")
        integral_l.get = MagicMock(return_value="")
        integral_r.get = MagicMock(return_value="")
        sum_i.get = MagicMock(return_value="")
        sum_n.get = MagicMock(return_value="")

        # Mock calculate to return None for error case
        with patch('calculator.calculate', return_value=None) as mock_calculate:
            calc_page()
            # Simulate clicking the calculate button
            click_button_mock = MagicMock()
            click_button_mock('calculate')

            assert entrybox.delete.called
            assert entrybox.insert.called_with("0", "ERROR")