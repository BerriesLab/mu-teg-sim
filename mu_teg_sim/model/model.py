from scipy.optimize import fsolve
import numpy as np


class Model:
    """ A class to model the device physics of muTEGs. """

    def __init__(self, params: dict):
        """ Note: params' data structure is model_params.params """
        self.params = params

        # Add arrays attributes
        n = self.params["Solver"]["n_steps"]
        self.l = np.zeros(n, dtype=np.float32)  # Thermocouples length
        self.p = np.zeros(n, dtype=np.float32)  # Power output per unit area
        self.e = np.zeros(n, dtype=np.float32)  # Efficiency (independent of area)
        self.r = np.zeros(n, dtype=np.float32)  # Resistance per unit area
        self.v = np.zeros(n, dtype=np.float32)  # Open circuit voltage per unit area
        self.i_sc = np.zeros(n, dtype=np.float32)  # Short circuit current per unit area
        self.i_cc = np.zeros(n, dtype=np.float32)  # Closed circuit current per unit area

    @staticmethod
    def _system_of_equation(x, a_pn, rho_pn, k_pni, ff, m, l, t_rh, t_rc, h_rh, h_rc, h_sh, h_sc):
        """Note: x is a list of variables, all the following arguments are parameters"""
        # Unpack the variables
        q_h, t_sh, t_h, t_c, t_sc, q_c = x
        # Define the system of equations
        eq1 = q_h * (1 / h_rh) - (t_rh - t_sh)
        eq2 = q_h * (1 / h_sh) - (t_sh - t_h)
        eq3 = q_h - (ff * a_pn ** 2 * t_h / (rho_pn * (1 + m) * l) + k_pni / l) * (t_h - t_c) + ((ff * a_pn ** 2) / (2 * rho_pn * (1 + m) ** 2 * l)) * (t_h - t_c) ** 2
        eq4 = q_c - (ff * a_pn ** 2 * t_c / (rho_pn * (1 + m) * l) + k_pni / l) * (t_h - t_c) - ((ff * a_pn ** 2) / (2 * rho_pn * (1 + m) ** 2 * l)) * (t_h - t_c) ** 2
        eq5 = q_c * (1 / h_sc) - (t_c - t_sc)
        eq6 = q_c * (1 / h_rc) - (t_sc - t_rc)
        return [eq1, eq2, eq3, eq4, eq5, eq6]

    def solve(self):
        """ Note: equations must be cast in the form f(x, params) = 0.
        The solution is: the temperature profile t_sh, t_h, t_c and t_sc, and the heat flux at the boundaries q_h and q_c.
        The function returns [True, msg] if the solver converged, or [False, msg] if the solver does not converge."""
        # Unpack the parameters
        (a_p, a_n, s_p, s_n, k_p, k_n, k_i, h_rh, h_rc, h_sh, h_sc,  # Physical Properties
         area_p, area_n, teg_area, ff, l_min, l_max, m, t_rh, t_rc,  # Device Design
         n_steps, log_steps, n_iter, x_tol,  # Solver
         x00, x01, x02, x03, x04, x05) = (  # Initial Conditions
            self.flatten_parameters())

        # Create new variables for solver
        rho_p = 1 / s_p
        rho_n = 1 / s_n
        area_i = (area_p + area_n) / ff - (area_p + area_n)
        a_pn = a_p - a_n
        rho_pn = (rho_p / area_p + rho_n / area_n) * (area_p + area_n)
        k_pni = (k_p * area_p + k_n * area_n + k_i * area_i) / (area_p + area_n + area_i)
        n = 1 / (area_p + area_n + area_i)
        N = teg_area / (area_p + area_n + area_i)

        # Set length array
        if log_steps is True:
            self.l = np.logspace(np.log10(l_min), np.log10(l_max), n_steps)
        else:
            self.l = np.linspace(l_min, l_max, n_steps)

        # Solve system of equations for each length value
        x0 = np.array([x00, x01, x02, x03, x04, x05])
        for idx, l in enumerate(self.l):
            solution, info, ier, msg = fsolve(func=self._system_of_equation,
                                              x0=x0,
                                              args=(a_pn, rho_pn, k_pni, ff, m, l, t_rh, t_rc, h_rh, h_rc, h_sh, h_sc),
                                              xtol=x_tol,
                                              maxfev=n_iter,
                                              full_output=True)
            # Handle case when solution is not found
            if ier != 1:
                return False, f"Solver did not converge for l = {l}: {msg}"
            t_h = solution[2]
            t_c = solution[3]
            q_h = solution[0]
            # Define the resistance of one thermocouple: r_pn = r_pn(l)
            r_p = rho_p * l / area_p
            r_n = rho_n * l / area_n
            r_pn = r_p + r_n
            # Set attributes value
            self.p[idx] = ff * a_pn ** 2 / (rho_pn * l) * m / (1 + m) ** 2 * (t_h - t_c) ** 2
            self.e[idx] = self.p[idx] / q_h
            self.r[idx] = n * r_pn
            self.v[idx] = n * a_pn * (t_h - t_c)
            self.i_sc[idx] = ff * a_pn * (t_h - t_c) / (N * rho_pn * l)
            self.i_cc[idx] = self.i_sc[idx] * 1 / (1 + m)
        return True, f"Solver converged for all values of l."

    def flatten_parameters(self):
        """ Flatten parameters and returns a list. """
        p = []
        for block in self.params.keys():
            for param in self.params[block].keys():
                p.append(self.params[block][param])
        return p
