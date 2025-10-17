import tkinter as tk
import tkinter.filedialog as filedialog
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mu_teg_sim.model.model import Model


class SimulationFrame(tk.Frame):
    """ A class for Simulation Frame with Buttons and Figure widgets. """

    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.main_frame = main_frame
        self._create_layout()
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.95)

    def _create_layout(self):
        """ Create layout by placing buttons and figure. """
        self._build_simulation_buttons()
        self._build_simulation_figure()

    def _build_simulation_buttons(self):
        """ Create and place buttons.
        Note, all buttons and check buttons are placed in a new frame, which is then placed in the 'Simulation Frame'. """
        btn_frame = tk.Frame(self, pady=5)
        # Add buttons
        tk.Button(master=btn_frame, text="Run", command=self._event_button_run).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Button(master=btn_frame, text="Save", command=self._event_button_save).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Button(master=btn_frame, text="Clear", command=self._event_button_clear).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        # Add Tkinter variable attributes
        self.check_buttons = {"n": tk.BooleanVar(value=False),
                              "p": tk.BooleanVar(value=True),
                              "e": tk.BooleanVar(value=True),
                              "r": tk.BooleanVar(value=False),
                              "v": tk.BooleanVar(value=False),
                              "i_sc": tk.BooleanVar(value=False),
                              "i_cc": tk.BooleanVar(value=False),}
        # Add check buttons
        tk.Checkbutton(master=btn_frame, text="Normalize", variable=self.check_buttons["n"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="Power", variable=self.check_buttons["p"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="Efficiency", variable=self.check_buttons["e"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="Resistance", variable=self.check_buttons["r"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="VOC", variable=self.check_buttons["v"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="SSC", variable=self.check_buttons["i_sc"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Checkbutton(master=btn_frame, text="CSC", variable=self.check_buttons["i_cc"], command=self._update_figure).pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        btn_frame.pack()

    def _build_simulation_figure(self):
        """ Create and place figure.
        Note: widgets are placed in a new frame, which is then placed in the 'Simulation Frame' """
        # Create figure and its attributes
        fig_frame = tk.Frame(self)
        self.fig = matplotlib.figure.Figure()
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.ax.set_xlabel("Length (m)")
        self.fig.tight_layout()
        self.lines = {"p": self.ax.plot([], [], label=r"Power ($\mathrm{W/m^{2}}$)")[0],
                      "e": self.ax.plot([], [], label="Efficiency")[0],
                      "r": self.ax.plot([], [], label=r"Resistance ($\mathrm{\Omega/m^2}$)")[0],
                      "v": self.ax.plot([], [], label=r"VOC ($\mathrm{V/m^{2}}$)")[0],
                      "i_sc": self.ax.plot([], [], label=r"SSC ($\mathrm{A/m^{2}}$)")[0],
                      "i_cc": self.ax.plot([], [], label=r"CSC ($\mathrm{A/m^{2}}$)")[0]}
        self._update_figure()
        # Add check buttons to toggle between LogX/LinX and LogY/LinY
        self.check_logx = tk.BooleanVar(value=False)
        self.check_logy = tk.BooleanVar(value=False)
        tk.Checkbutton(master=fig_frame, text="LogX", variable=self.check_logx, command=self._event_check_button_logx).pack(side=tk.LEFT, expand=False, fill=tk.Y)
        tk.Checkbutton(master=fig_frame, text="LogY", variable=self.check_logy, command=self._event_check_button_logy).pack(side=tk.LEFT, expand=False, fill=tk.Y)
        fig_frame.pack(expand=True, fill=tk.BOTH)

    def _event_button_run(self):
        """ Handles button 'Run' event: validate params, run simulation and plot results. """
        self.main_frame.model_params.validate_params()
        self.model = Model(params=self.main_frame.model_params.convert_params_to_json_compatible_format())
        solution, msg = self.model.solve()
        if solution is True:
            self._update_figure()
        else:
            self._event_button_clear()
        self.main_frame.frame_status_bar.text.set(msg)

    def _event_button_save(self):
        """ Handles button 'Save' event: save data to disc in txt format. """
        # Check if the simulation has been executed, i.e. if the attribute model exists
        if not hasattr(self, "model"):
            self.main_frame.frame_status_bar.text.set(value=f"Cannot save: must run model first.")
            return
        # Open file dialog window
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            self.main_frame.frame_status_bar.text.set(value=f"Attention! Data not saved.")
            return
        # Save data
        data_to_save = np.column_stack((self.model.l, self.model.p, self.model.e, self.model.r, self.model.v,
                                        self.model.i_sc, self.model.i_cc))
        header = ("Length, Power, Efficiency, Resistance, Open Circuit Voltage, Short Circuit Current, Closed Circuit Current\n"
                  "m, W/m2, #, Ohm/m2, V/m2, A/m2, A/m2")
        try:
            np.savetxt(file_path, data_to_save, header=header, comments='', fmt='%.6e')
        except Exception:
            self.main_frame.frame_status_bar.text.set(value=f"Attention! Data not saved.")
            return
        self.main_frame.frame_status_bar.text.set(value=f"Data saved to {file_path}.")

    def _event_button_clear(self):
        """ Clear figure. This re-initialize Model. """
        # Check if the simulation has been executed, i.e. if the attribute model exists
        if not hasattr(self, "model"):
            return
        self.__delattr__("model")
        self._set_lines_to_default_values()
        self._update_figure()

    def _set_lines_to_default_values(self):
        for line in self.lines.keys():
            self.lines[line].set_data([], [])

    def _update_figure(self):
        """ Update figure. """
        # Check if the simulation has been executed, i.e. if the attribute model exists
        if not hasattr(self, "model"):
            for line in self.lines.keys():
                self.lines[line].set_visible(self.check_buttons[line].get())
            self._update_legend()
            self.canvas.draw()
            return

        # Set lines data and redraw canvas
        self._set_lines()
        self._update_legend()
        self._autoscale()
        self.canvas.draw()

    def _set_lines(self):
        """ Set lines data and visibility"""
        for line in self.lines.keys():
            if self.check_buttons["n"].get():
                self.lines[line].set_data(self.model.l, getattr(self.model, line) / max(getattr(self.model, line)))
            else:
                self.lines[line].set_data(self.model.l, getattr(self.model, line))
            self.lines[line].set_visible(self.check_buttons[line].get())

    def _update_legend(self):
        """ Update legend including only visible lines. Note: lines to show are chosen depending on the check buttons value."""
        lines = self.ax.get_lines()
        visible_lines = [line for line in lines if line.get_visible()]
        labels = [line.get_label() for line in visible_lines]
        self.ax.legend(visible_lines, labels)

    def _autoscale(self):
        """Autoscale the plot taking into account only visible lines and lines with data."""
        self.ax.relim()
        visible_lines = [line for line in self.ax.get_lines() if line.get_visible() and line.get_data()]
        if visible_lines:
            data = np.concatenate([line.get_data()[1] for line in visible_lines])
            self.ax.set_ylim(data.min(), data.max())
        else:
            self.ax.set_ylim(0, 1)
        self.ax.autoscale_view()

    def _event_check_button_logx(self):
        """ Toggle x-axis scale. """
        if self.check_logx.get():
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')
        self._update_figure()

    def _event_check_button_logy(self):
        """ Toggle y-axis scale. """
        if self.check_logy.get():
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')
        self._update_figure()
