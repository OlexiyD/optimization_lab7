import sys
from tkinter import *
import customtkinter
import core.core as core
import gui.helper as hp

# TODO: remove. Link to tkinter site: https://customtkinter.tomschimansky.com/

class ProblemFrame(customtkinter.CTkFrame):
    """This class implements problem configuration

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Optimization Problem", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="wne")

        # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck2)
        # self.button.grid(row=1, column=0, padx=20, pady=20)

    # def button_callbck2(self):
    #     print("button clicked !!!!")

class SolutionFrame(customtkinter.CTkFrame):
    """This class implements solution output

    Attributes:
        var (int):          N

    Methods:
        button_callbck:     Optimize problem
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Solution", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="wne")

        self.result_label = customtkinter.CTkLabel(self, text="Solution", font=customtkinter.CTkFont(size=16), 
                                                   fg_color="grey", text_color="black", corner_radius=10, anchor="nw")
        self.result_label.grid(row=1, column=0, rowspan=5, padx=10, pady=0, sticky="wsne")

        self.solve_button = customtkinter.CTkButton(self, text="Optimize", command=self.button_callbck)
        self.solve_button.grid(row=6, column=0, rowspan=1, padx=30, pady=10, sticky="wsne")

        # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck2)
        # self.button.grid(row=1, column=0, padx=20, pady=20)

    def button_callbck(self):
        # TODO: call solver
        self.solve_button.configure(state="disabled")
        self.result_label.configure(text=f"Placeholder")
        self.solve_button.configure(state="normal")
        pass

class AlgorithmFrame(customtkinter.CTkFrame):
    """This class implements algorithm configuration

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Algorithm configuration", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="wne")

        # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck2)
        # self.button.grid(row=1, column=0, padx=20, pady=20)

    # def button_callbck2(self):
    #     print("button clicked !!!!")

class StatusFrame(customtkinter.CTkFrame):
    """This class implements output

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Status", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="wne")

        # Create textbox
        self.textbox = customtkinter.CTkTextbox(self, font=customtkinter.CTkFont(size=16), fg_color="grey")
        self.textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

class TopFrame(customtkinter.CTkFrame):
    """This class implements output

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # TODO: adjust colors
        self.help_button = customtkinter.CTkButton(self, text="Help", corner_radius=0, fg_color="#2b2b2b", command=self.help_button_callbck)
        self.help_button.grid(row=0, column=0, padx=0, pady=0, sticky="e")

        self.doc_button = customtkinter.CTkButton(self, text="Documentation", corner_radius=0, fg_color="#2b2b2b", command=self.doc_button_callbck)
        self.doc_button.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        self.about_button = customtkinter.CTkButton(self, text="About", corner_radius=0, fg_color="#2b2b2b", command=self.about_button_callbck)
        self.about_button.grid(row=0, column=2, padx=0, pady=0, sticky="e")

    def help_button_callbck(self):
        # TODO: link to documentation
        print("button clicked !!!!")

    def doc_button_callbck(self):
        # TODO: link to documentation
        print("button clicked !!!!")

    def about_button_callbck(self):
        # TODO: pop-up form with some info
        print("button clicked !!!!")

class GuiApp(customtkinter.CTk):
    """This class implements GUI

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """
    def __init__(self):
        super().__init__()
    
        # Configure color theme
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # Set name of programm and size
        self.title("Multicriteria optimization demonstrator")
        self.geometry("900x700")

        # Configure layout
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)


        # self.tab_view = MyTabView(master=self)
        # self.tab_view.grid(row=0, column=0, padx=20, pady=20)

        # Frames initialization
        self.top_row_frame = TopFrame(self, height=20, corner_radius=0)
        self.top_row_frame.grid(row=0, column=0, columnspan=5, padx=0, pady=0, sticky="ew")

        self.problem_frame = ProblemFrame(self)
        self.problem_frame.grid(row=1, column=0, rowspan=5, columnspan=3, padx=(10, 5), pady=(10, 5), sticky="nswe")

        self.algorithm_frame = AlgorithmFrame(self)
        self.algorithm_frame.grid(row=6, column=0, rowspan=1, columnspan=3, padx=(10, 5), pady=(5, 10), sticky="nswe")

        self.solution_frame = SolutionFrame(self)
        self.solution_frame.grid(row=1, column=3, rowspan=5, columnspan=2, padx=(5, 10), pady=(10, 5), sticky="nswe")

        self.status_frame = StatusFrame(self)
        self.status_frame.grid(row=6, column=3, rowspan=1, columnspan=2, padx=(5, 10), pady=(5, 10), sticky="nswe")

        # Redirect standart output to log box
        sys.stdout = hp.StdoutRedirector(self.status_frame.textbox)

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck)
        # self.button.grid(row=1, column=0, padx=20, pady=20)

    def button_callbck(self):
        print("\x1b[31mbutton clicked")
        