from setuptools import setup, find_packages

setup(
    name="mu_teg_sim",
    version="1.0.1",
    author="Davide Beretta",
    author_email="mail.davide.beretta+github@gmail.com",
    description="An app to simulate the device physics of micro Thermoelectric Generators",
    long_description="An app to simulate the device physics of micro Thermoelectric Generators (μTEGs). "
                     "It calculates the power generated, the efficiency of conversion, the device resistance, "
                     "the open circuit voltage, the short circuit current and the closed circuit current per unit of "
                     "device area as a function of the thermocouple length. "
                     "This app is designed for scientists, researchers, and engineers who want to simulate the device physics of μTEGs, "
                     "to analyze performance metrics and optimize designs for various applications.",
    url="https://github.com/BerriesLab/mu-teg-sim",
    packages=find_packages(),
    keywords=["python", "thermoelectric", "physics"],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            "mu_teg_sim=mu_teg_sim.cli.cli:main",
        ]
    },
    include_package_data=False,
)
