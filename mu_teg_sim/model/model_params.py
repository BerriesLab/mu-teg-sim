import tkinter as tk
import numpy as np


class ModelParams:

    def __init__(self, root: tk.Tk):
        # A Tkinter root must be defined before instantiating the tk variables.
        if not isinstance(root, tk.Tk):
            return

        # {block name: {param name: [default value, current value, units, (min val, max val)],...}, ...}
        self.params = {
            "Physical Properties": {
                "a_p": self.Param(tk.DoubleVar(value=100e-6), tk.DoubleVar(), "V/K", (-np.inf, np.inf)),  # Seebeck coefficient of p-type leg
                "a_n": self.Param(tk.DoubleVar(value=-100e-6), tk.DoubleVar(), "V/K", (-np.inf, np.inf)),  # Seebeck coefficient of n-type leg
                "s_p": self.Param(tk.DoubleVar(value=1e5), tk.DoubleVar(), "S/m", (0, np.inf)),  # Electrical conductivity of p-type leg
                "s_n": self.Param(tk.DoubleVar(value=1e5), tk.DoubleVar(), "S/m", (0, np.inf)),  # Electrical conductivity of n-type leg
                "k_p": self.Param(tk.DoubleVar(value=1e0), tk.DoubleVar(), "W/(m•K)", (0, np.inf)),  # Thermal conductivity of p-type leg
                "k_n": self.Param(tk.DoubleVar(value=1e0), tk.DoubleVar(), "W/(m•K)", (0, np.inf)),  # Thermal conductivity of n-type leg
                "k_i": self.Param(tk.DoubleVar(value=1e-1), tk.DoubleVar(), "W/(m•K)", (0, np.inf)),  # Thermal conductivity of insulating volume
                "h_rh": self.Param(tk.DoubleVar(value=1e5), tk.DoubleVar(), "W/(m2•K)", (0, np.inf)),  # Thermal conductance of substrate - hot side
                "h_rc": self.Param(tk.DoubleVar(value=1e3), tk.DoubleVar(), "W/(m2•K)", (0, np.inf)),  # Thermal conductance of substrate - cold side
                "h_sh": self.Param(tk.DoubleVar(value=1e4), tk.DoubleVar(), "W/(m2•K)", (0, np.inf)),  # Thermal coupling with environment - hot side
                "h_sc": self.Param(tk.DoubleVar(value=1e4), tk.DoubleVar(), "W/(m2•K)", (0, np.inf))  # Thermal coupling with environment - cold side
            },
            "Device Design": {
                "area_p": self.Param(tk.DoubleVar(value=1e-8), tk.DoubleVar(), "m2", (1e-12, np.inf)),  # Area of p-type leg
                "area_n": self.Param(tk.DoubleVar(value=1e-8), tk.DoubleVar(), "m2", (1e-12, np.inf)),  # Area of n-type leg
                "teg_area": self.Param(tk.DoubleVar(value=25e-6), tk.DoubleVar(), "m2", (1e-12, np.inf)),  # Device area
                "ff": self.Param(tk.DoubleVar(value=0.5), tk.DoubleVar(), "", (1e-12, np.inf)),  # (A_p + A_n) / (A_p + A_n + A_i), where A_i is the area of the insulator
                "l_min": self.Param(tk.DoubleVar(value=1e-6), tk.DoubleVar(), "m", (1e-12, np.inf)),  # Minimum length of the thermoelectric legs
                "l_max": self.Param(tk.DoubleVar(value=1e-2), tk.DoubleVar(), "m", (1e-12, np.inf)),  # Maximum length of the thermoelectric legs
                "m": self.Param(tk.DoubleVar(value=1), tk.DoubleVar(), "", (0, np.inf)),  # Device resistance to load resistance ratio (optimal = 1)
                "t_rh": self.Param(tk.DoubleVar(value=305.0), tk.DoubleVar(), "K", (0, np.inf)),  # Temperature of the hot reservoir
                "t_rc": self.Param(tk.DoubleVar(value=300.0), tk.DoubleVar(), "K", (0, np.inf))  # Temperature of the cold reservoir
            },
            "Solver": {
                "n_steps": self.Param(tk.IntVar(value=1000), tk.IntVar(), "", (1, np.inf)),  # Number of steps between l_min and l_max
                "log_steps": self.Param(tk.BooleanVar(value=True), tk.BooleanVar(), "", (0, 1)),  # False: lin spaced. True: log spaced
                "n_iter": self.Param(tk.IntVar(value=0), tk.IntVar(), "", (0, np.inf)),  # Number of max iterations. If 0: 100*(N+1) where N is the number of variables.
                "x_tol": self.Param(tk.DoubleVar(value=1.49012e-8), tk.DoubleVar(), "", (0, np.inf))
                # Calculation terminates if the relative error between two iterations <=`x_tol`
            },
            "Initial Conditions": {
                "q_h": self.Param(tk.DoubleVar(value=1), tk.DoubleVar(), "W/m2", (0, np.inf)),
                "t_sh": self.Param(tk.DoubleVar(value=305.0), tk.DoubleVar(), "K", (0, np.inf)),
                "t_s": self.Param(tk.DoubleVar(value=303.0), tk.DoubleVar(), "K", (0, np.inf)),
                "t_c": self.Param(tk.DoubleVar(value=302.0), tk.DoubleVar(), "K", (0, np.inf)),
                "t_sc": self.Param(tk.DoubleVar(value=300.0), tk.DoubleVar(), "K", (0, np.inf)),
                "q_c": self.Param(tk.DoubleVar(value=1), tk.DoubleVar(), "W/m2", (0, np.inf))
            }
        }
        self.init_current_values()

    def init_current_values(self):
        """ Set current values to default values. """
        for block in self.params.keys():
            for param in self.params[block].keys():
                self.params[block][param].reset()

    def convert_params_to_json_compatible_format(self):
        """ Convert self.params to .json compatible format. Note: drop all parameters attributes except 'current value' """
        params_to_convert = {}
        for block in self.params.keys():
            params_to_convert[block] = {}
            for param in self.params[block].keys():
                params_to_convert[block][param] = self.params[block][param].current_value.get()
        return params_to_convert

    def validate_params(self):
        """ Validate all parameters. """
        for block in self.params.keys():
            for param in self.params[block].keys():
                if not self.params[block][param].validate():
                    return False

    class Param:
        """ A class for parameters."""

        def __init__(self, default_value, current_value, units, interval):
            self._default_value = default_value
            self.current_value = current_value
            self._units = units
            self._interval = interval

        def set_current_value(self, value):
            """ Set current value. Return Error if value is of wrong type. """
            try:
                self.current_value.set(value=value)
                return True
            except tk.TclError:
                return False

        def get_default_value(self):
            """ Get default value. """
            return self._default_value

        def get_units(self):
            return self._units

        def get_interval(self):
            return self._interval

        def validate(self):
            """ Check if current value is of same type as default value, and if it falls within the parameter range. """
            try:
                self.current_value.get()
            except (ValueError, Exception):
                return False
            if self.get_interval()[0] <= self.current_value.get() <= self.get_interval()[1]:
                return True
            else:
                return False

        def reset(self):
            """ Reset current value to default value. """
            default_value = self._default_value.get()
            self.current_value.set(value=default_value)
