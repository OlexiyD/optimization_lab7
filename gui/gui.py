import sys
import numpy as np
from sympy import lambdify
import colorama
from tkinter import *
import customtkinter
from pymoo.decomposition.asf import ASF
import core.core as core
import gui.helper as hp
import gui.table as tb

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

        # Layout configuration
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Optimization Problem", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, columnspan=6, padx=20, pady=10, sticky="wne")

        # Variables, objectives and constrains count
        self.var_label = customtkinter.CTkLabel(self, text="Number of variables:", font=customtkinter.CTkFont(size=16))
        self.var_label.grid(row=1, column=0, rowspan=1, padx=(10, 0), pady=(0, 10), sticky="wne")

        self.obj_label = customtkinter.CTkLabel(self, text="Number of objectives (min):", font=customtkinter.CTkFont(size=16))
        self.obj_label.grid(row=1, column=1, rowspan=1, padx=(10, 0), pady=(0, 10), sticky="wne")

        self.constr_label = customtkinter.CTkLabel(self, text="Number of constrains (le):", font=customtkinter.CTkFont(size=16))
        self.constr_label.grid(row=1, column=2, rowspan=1, padx=(10, 10), pady=(0, 10), sticky="wne")

        # Input fields
        self.var_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.var_entry.grid(row=2, column=0, rowspan=1, padx=(10, 0), pady=(0, 10), sticky="wne")
        self.var_entry.bind("<Return>", self.var_cnt_changed)

        self.obj_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.obj_entry.grid(row=2, column=1, rowspan=1, padx=(10, 0), pady=(0, 10), sticky="wne")
        self.obj_entry.bind("<Return>", self.obj_cnt_changed)

        self.constr_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.constr_entry.grid(row=2, column=2, rowspan=1, padx=(10, 10), pady=(0, 10), sticky="wne")
        self.constr_entry.bind("<Return>", self.constr_cnt_changed)

        # Input tables
        var_columns = ("var", "xl", "xu")
        self.var_table = tb.TableView(self, columns=var_columns, show="headings", height=6)
        self.var_table.grid(row=3, column=0, padx=(10, 0), pady=(0, 10), sticky="wnse")

        self.var_table.column("var", anchor=CENTER, stretch=NO, width=40)
        self.var_table.column("xl", anchor=CENTER, width=80)
        self.var_table.column("xu", anchor=CENTER, width=80)

        self.var_table.heading("var", text='Var')
        self.var_table.heading("xl", text='Lower lim')
        self.var_table.heading("xu", text='Higher lim')

        obj_columns = ("obj", "equation", "weight")
        self.obj_table = tb.TableView(self, columns=obj_columns, show="headings", height=6)
        self.obj_table.grid(row=3, column=1, padx=(10, 0), pady=(0, 10), sticky="wnse")

        self.obj_table.column("obj", anchor=CENTER, stretch=NO, width=65)
        self.obj_table.column("equation", anchor=CENTER, width=50)
        self.obj_table.column("weight", anchor=CENTER, stretch=NO, width=50)

        self.obj_table.heading("obj", text='Objective')
        self.obj_table.heading("equation", text='Function')
        self.obj_table.heading("weight", text='Weight')

        constr_columns = ("constr", "equation")
        self.constr_table = tb.TableView(self, columns=constr_columns, show="headings", height=6)
        self.constr_table.grid(row=3, column=2, padx=(10, 10), pady=(0, 10), sticky="wnse")

        self.constr_table.column("constr", anchor=CENTER, stretch=NO, width=60)
        self.constr_table.column("equation", anchor=CENTER, width=50)

        self.constr_table.heading("constr", text='Constrain')
        self.constr_table.heading("equation", text='Function')


    def var_cnt_changed(self, event):       
        # Initialize appropriate number of rows
        self.fill_table(self.var_table, "x", int(self.var_entry.get()))

    def obj_cnt_changed(self, event):
        # Initialize appropriate number of rows
        self.fill_table(self.obj_table, "f", int(self.obj_entry.get()))
        pass

    def constr_cnt_changed(self, event):
        # Initialize appropriate number of rows
        self.fill_table(self.constr_table, "g", int(self.constr_entry.get()))
        pass

    def fill_table(self, table: tb.TableView, var_name: str, cnt: int):
        # Clear current table andd adds empty rows
        for item in table.get_children():
           table.delete(item)

        for i in range(cnt):
            table.insert('', END, iid = i, values = [f"{var_name}{i}", "", ""])

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
                                                   fg_color="#343638", text_color="#c7cfda", corner_radius=10, anchor="nw")
        self.result_label.grid(row=1, column=0, rowspan=5, padx=10, pady=0, sticky="wsne")

        self.solve_button = customtkinter.CTkButton(self, text="Optimize", command=self.button_callbck)
        self.solve_button.grid(row=6, column=0, rowspan=1, padx=30, pady=10, sticky="wsne")

    def button_callbck(self):
        # Lock button
        self.solve_button.configure(state="disabled")

        try:
            # Report state
            self.result_label.configure(text=f"Calculation running")

            # Initialize problem variables
            problem_config = core.ProblemConfiguration()
            problem_config.n_var = int(self.master.problem_frame.var_entry.get())
            problem_config.n_obj = int(self.master.problem_frame.obj_entry.get())
            problem_config.n_ieq_constr = int(self.master.problem_frame.constr_entry.get())

            # Get limits from variable table
            tmp_xl_array = [0]*problem_config.n_var
            tmp_xu_array = [0]*problem_config.n_var
            vars_names = ['']*problem_config.n_var
            for row_idx in range(problem_config.n_var):
                row = self.master.problem_frame.var_table.item(row_idx, 'values')
                vars_names[row_idx] = str(row[0])
                tmp_xl_array[row_idx] = int(row[1])
                tmp_xu_array[row_idx] = int(row[2])

            problem_config.xl = np.array(tmp_xl_array)
            problem_config.xu = np.array(tmp_xu_array)

            # Get objectives TODO add weight
            tmp_obj_array = ['']*problem_config.n_obj
            tmp_weights_array = ['']*problem_config.n_obj
            for row_idx in range(problem_config.n_obj):
                row = self.master.problem_frame.obj_table.item(row_idx, 'values')
                tmp_obj_array[row_idx] = lambdify(vars_names, str(row[1]))
                tmp_weights_array[row_idx] = float(row[2])

            # Get constrains
            tmp_constr_array = ['']*problem_config.n_ieq_constr
            for row_idx in range(problem_config.n_ieq_constr):
                row = self.master.problem_frame.constr_table.item(row_idx, 'values')
                tmp_constr_array[row_idx] = lambdify(vars_names, str(row[1]))

            problem_config.objective_fcn = tmp_obj_array
            problem_config.constrains = tmp_constr_array


            algo_config = core.AlgorithmConfiguration()
            algo_config.algo_type = str(self.master.algorithm_frame.algo_sel.get())
            algo_config.n_obj = problem_config.n_obj
            algo_config.n_partitions = int(self.master.algorithm_frame.n_part_entry.get())
            algo_config.n_points = int(self.master.algorithm_frame.n_points_entry.get())
            algo_config.ref_dirs_type = str(self.master.algorithm_frame.ref_dirs.get())
            algo_config.pop_size = int(self.master.algorithm_frame.pop_size_entry.get())
            algo_config.eliminate_duplicates = (True) if (int(self.master.algorithm_frame.rem_duplicates.get())) else (False)

            opt_config = core.OptimizationConfiguration()
            opt_config.termination_n_gen = 60 # Hardcoded
            opt_config.save_history = False
            opt_config.verbose = False
            opt_config.weights = np.array(tmp_weights_array)

            # Instanciating object of problem class
            problem = core.Problem(problem_config)

            # Creating algorithm for optimization
            algorithm = core.init_algo(algo_config)

            # Creating termination criteria
            termination = core.get_termination("n_gen", opt_config.termination_n_gen)

            # Applying optimization (produces set of solutions)
            res = core.minimize(problem,
                       algorithm,
                       termination,
                       seed=1,
                       save_history=opt_config.save_history,
                       verbose=opt_config.verbose)
            
            # Storing solutions to variables
            X = res.X
            F = res.F

            # Normalization
            approx_ideal = F.min(axis=0)
            approx_nadir = F.max(axis=0)
            nF = (F - approx_ideal) / (approx_nadir - approx_ideal)

            # Selecting single solution based on weights
            weights = opt_config.weights
            decomp = ASF()
            idx = decomp.do(nF, 1/weights).argmin()       # index of selected solution
            
            self.result_label.configure(text=f"Best regarding ASF: \nidx = {idx}\nX = {X[idx]}\nF = {F[idx]}")

            # Visualizing
            core.visualize(problem, X, F, idx)
        
        except Exception as ex:
            print(f"{colorama.Fore.RED}{ex}")
        finally:
            self.solve_button.configure(state="normal")

class AlgorithmFrame(customtkinter.CTkFrame):
    """This class implements algorithm configuration

    Attributes:
        var (int):          N

    Methods:
        method:             N
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Algorithm configuration", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.frame_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="wne")

        # Controls
        algos = ["NSGA2", "U-NSGA-III", "CTAEA"]
        self.algo_sel = customtkinter.CTkComboBox(self, values=algos)
        self.algo_sel.grid(row=1, column=0, columnspan=1, padx=(20, 5), pady=(0, 10), sticky="wnes")

        ref_dirs = ["energy", "uniform"]
        self.ref_dirs = customtkinter.CTkComboBox(self, values=ref_dirs)
        self.ref_dirs.grid(row=1, column=1, columnspan=1, padx=(5, 20), pady=(0, 10), sticky="wnes")

        self.rem_duplicates = customtkinter.CTkCheckBox(self, text="Eliminate duplicates enable", onvalue=True, offvalue=False)
        self.rem_duplicates.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="wnes")

        self.pop_size_label = customtkinter.CTkLabel(self, text="Population size:", font=customtkinter.CTkFont(size=16))
        self.pop_size_label.grid(row=3, column=0, rowspan=1, padx=(20, 5), pady=(0, 10), sticky="wnes")
        self.pop_size_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.pop_size_entry.grid(row=3, column=1, rowspan=1, padx=(5, 20), pady=(0, 10), sticky="wnes")

        self.n_part_label = customtkinter.CTkLabel(self, text="Number of pertitions:", font=customtkinter.CTkFont(size=16))
        self.n_part_label.grid(row=4, column=0, rowspan=1, padx=(20, 5), pady=(0, 10), sticky="wnes")
        self.n_part_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.n_part_entry.grid(row=4, column=1, rowspan=1, padx=(5, 20), pady=(0, 10), sticky="wnes")

        self.n_offsprings_label = customtkinter.CTkLabel(self, text="Number of offsprings:", font=customtkinter.CTkFont(size=16))
        self.n_offsprings_label.grid(row=5, column=0, rowspan=1, padx=(20, 5), pady=(0, 10), sticky="wnes")
        self.n_offsprings_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.n_offsprings_entry.grid(row=5, column=1, rowspan=1, padx=(5, 20), pady=(0, 10), sticky="wnes")

        self.n_points_label = customtkinter.CTkLabel(self, text="Number of points:", font=customtkinter.CTkFont(size=16))
        self.n_points_label.grid(row=6, column=0, rowspan=1, padx=(20, 5), pady=(0, 10), sticky="wnes")
        self.n_points_entry = customtkinter.CTkEntry(self, font=customtkinter.CTkFont(size=16))
        self.n_points_entry.grid(row=6, column=1, rowspan=1, padx=(5, 20), pady=(0, 10), sticky="wnes")

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
        self.textbox = customtkinter.CTkTextbox(self, font=customtkinter.CTkFont(size=16), fg_color="#343638", text_color="#c7cfda")
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
        self.title("Multicriteria optimization demonstrator (MVP)")
        self.geometry("900x700")

        # Configure layout
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
        