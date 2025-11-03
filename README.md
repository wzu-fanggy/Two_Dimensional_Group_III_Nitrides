# Two_Dimensional_Group_III_Nitrides
Machine Learning Potentials for Property Predictions of Two-Dimensional Group-III Nitrides

# Machine Learning Potentials for Property Predictions of Two-Dimensional Group-III Nitrides  


## Project Introduction  
This project focuses on the development of machine learning potentials for **two-dimensional (2D) group-III nitrides** (e.g., AlN, BN, GaN, InN) using the DeepMD method. Four potentials are fitted, and these potentials are further utilized to predict and simulate key physical properties, including phonon spectra and other material characteristics.  


## Folder Structure  
| Folder Name               | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `aimd`                    | Directory for ab initio molecular dynamics (AIMD) simulation files          |
| `data`                    | Stores data for model training and testing                                 |
| `model`                   | Contains trained machine learning potential models                          |
| `modelTrain`              | Holds scripts and configuration files for model training, freezing, and compression |
| `phonon`                  | Includes input files and scripts for phonon spectrum calculations           |
| `python_script`           | Auxiliary Python scripts for data processing and analysis                  |
| `result`                  | Stores simulation results (e.g., property data, visualization outputs)      |
| `strain`                  | Files related to strain-dependent property simulations                      |
| `structure`               | Atomic structure files (e.g., POSCAR) of 2D group-III nitrides              |
| `thermal_conductivity`    | Files for thermal conductivity simulation                                  |  


## Usage Instructions  

### 1. Train, Freeze, Compress, and Test Machine Learning Potentials (Taking AlN as an Example)  
```bash
# Train the model
dp train input.json

# Freeze the model (generate frozen graph)
dp freeze -o graph.pb

# Compress the model
dp compress -i graph.pb -o AlNcompress.pb

# Test the model
dp test -m compress.pb -s /personal/B_Al_Ga_In_N/AlN/test_data/ -n 100 -d results
```  


### 2. Plot Phonon Spectra (Taking AlN as an Example)  
```bash
# Calculate phonon dynamical matrix using LAMMPS
phonolammps AlN_ph.in -c POSCAR --dim 5 5 1

# Generate and plot phonon band structure
phonopy -c POSCAR band.conf --dim="5 5 1" -p -s

# Export band structure data for further plotting
phonopy-bandplot --gnuplot band.yaml > band.txt
```  


### 3. Simulations of Other Properties  
Simulations for other material properties (e.g., mechanical, thermal) are performed using LAMMPS. Relevant input scripts and configuration files can be found in the corresponding directories.
