# mu-teg-sim
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12802052.svg)](https://doi.org/10.5281/zenodo.12802052)

An app to simulate the device physics of micro Thermoelectric Generators (μTEGs), based on the work by **D. Beretta et
al.**, Sustainable Energy Fuels, 2017, 1, 174-190. The app calculates the power generated, the efficiency of conversion,
the electrical resistance, the open circuit voltage, the short circuit 
current and the closed circuit current per unit area, given the device
design and the physical properties of materials.

This app is designed for scientists, researchers, and engineers who want to simulate the device physics of μTEGs, to
analyze performance metrics and optimize designs for various applications. By providing a user-friendly GUI and robust
computational tools, this app facilitates the study and development of energy conversion technologies using μTEGs.

## Table of Contents

* [Installation](#installation)
* [How to use](#how-to-use)
    * [Main window](#main-window)
    * [Parameters Tabs](#parameters-tabs)
    * [Solver](#solver)
    * [Saving and loading](#saving-and-loading)
* [Contributing](#contributing)
* [Credits](#credits)
* [License](#license)

## Installation

The `mu-teg-sim` app can be installed either via pip or by cloning the repository.

To install the app via pip, use the following commands based on your operating system:

- **On Unix/Mac**: Open a terminal and run:
  ```bash 
  pip install mu-teg-sim
- **On Windows**: Open Command Prompt or PowerShell and run:
  ```bash
  pip install mu-teg-sim

To install the app by cloning the repository to your local machine, follow these steps:

- Clone the repository:
  ```bash
  git clone https://github.com/BerriesLab/mu-teg-sim.git
- Navigate to the project directory:
  ```bash
  cd project-name
- Install the required dependencies:
  ```bash
  pip install -r requirements.txt

## How to use

The app is based on the device physics described in **D. Beretta et al.**, Sustainable Energy Fuels, 2017, 1,
174-190. Readers are encouraged to consult the manuscript to understand the meaning of the parameters and equations
referenced in this application.

### Launching the GUI from terminal
The app can be launched from terminal after installation by typing 
```bash 
mu_teg_sim
``` 

### Main window

<div id="fig_gui" align="center">
    <img src="images/gui_overview.png" alt="" width="700">
    <p><b>Figure 1:</b> GUI main window.</p>
</div>

The main window of the app consists of three primary frames:

- **Input Frame**: This frame allows users to enter the parameters to run the model. Refer to
  the [Parameters Tabs](#Parameters-Tabs) section for information on data types and accepted value intervals. The input
  frame includes the following buttons:
    - **Reset**: Resets all parameters to their default values.
    - **Save Params**: Saves the current set of parameters to a file in .json format.
    - **Load Params**: Loads parameters from a .json file on disk. Note: the parameters are loaded only if the file and
      all parameters it contains pass a validation check on data type and range.


- **Simulation Frame**: This frame is used to run simulations and display results. It includes the following buttons
  and check buttons:
    - **Run**: Starts the simulation. Results are shown in a figure within this frame.
    - **Clear**: Removes the current figure and results.
    - **Save**: Saves the results of the current simulation to a .txt file, which includes the power generated, the
      conversion efficiency, the resistance, the open circuit voltage, and the short circuit current as a function of
      the thermocouple length, per unit area.
    - **Normalize**: Normalizes the results with respect to their maximum value, allowing all results to be shown
      simultaneously in the same figure.
    - **Power**: Shows or hides the power per unit area vs. length.
    - **Efficiency**: Shows or hides the efficiency vs. length.
    - **Resistance**: Shows or hides the device resistance per unit area vs. length.
    - **VOC**: Shows or hides the open circuit voltage per unit area vs. length.
    - **SCC**: Shows or hides the short circuit current per unit area vs. length.
    - **CSC**: Shows or hides the closed circuit current per unit area vs. 
      length.
    - **LogX**: Switches the x-axis between linear and logarithmic scales.
    - **LogY**: Switches the y-axis between linear and logarithmic scales.


- **Status Bar Frame**: Provides real-time updates and status information, including errors or alerts related to the
  simulation, loading, and saving of files.

### Parameters Tabs

<div id="fig_params" align="center"> 
    <img src="images/gui_params.png" alt="" width="400">
    <p><b>Figure 2:</b> Parameter tabs.</p>
</div>

The parameters in the Input Frame are organized into two tabs. Each parameter has a specific data type (float, int, or
boolean) and is restricted to a particular range. If an invalid value is entered, the background of the entry field
turns red, and the simulation cannot be executed. The following tables list the parameters along with their
descriptions, units, data types, default values, and valid ranges.

Tab 1 - **Model Params**: Physical Properties

| Parameter | Description                           | Units    | Type  | Default Value | Valid Values |
|-----------|---------------------------------------|----------|-------|---------------|--------------|
| a_p       | Seebeck coefficient of p-type         | V/K      | float | 100e-6        | [-∞, ∞]      |
| a_n       | Seebeck coefficient of n-type         | V/K      | float | -100e-6       | [-∞, ∞]      |
| s_p       | Electrical conductivity of p-type leg | S/m      | float | 1e5           | [0, ∞]       |
| s_n       | Electrical conductivity of n-type leg | S/m      | float | 1e5           | [0, ∞]       |
| k_p       | Thermal conductivity of p-type leg    | W/(m·K)  | float | 1             | [0, ∞]       |
| k_n       | Thermal conductivity of n-type leg    | W/(m·K)  | float | 1             | [0, ∞]       |
| k_i       | Thermal conductivity of insulator     | W/(m·K)  | float | 0.1           | [0, ∞]       |
| h_rh      | Thermal conductance of hot reservoir  | W/(m²·K) | float | 1e5           | [0, ∞]       |
| h_rc      | Thermal conductance of hot substrate  | W/(m²·K) | float | 1e3           | [0, ∞]       |
| h_sh      | Thermal conductance of cold substrate | W/(m²·K) | float | 1e4           | [0, ∞]       |
| h_sc      | Thermal conductance of cold reservoir | W/(m²·K) | float | 1e4           | [0, ∞]       |

Tab 1 - **Model Params**: Device Design

| Parameter | Description                                    | Units | Type  | Default Value | Valid Values  |
|-----------|------------------------------------------------|-------|-------|---------------|---------------|
| area_p    | Area of p-type leg                             | m²    | float | 1e-8          | [1e-12, ∞]    |
| area_n    | Area of n-type leg                             | m²    | float | 1e-8          | [1e-12, ∞]    |
| teg_area  | Device area                                    | m²    | float | 25e-6         | [1e-12, ∞]    |
| ff        | (area_p + area_n) / (area_p + area_n + area_i) |       | float | 0.5           | [1e-12, ∞]    |
| l_min     | Minimum length of the thermoelectric legs      | m     | float | 1e-6          | [1e-12, ∞]    |
| l_max     | Maximum length of the thermoelectric legs      | m     | float | 1e-2          | [0, ∞]        |
| m         | Device to load resistance ratio (optimal = 1)  |       | float | 1             | [0, ∞]        |
| t_rh      | Temperature of the hot reservoir               | K     | float | 305           | [0, ∞]        |
| t_rc      | Temperature of the cold reservoir              | K     | float | 300           | [0, ∞]        |

Tab 2 - **Simulation Params**: Solver

| Parameter | Description                         | Units | Type  | Default Value | Valid Values  |
|-----------|-------------------------------------|-------|-------|---------------|---------------|
| n_steps   | Number of steps in the simulation   |       | int   | 1000          | [1, ∞]        |
| log_steps | Use logarithmic scaling for steps   |       | bool  | True          | [True, False] |
| n_iter    | Number of iterations for the solver |       | int   | 0             | [0, ∞]        |
| x_tol     | Solver tolerance                    |       | float | 1.49012e-8    | [0, ∞]        |

Tab 2 - **Simulation Params**: Initial Conditions

| Parameter | Description                                                                   | Units | Type  | Default Value | Valid Values |
|-----------|-------------------------------------------------------------------------------|-------|-------|---------------|--------------|
| q_h       | Heat flux absorbed from the hot reservoir                                     | W/m²  | float | 1.0           | [0, ∞]       |
| t_sh      | Temperature between the hot reservoir and the hot substrate                   | K     | float | 305.0         | [0, ∞]       |
| t_h       | Temperature between the hot side of the thermocouples and the hot reservoir   | K     | float | 303.0         | [0, ∞]       |
| t_c       | Temperature between the cold side of the thermocouples and the cold reservoir | K     | float | 302.0         | [0, ∞]       |
| t_sc      | Temperature between the cold reservoir and the cold substrate                 | K     | float | 300.0         | [0, ∞]       |
| q_c       | Heat flux released to the cold reservoir                                      | W/m²  | float | 1.0           | [0, ∞]       |

### Solver

<div id="fig_eq" align="center">
    <img src="images/gui_eq.png" alt="" width="500">
    <p><b>Figure 3:</b> System of non-linear equations to solve.</p>
</div>

The model is formulated as a parametric optimization problem, resulting in the system of non-linear equations shown in
in [Figure 3](#fig_eq). The solver uses the finite difference method for numerical differentiation and employs SciPy's
fsolve to solve the system of equations, utilizing the initial conditions provided by the user. Note that fsolve is a
local solver, which means it finds solutions based on the initial guess provided. Therefore, choosing appropriate
initial conditions is crucial to ensure that the solver converges to a correct and meaningful solution. If the initial
guess is not close to the true solution, the solver may get trapped in local minima or fail to find a solution.

For example, it is good practice to choose the initial conditions on the temperatures such that t_rh >= t_sh >= t_h >=
t_c >= t_sc >= t_sc, and to set the initial conditions on the heat flux such that q_h = h_rh * (t_rh - t_sh) and q_c =
h_rc * (t_sc - t_rc). Following these conventions can help in achieving a more accurate and stable solution.

Please note that the heat transfer coefficients of the reservoirs, namely h_rh and h_rc, depend on their temperatures
and might include contributions from conduction, convection, and radiation. Details on the calculation of these
coefficients can be found in the ESI of **D. Beretta et al.**, Sustainable Energy Fuels, 2017, 1, 174-190.

### Saving and loading

The **Save Params** button saves the model parameters to disk in .json format. Similarly, the **Load Params**
button loads a .json file containing previously saved parameters.

The structure of the file to be loaded must adhere to the format shown below, which includes the default values for the
parameters. A template file is available
at [model_params_template.json](docs/model_params_template.json) for users to edit as needed.
Please note that all values are saved in SI units.

```json
{
  "Physical Properties": {
    "a_p": 100e-6,
    "a_n": -100e-6,
    "s_p": 1e5,
    "s_n": 1e5,
    "k_p": 1e0,
    "k_n": 1e0,
    "k_i": 1e-1,
    "h_rh": 1e5,
    "h_rc": 1e3,
    "h_sh": 1e4,
    "h_sc": 1e4
  },
  "Device Design": {
    "area_p": 1e-08,
    "area_n": 1e-08,
    "teg_area": 25e-6,
    "ff": 0.5,
    "l_min": 1e-6,
    "l_max": 1e-2,
    "m": 1.0,
    "t_rh": 305.0,
    "t_rc": 300.0
  },
  "Solver": {
    "n_steps": 1000,
    "log_steps": true,
    "n_iter": 0,
    "x_tol": 1.49012e-08
  },
  "Initial Conditions": {
    "q_h": 1.0,
    "t_sh": 305.0,
    "t_s": 303.0,
    "t_c": 302.0,
    "t_sc": 300.0,
    "q_c": 1.0
  }
}
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull
requests.

## Credits

This app has been developed by **D. Beretta**, building on the work by **D. Beretta et al.**, Sustainable Energy Fuels,
2017, 1, 174-190. Please refer to [CREDITS.md](CREDITS.md) and [CITATION.md](CITATION.cff) for more details.

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.
