# PySCES
PySCES, **Py**thon code for Linearized **S**emi-**C**lassical Dynamics with On-the-fly **E**lectronic **S**tructure, is a highly parallelized code for ab initio nonadiabatic molecular dynamics using linearized semiclassical initial value representation (LSC-IVR). As of now, on-the-fly updates of electronic structure variables can be performed either by GPU-assisted electronic structure package, TeraChem, or, as its original implementation was structured, GAMESS. The code is intended for computing electronic population correlation functions through one of three population estimators: Wigner, semiclassical, or spin mapping population estimator. See the following references for the original implementation and the application of the code:

- K. Miyazaki and N. Ananth. "Nonadiabatic simulations of photoisomerization and dissociation in ethylene using ab initio classical trajectories," J. Chem. Phys. 159, 124110 (2023)
  - https://doi.org/10.1063/5.0163371

References for the most recent implementation will be added as they become available.

Created by Christopher Myers, Ken Miyazaki, and Thomas Werner Trepl.

Disclaimer: The code contained in this package has been written, edited, and used by members of the Ananth group at Cornell University and the Isborn group at the University of California, Merced. It has not been formally reviewed, nor published, nor are there copyrights. Bugs and errors may be present.


# For running trajectories on Pinnacles cluster UCM,
 Steps :
  
 1) Setup no_cavity traj directories :  bash setup.sh  (ensure to have correct input file and slurm script in the same directory, examples provided in repo)
 2) Submit trajectories : bash submit.sh [submits a bunch of slurm jobs]
 3) Get list of random input seeds used : bash get_seed.sh [stores no_cavity seeds in file seed.out]
 4) Copy over list of no_cavity input seeds to cavity traj directory
 5) Setup cavity traj directories : bash setup_cavity.sh (ensure to have correct input file and slurm script in the same directory, examples provided in repo)
 6) Get list of new input seeds used : bash get_seed_new.sh [stores cavity seeds in file seed_new.out]
 7) Verify that the cavity and no_cavity input seeds match
 8) Submit trajectories : bash submit.sh [submits a bych of slurm jobs]
 
 Note : Make sure to modify the trajectory numbers in all scripts according to your requirements. 
