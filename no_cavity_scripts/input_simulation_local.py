
integrator = 'rk4-uprop'

# number of atoms in the molecule
natom = 9
nel = 3      # number of electronic states
temp = 300   # simulation temperature in Kelvin

# Maximum propagation time (a.u.), one Runge-Kutta step (a.u.) (Only relevant for RK4)
tmax_rk4, Hrk4 = 70*42, 4.0

# Index of initially occupied electronic state
init_state = 2

# Restart request: 0 = no restart, 1 = restart
restart = 0
#restart_file_in = 'restart.json'

#   TeraChem runner options
tcr_host = ['ipserver']
tcr_port = [portnumber]
tcr_server_root = ['pathserver']
tcr_job_options = {
        'method': 'pbe0',
        'basis': '6-31G*',
        'charge': 0,
        'spinmult': 1,
        'closed_shell': True,
        'restricted': True,
        'precision': 'mixed',
        'convthre': 1E-6,

        #   TD-DFT
        'cis': 'yes',
        'cisguessvecs': 5,
        'cissubspace': 5,
        'cisnumstates': 3,
        'cisconvtol': 1e-5,
        'cismaxiter': 500,
}
tcr_state_options = {
    'grads': [1, 2, 3]
}



# Terachem files
fname_tc_xyz      = "/home/souravmajumdar/trial_10_21/traj_1/Wigner/a_opt.xyz"
fname_tc_geo_freq = "/home/souravmajumdar/trial_10_21/traj_1/Wigner/Geometry.frequencies.dat"
fname_tc_redmas   = "/home/souravmajumdar/trial_10_21/traj_1/Wigner/Reduced.mass.dat"
fname_tc_freq     = "/home/souravmajumdar/trial_10_21/traj_1/Wigner/Frequencies.dat"

hdf5_logging = False
logging_mode = 'w'
QC_RUNNER = 'terachem'

input_seed = 2seednumber
