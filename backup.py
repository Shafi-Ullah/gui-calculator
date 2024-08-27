from collections import OrderedDict
from decimal import Decimal, getcontext
from fractions import Fraction
import customtkinter as ctk
import re
import math
import copy

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# The first element of this tuple is the button text, while the second and third elements represent the row and column, respectively.
basic_button_position = [
    ("7", 0, 0),
    ("8", 0, 1),
    ("9", 0, 2),
    ("DEL", 0, 3),
    ("AC", 0, 4),
    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("\u00D7", 1, 3),
    ("\u00F7", 1, 4),
    ("1", 2, 0),
    ("2", 2, 1),
    ("3", 2, 2),
    ("+", 2, 3),
    ("-", 2, 4),
    ("0", 3, 0),
    (".", 3, 1),
    ("EXP", 3, 2),
    ("Ans", 3, 3),
    ("=", 3, 4),
]
# The tuple contains button text, row, column and  button width  (first, second, third, fourth element)
scientific_button_position = [
    ("CALC", 3, 0, 10),
    ("x", 3, 1, 10),
    ("x\u207B\u00B9", 3, 4, 10),
    ("\u221Bx", 4, 0, 11),
    ("x\u00b3", 3, 5, 10),
    ("\u221Ax", 4, 1, 10),
    ("x\u00b2", 4, 2, 10),
    ("^", 4, 3, 15),
    ("log", 4, 4, 10),
    ("ln", 4, 5, 11),
    ("sin\u207B\u00B9", 5, 0, 11),
    ("cos\u207B\u00B9", 5, 1, 11),
    ("tan\u207B\u00B9", 5, 2, 11),
    ("sin", 5, 3, 11),
    ("cos", 5, 4, 11),
    ("tan", 5, 5, 11),
    ("STO", 6, 0, 10),
    ("ENG", 6, 1, 10),
    ("(", 6, 2, 10),
    (")", 6, 3, 10),
    ("S\u21D4D", 6, 4, 10),
    ("y", 6, 5, 10),
]
# This dictionary contains tuples(value) where the first string is displayed to users, and the second string is used for calculations.
replace_element = {
    "\u00D7": ("\u00D7", "*"),
    "\u00F7": ("\u00F7", "/"),
    "sin": ("sin(", ("math.", "sin", "(math.radians", "(")),
    "cos": ("cos(", ("math.", "cos", "(math.radians", "(")),
    "tan": ("tan(", ("math.", "tan", "(math.radians", "(")),
    "sin\u207B\u00B9": ("sin\u207B\u00B9(", ("math.degrees(math.", "asin", "(")),
    "cos\u207B\u00B9": ("cos\u207B\u00B9(", ("math.degrees(math.", "acos", "(")),
    "tan\u207B\u00B9": ("tan\u207B\u00B9(", ("math.degrees(math.", "atan", "(")),
    "log": ("log(", ("math.log", "(")),
    "ln": ("ln(", ("math.log", "(")),
    "x\u207B\u00B9": ("\u207B\u00B9", ("**", "-1")),
    "x\u00b2": ("\u00b2", ("**", "2")),
    "x\u00b3": ("\u00b3", ("**", "3")),
    "\u221Ax": ("\u221A", ("self.root(0.5,")),
    "\u221Bx": ("\u221B", ("self.root((1/3),")),
    "EXP": ("×₁₀", "*10**"),
    "^": ("^", "**"),
}
trigonometry_name = ["sin", "cos", "tan"]
inverse_trigonometry_name = ["asin", "acos", "atan"]
# first value represent the shape, next two row and column and second next represent width and height and last one is columnspan.
controle_button_position = [
    ("\u25C0", 0, 0, 25, 40, 2),
    ("\u25B6", 0, 2, 25, 40, 2),
    ("\u25B4", 0, 1, 50, 25, 1),
    ("\u25BE", 1, 1, 50, 25, 1),
]
frame2_button2 = [
    ("ON", 0, 5, "white"),
    ("MENU SETUP", 0, 4, "yellow"),
    ("ALPHA", 0, 1, "pink"),
    ("SHIHT", 0, 0, "yellow"),
]


class calculator(ctk.CTk):
    def __init__(self):
        """
        This class represents a custom calculator application.

        It inherits from `customtkinter.CTk` and provides a graphical user interface
        (GUI) for performing mathematical calculations.

        Attributes:
            result_var (ctk.StringVar): Variable to show the result of calculations.
            equation_var (ctk.StringVar): Variable to show the current equation being entered.
            count_cursor_move (int): Tracks cursor movements in the equation display using some specific button.
            equation_list (list): List to store the components of the current equation and is also used to display the equation to the users..
            row_result_equation_list (list): Modified list for equation components used in calculation.
            result_equation_list (list): Fully modified list of equation components for evaluation.
            store_index_and_value (list): Stores indices and values for managing equation modifications.
            variable_value (dict): Dictionary to store variable values like X, Y, Ans.
            calc_boolean (bool): Flag indicating whether a calculation is ongoing.
        """
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        # Variables
        self.result_var = ctk.StringVar()
        self.equation_var = ctk.StringVar()

        self.count_cursor_move = 0
        #
        self.count_equal_button_click = 0

        #
        self.variable_index = 0
        self.global_result = None
        #

        self.equation_list = []
        #
        self.copy_equation_list = []
        self.copy_row_result_equation_list = []

        self.row_result_equation_list = []
        self.result_equation_list = []
        self.store_index_and_value = []

        self.variable_value = {}
        self.copy_variable_value = {}

        self.calc_boolean = False
        self.sto_boolean = False
        self.result_boolean = False
        # configure row and column.
        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Calling Function
        self.screen()
        self.normal_button()
        self.scientific_button()
        #
        # self.cursor_position = self.equation_display.index(ctk.INSERT)

    def cursor_incursion(self, cursor_position, text):
        """
        Move the cursor position in the equation display and set focus.

        Parameters:
        cursor_position (int): The current cursor position in the equation display.
        text (str): The text to be inserted at the cursor position.
        """
        self.equation_display.icursor(cursor_position + len(text))
        self.equation_display.focus_set()

    def place_element(self, cursor_position, new_text):
        """
        Insert `new_text` into `self.equation_var` at `cursor_position`.
        """
        previous_equation = self.equation_var.get()[:cursor_position]
        after_equation = self.equation_var.get()[cursor_position:]
        new_equation = previous_equation + new_text + after_equation
        self.equation_var.set(new_equation)

    def update_equation_list(self, index, text):
        """
        Update the equation lists with modified text.
        modified_text1: used for displaying to the user
        modified_text2: needed for calculation
        Args:
            index (int): Index to insert `text` into the equation lists.
            text (str): Text to insert and modify.

        Returns:
            str: Modified text to be inserted into UI.
        """
        modified_text = replace_element.get(text, text)
        modified_text1 = modified_text[0] if type(modified_text) == tuple else text
        modified_text2 = modified_text[-1] if type(modified_text) == tuple else text

        self.equation_list.insert(index, modified_text1)
        self.row_result_equation_list.insert(index, modified_text2)
        print("row equation list", self.row_result_equation_list)
        print("equation list", self.equation_list)
        return modified_text1

    def unpacked_any_list(self, list_: list, classinfo: type) -> list:
        unpacked_list = []
        for object_ in list_:
            if isinstance(object_, classinfo):
                # Unpack the tuple and add its elements to the list
                unpacked_list.extend(object_)
            else:
                # Add non-tuple elements directly to the list
                unpacked_list.append(object_)
        return unpacked_list

    def bracket_count(self, list_: list, index1: int, reverse=False) -> int:
        """
        Count brackets in `list_` starting from `index1`.

        Parameters:
        reverse (bool, optional): If True, count backwards. Defaults to False.

        Returns:
        int: The index where the matching bracket is found, or `index1` if no matching bracket is found.
        """
        bracket = 0
        return_ = False
        stopping_index = -1 if reverse else len(list_)
        step = -1 if reverse else 1
        for index2 in range(index1, stopping_index, step):
            if list_[index2] == "(":
                return_ = True
                bracket += 1
            elif list_[index2] == ")":
                bracket -= 1
                return_ = True
            if bracket == 0 and return_:
                return index2
        return index1

    def placed_essential_element(self) -> None:
        """
        Insert essential elements into the result equation list.

        This method iterates through a sorted dictionary of index-value pairs,
        inserting each value into `self.result_equation_list` at the specified index,
        adjusted by the increasing `add_index`.
        """
        add_index = 0
        sorted_dict = sorted(self.store_index_and_value)
        for index, value in sorted_dict:
            self.result_equation_list.insert(index + add_index, value)
            add_index += 1

    def entry_widget_scroll(self, entry_widget, len_text: int) -> None:
        """
        Scroll the entry widget based on cursor movement and text length.

        Parameters:
        entry_widget (ctk.CTkEntry): The entry widget to be scrolled.
        len_text (int): The length of the text in the entry widget.
        """
        print(entry_widget != self.focus_get())
        if entry_widget != self.focus_get():
            if self.count_cursor_move < 0:
                entry_widget.xview_scroll(-len_text, "units")
            else:
                entry_widget.xview_scroll(len_text, "units")

    def placed_bracket(self, list_: list, root=False) -> None:
        """
        Insert brackets into a list based on power and root conditions.

        This method iterates through the given list and inserts opening and closing
        brackets at appropriate positions to correctly format mathematical expressions.
        It handles both power (**) and root scenarios.

        Parameters:
        list_ (list): The list of elements to process.
        root (bool, optional):  If True, handle root expressions (forward brackets) only.
                                If False, handle power expressions (both forward and backward brackets).
                                Default is False.
        Returns:
        None
        """
        index = 0
        power = False if root else True
        root_list = ["self.root((1/3),", "self.root(0.5,"]
        while index < len(list_):
            element = list_[index]
            sign = ["**", "*10**"]
            if (element in sign and power) or (element in root_list and root):

                if root == False:

                    if list_[index - 1] == ")":
                        list_index = self.bracket_count(list_, index - 1, reverse=True)

                        match list_[list_index - 1]:
                            case "(math.radians":
                                list_index -= 3
                            case x if x in inverse_trigonometry_name:
                                list_index -= 2
                            case "math.log":
                                list_index -= 1
                    elif list_[index - 1] == "Ans":
                        list_index -= 1
                    else:
                        for for_index in range(index - 1, -1, -1):
                            element = list_[for_index]
                            # We consider "x" and  "y" as digits because they are replaced with digits.
                            if element.isdigit() or element in [
                                ".",
                                "-1",
                                "x",
                                "y",
                            ]:
                                list_index = for_index
                            else:
                                # In the next iteration, index1 concatenates a non-integer value; therefore, index1 is added by 1.
                                list_index = for_index + 1
                                break
                    list_.insert(list_index, "(")
                    index = index + 1

                if root:
                    copy_index = copy.deepcopy(index)
                if list_[index + 1] in root_list and root:

                    index = index + 1
                    while_element = list_[index]
                    while while_element in root_list:
                        index = index + 1
                        while_element = list_[index]
                    index = index - 1

                match list_[index + 1]:
                    # We add 4, 3, etc., to the index because the replace_element dictionary is designed that way.
                    case "math.":
                        closing_index = self.bracket_count(list_, index + 4)
                    case "math.degrees(math.":
                        closing_index = self.bracket_count(list_, index + 3)
                    case "math.log":
                        closing_index = self.bracket_count(list_, index + 2)
                    case "(":
                        closing_index = self.bracket_count(list_, index + 1)
                    case "Ans":
                        closing_index = index + 1
                    case _:
                        for for_index in range(index + 1, len(list_)):
                            element = list_[for_index]
                            if element.isdigit() or element in [
                                ".",
                                "-1",
                                "x",
                                "y",
                            ]:
                                closing_index = for_index

                            else:
                                # In the next iteration, index1 concatenates a non-integer value; therefore, index1 is subtracted by 1.
                                closing_index = for_index - 1
                                break
                if root:
                    index = copy_index
                list_.insert(closing_index + 1, ")")

            index = index + 1

    def insert_multiplication(self, list_: list, index: int, element: str) -> None:
        """
        Insert multiplication sign in the list at the specified index if necessary . It is common calculator feature.

        Parameters:
        list_ (list): The list containing elements.
        index (int): The index to insert the multiplication sign.
        element (str): The element to check for multiplication.

        Returns:
        list: The modified list with inserted multiplication sign.
        """
        if index != 0:
            permissble_element = [
                "self.root(0.5,",
                "self.root((1/3),",
                "math.degrees(math.",
                "math.",
                "math.log",
                "(",
                "x",
                "y",
            ]

            previous_element = list_[index - 1]
            if element in permissble_element:
                match previous_element:
                    case ")":
                        self.store_index_and_value.append((index, "*"))
                    case str_value if str_value.isdigit():
                        self.store_index_and_value.append((index, "*"))
                    case ".":
                        self.store_index_and_value.append((index, "*"))
                    case x if x in ["x", "y"]:
                        self.store_index_and_value.append((index, "*"))

    def screen(self):
        """
        Setup the calculator screen using customtkinter widgets.
        """
        self.display_frame = ctk.CTkFrame(self)
        self.equation_display = ctk.CTkEntry(
            self.display_frame,
            font=("Arial", 20),
            text_color="#C1C1C1",
            fg_color="#333633",
            bg_color="#333633",
            border_width=0,
            textvariable=self.equation_var,
        )
        self.result_label = ctk.CTkLabel(
            self.display_frame,
            text_color="#C1C1C1",
            font=("Arial", 20),
            textvariable=self.result_var,
            fg_color="#333633",
            anchor="ne",
        )
        self.display_frame.grid(row=0, column=0, sticky="nsew", pady=(2, 5))
        self.equation_display.grid(row=0, column=0, sticky="nsew", ipady=10)
        self.result_label.grid(row=1, column=0, sticky="nsew")

        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(1, weight=1)

    def normal_button(self):
        """
        Setup the normal calculator buttons for basic arithmetic operations.
        """
        button_frame1 = ctk.CTkFrame(self)
        button_frame1.grid(row=2, column=0, sticky="nsew")
        normal = ("Arial", 15, "normal")
        bold = ("Arial", 14, "bold")
        small_normal = ("Arial", 15, "normal")

        for num, row, column in basic_button_position:
            font = (
                bold
                if num in ["DEL", "AC"]
                else small_normal if num in ["EXP", "Ans"] else normal
            )
            button = ctk.CTkButton(
                button_frame1,
                text=num,
                font=font,
                # fg_color="#F5F5E6",
                fg_color="#FAFAF0",
                text_color="black",
                corner_radius=5,
                hover_color="lightblue",
            )
            if num == "=":
                button.configure(command=self.calculate_equation)
            elif num == "DEL":
                button.configure(command=self.DEL)
            elif num == "AC":
                button.configure(command=self.AC)
            else:
                button.configure(command=lambda b=button: self.update_display(b))

            button.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)

            button_frame1.grid_rowconfigure(row, weight=1)
            button_frame1.grid_columnconfigure(column, weight=1)

    def scientific_button(self):
        """
        Setup the scientific calculator buttons for advanced operations.
        """

        button_frame2 = ctk.CTkFrame(self)

        button_frame2.grid(row=1, column=0, sticky="nsew", pady=(3, 10))
        # frame2_inside_frame.grid(row=0, column=3, rowspan=3, padx=10, pady=(5, 0))

        for symbol, row, column, text_size in scientific_button_position:
            button = ctk.CTkButton(
                button_frame2,
                text=symbol,
                font=("Arial", text_size, "normal"),
                fg_color="#FAFAF0",
                text_color="black",
                corner_radius=5,
                hover_color="lightblue",
                width=50,
            )
            if symbol == "STO":
                button.configure(command=self.STO)
            elif symbol == "ENG":
                pass
            elif symbol == "S\u21D4D":
                button.configure(command=self.float_to_fraction)
            elif symbol == "CALC":
                button.configure(command=self.CALC)
            elif symbol in ["x", "y"]:
                button.configure(command=lambda b=button: self.variable(b))
            else:
                button.configure(command=lambda b=button: self.update_display(b))
            button.grid(row=row, column=column, sticky="nsew")
            # button_frame2.grid_rowconfigure(row, weight=1)
            button_frame2.grid_columnconfigure(column, weight=1)
        self.controle_button(button_frame2)

    def controle_button(self, frame):
        controle_button_frame1 = ctk.CTkFrame(frame, fg_color="#FAFAF0")
        controle_button_frame2 = ctk.CTkFrame(
            controle_button_frame1, fg_color="#FAFAF0"
        )

        controle_button_frame1.grid(
            row=2, column=2, rowspan=2, columnspan=2, padx=5, sticky="nsew"
        )
        # controle_button_frame2.grid(row=0, column=0, padx=(2, 10), pady=(2, 3))
        #  padx=10, pady=(5, 0)
        for text, row, column, width, height, rowspan in controle_button_position:

            button = ctk.CTkButton(
                controle_button_frame1,
                text=text,
                font=("Arial", 15, "normal"),
                # fg_color="#F5F5E6",
                fg_color="#FAFAF0",
                text_color="black",
                corner_radius=5,
                hover_color="lightblue",
                width=width,
                height=height,
            )
            button.grid(row=row, column=column, rowspan=rowspan, sticky="nsew")

            controle_button_frame1.grid_rowconfigure(row, weight=1)
            controle_button_frame1.grid_columnconfigure(column, weight=1)

        for name, row, column, color in frame2_button2:
            button = ctk.CTkButton(
                frame,
                text="",
                font=("Arial", 15, "normal"),
                # fg_color="#F5F5E6",
                fg_color="#FAFAF0",
                text_color="black",
                corner_radius=5,
                hover_color="lightblue",
                width=width,
                height=height,
            )
            button.grid(row=2, column=column)

    def additional_button(self, frame):
        left_frame = ctk.CTkFrame(frame)
        right_frame = ctk.CTkFrame(frame)
        left_frame.grid(row=2, column=0, columnspan=2)
        left_frame.grid(row=2, column=4, columnspan=2)

        for name, row, column, color in frame2_button2:
            frame_choice = left_frame if name in ["ALPHA", "SHIFT"] else right_frame
            button = ctk.CTkButton(
                frame_choice,
                text="",
                font=("Arial", 15, "normal"),
                # fg_color="#F5F5E6",
                fg_color="#FAFAF0",
                text_color="black",
                corner_radius=5,
                hover_color="lightblue",
            )
            button.grid(row=2, column=column, sticky="nsew")

    def update_display(self, widget: str) -> None:
        """
        Update the display when a button is clicked, modifying equation variables.

        Parameters:
        widget (str): The button name.
        """
        if self.calc_boolean and "= ?" in self.equation_var.get():
            self.equation_var.set("")

        if self.sto_boolean == True and widget.cget("text") not in ["x", "y"]:
            self.sto_boolean = False

        if self.result_boolean:
            self.AC()
        cursor_position = self.equation_display.index(ctk.INSERT)
        len_equation_list = len(self.equation_list)

        new_text = widget.cget("text")
        # It checks the cursor position to place the element according to the equation_list and cursore move using button
        index = len_equation_list + self.count_cursor_move
        modified_text = self.update_equation_list(index, new_text)

        # Place element according to the cursore position
        self.place_element(cursor_position, modified_text)

        self.cursor_incursion(cursor_position, modified_text)

        self.entry_widget_scroll(self.equation_display, len(modified_text))
        # Remove result when type any number.
        if len(self.result_var.get()) > 0:
            self.result_var.set("")

    def calculate_equation(self, calc=False) -> None:
        """
        Process and display the result of the current equation.

        This method performs a series of operations on `self.row_result_equation_list`
        to process the equation and display the result. It handles trigonometric functions,
        inserts necessary brackets, replaces variable values, and evaluates the final equation.
        If the equation is valid, it sets the result to `self.result_var` and updates the
        result label. Optionally, it logs the calculation to the history.

        Parameters:
        calc (bool, optional): If True, skips logging the calculation to history. Default is False.

        Returns:
        None
        """

        unpacked_list = self.unpacked_any_list(self.row_result_equation_list, tuple)

        self.result_equation_list = copy.deepcopy(unpacked_list)

        all_trigonometry_name = [*trigonometry_name, *inverse_trigonometry_name]

        self.placed_bracket(self.result_equation_list)

        for index, element in enumerate(self.result_equation_list):
            if element in all_trigonometry_name:
                self.trigonometry(self.result_equation_list, index, element)
            else:
                self.insert_multiplication(self.result_equation_list, index, element)

        self.placed_essential_element()
        self.placed_bracket(self.result_equation_list, root=True)
        self.replace_variable_value(self.result_equation_list)
        if "Ans" in self.result_equation_list:
            self.result_equation_list = self.Ans(self.result_equation_list)

        # Clear list value for each "=" button click .
        self.store_index_and_value.clear()

        # Make a string of this list
        self.result_equation_list = "".join(self.result_equation_list)
        print(self.result_equation_list)
        if self.result_equation_list != "":
            result = eval(self.result_equation_list)
            modified_result = self.show_result(result=result)
            if self.sto_boolean:
                return modified_result

        else:
            pass

    def show_result(self, result: float) -> None:
        self.calc_boolean = self.calc_boolean
        if self.calc_boolean == False:
            self.result_boolean = True
            result = f"{result:.13f}".rstrip("0").rstrip(".")
            self.result_var.set(result)
            self.result_label.update()
            # Writing Calculation to data base
            self.calculation_history(equation=self.equation_var.get(), result=result)
            self.global_result = result
            if self.sto_boolean:
                return result
        else:

            keys = list(self.variable_value.keys())
            var = keys[-self.variable_index]
            if self.count_equal_button_click == 0:
                self.result_var.set(f"{var} = {result:.13f}".rstrip("0").rstrip("."))
                self.result_label.update()
                self.focus()
                self.count_equal_button_click = 1

            elif self.count_equal_button_click == 1:
                self.equation_list.clear()
                self.row_result_equation_list.clear()
                self.result_var.set("")

                self.variable_index += 1
                self.variable_value[var] = str(result)
                self.set_variable_value(self.variable_index)
                self.count_equal_button_click = 0

            # len_variable_value_dict = len(self.variable_value)
            subtracted_len = len(self.variable_value) - self.variable_index

            if subtracted_len == 0 and self.count_equal_button_click == 0:
                self.calc_boolean = False
                self.variable_index = 0

                self.equation_list = self.copy_equation_list
                self.row_result_equation_list = self.copy_row_result_equation_list
                self.equation_var.set("".join(self.equation_list))
                self.calculate_equation()
                self.variable_value = self.copy_variable_value

    def move_cursor_position(self, widget):
        """
        Adjust the cursor position in the equation display based on the widget's text.

        Moves the cursor left (◀) or right (▶) within `self.equation_display` and updates
        `self.count_cursor_move`.

        Parameters:
        widget: The button widget triggering the cursor movement.

        Returns:
        None
        """
        cursor_position = self.equation_display.index(ctk.INSERT)
        button_text = widget.cget("text")
        text_length = len(self.equation_var.get())

        if button_text == "\u25C0" and cursor_position != 0:
            self.count_cursor_move -= 1
            cursor_position -= len(self.equation_list[self.count_cursor_move])
            self.cursor_incursion(cursor_position, "")

        elif button_text == "\u25B6" and cursor_position != text_length:
            cursor_position += len(self.equation_list[self.count_cursor_move])
            self.count_cursor_move += 1
            self.cursor_incursion(cursor_position, "")

    def DEL(self):
        """Delete the character at the current cursor position in the equation display."""
        cursor_position = self.equation_display.index(ctk.INSERT)
        if cursor_position > 0:
            pop_element = self.equation_list.pop(self.count_cursor_move - 1)
            self.row_result_equation_list.pop(self.count_cursor_move - 1)
            self.equation_var.set("".join(self.equation_list))
            self.equation_display.icursor(cursor_position - len(pop_element))

    def AC(self):
        """Clear the equation display and reset all stored variables."""

        self.equation_display.delete(0, "end")
        self.result_var.set("")
        self.equation_list.clear()
        self.row_result_equation_list.clear()
        self.store_index_and_value.clear()
        self.calc_boolean = False
        self.calc_boolean = False
        self.result_boolean = False
        self.global_result = None
        self.copy_equation_list.clear()
        self.variable_value.clear()

    def Ans(self, list_: list) -> None:
        """Retrieve the last calculated result from a file ('database.txt')."""

        with open("database.txt", "r", encoding="utf-8") as f:
            previous_equation = f.readlines()[-1]
            answer = previous_equation.split("=")[-1].strip()
        join_list = "~@~".join(list_)
        join_list = join_list.replace("Ans", str(answer))
        list_ = join_list.split("~@~")
        return list_

    def calculation_history(self, equation, result):
        """Record the calculation history to a file ('database.txt')."""

        with open("database.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{equation}={result}")

    def trigonometry(self, list_: list, index: int, element: str) -> None:
        """
        Handle trigonometric functions and their brackets in the list.

        Parameters:
        list_ (list): The list containing elements.
        index (int): The index of the trigonometric function.
        element (str): The trigonometric function.

        Returns:
        list: The modified list with handled trigonometric functions.
        """
        add_index = 2 if element in trigonometry_name else 1
        last_bracket_index = self.bracket_count(list_, index + add_index)
        # self.result_equation_list.insert(last_bracket_index + 1, ")")
        self.store_index_and_value.append((last_bracket_index + 1, ")"))

    def root(self, power: float, equation: float) -> float:
        """Calculate the root of the equation with specified power."""

        getcontext().prec = 50
        x, y = (1, 2) if power == 0.5 else (1, 3)
        return float(equation ** (Decimal(x) / Decimal(y)))

    def CALC(self):
        if self.calc_boolean == False:
            self.sto_boolean = False
            self.result_boolean = False  # because calc use more time
            equation = self.equation_var.get()
            if any(char in equation for char in ["x", "y"]):
                self.calc_boolean = True
                self.copy_variable_value = copy.deepcopy(self.variable_value)
                self.copy_equation_list = copy.deepcopy(self.equation_list)

                self.copy_row_result_equation_list = copy.deepcopy(
                    self.row_result_equation_list
                )

                self.equation_list.clear()
                self.row_result_equation_list.clear()
                self.result_var.set("")

                self.set_variable_value(self.variable_index)
                # self.count_equal_button_click = 1
            else:
                self.calculate_equation()
        else:

            pass

    def variable(self, widget: str) -> None:
        """Process the selection of a variable and update the display"""
        variable = widget.cget("text")

        if self.sto_boolean:
            result = self.calculate_equation()
            equation = self.equation_var.get()
            right_arrow = "\u21D2"
            self.write_variable_value(variable, result)
            # self.AC()
            self.equation_var.set(equation + f" {right_arrow}{variable.capitalize()}")
            self.result_var.set(f"{variable.capitalize()} = {result}")
            self.focus()
        else:
            self.update_display(widget)
            self.read_variable_value(variable)

    def read_variable_value(self, variable: str) -> None:
        """
        Retrieve and store the value associated with the given variable from 'variable data base.txt' and store that variable value in variable_value dictionary.

        Parameters:
        variable (str): The name of the variable to retrieve the value for.

        Returns:
        None
        """

        with open("variable data base.txt", "r", encoding="utf-8") as f:
            all_value = f.readlines()

            index = next(
                index for index, item in enumerate(all_value) if variable in item
            )
            value = all_value[index].strip().split("=")[-1]
            self.variable_value[variable] = str(value)
            print("read", self.variable_value)

    def write_variable_value(self, variable: str, new_value: str) -> None:
        with open("variable data base.txt", "r", encoding="utf-8") as f:
            values = f.readlines()

        index = next(index for index, item in enumerate(values) if variable in item)
        variable_value = values[index].strip().split("=")[-1]
        str_values = "@".join(list(map(str.strip, values)))

        list_values = str_values.replace(
            f"{variable}={variable_value}", f"{variable}={new_value}"
        ).split("@")

        with_new_line_list = list(map(lambda x: x + "\n", list_values))
        with open("variable data base.txt", "w", encoding="utf-8") as f:
            f.writelines(with_new_line_list)

    def replace_variable_value(self, list_: list) -> None:
        """
        Replace variables in the list with their corresponding values from `self.variable_value`.

        Iterates through the elements of the list and replaces any occurrence of a variable
        with its corresponding value from `self.variable_value`.
        """

        for variable, value in self.variable_value.items():
            for index in range(len(list_)):
                if list_[index] == variable:
                    list_[index] = value

    def set_variable_value(self, index: int) -> None:
        if index != len(self.variable_value):
            keys = list(self.variable_value.keys())
            variable = keys[index]
            self.equation_var.set(f"{variable} = ?")
            self.focus()

    def STO(self):
        if self.equation_var.get() != "" and self.calc_boolean == False:
            self.sto_boolean = True

    def float_to_fraction(self):
        result_var_str = self.result_var.get()
        if "/" not in result_var_str and result_var_str != "":
            fraction_representation = Fraction(self.global_result).limit_denominator(
                10000
            )
            # numerator = fraction_representation.numerator
            # denominator = fraction_representation.denominator
            self.result_var.set(f"{fraction_representation}")
            # self.result_var.set(f"{numerator}/{denominator}")
        elif result_var_str != "":
            # print("s" + self.result_var.get() + "hrvukvrukkvrvr")
            self.result_var.set(self.global_result)

    def ENG(self, widget):
        pass


if __name__ == "__main__":
    app = calculator()
    app.mainloop()
