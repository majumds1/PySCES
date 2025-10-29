from PySCESPol.Polariton import TCPolaritonRunner, CoupledMolecule, TCRunnerOptions
from qcelemental.models import Molecule

integrator = 'rk4-uprop'


#   number of atoms in the molecule
natom = 9
nel = 4 # number of electronic states
temp = 300 # simulation temperature in Kelvin

# Maximum propagation time (a.u.), one Runge-Kutta step (a.u.) (Only relevant for RK4)
tmax_rk4, Hrk4 = 70*42, 4.0

# Index of initially occupied electronic state
init_state = 3

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
        'maxit': 300, 
        #   TD-DFT
        'cis': 'yes',
        'cisguessvecs': 5,
        'cissubspace': 5,
        'cisnumstates': 3,
        'cisconvtol': 1e-5,
        'cismaxiter': 500,
}


# Terachem files
fname_tc_xyz      = "/home/souravmajumdar/trial_10_21/cavity/traj-1/Wigner/a_opt.xyz"
fname_tc_geo_freq = "/home/souravmajumdar/trial_10_21/cavity/traj-1/Wigner/Geometry.frequencies.dat"
fname_tc_redmas   = "/home/souravmajumdar/trial_10_21/cavity/traj-1/Wigner/Reduced.mass.dat"
fname_tc_freq     = "/home/souravmajumdar/trial_10_21/cavity/traj-1/Wigner/Frequencies.dat"

#hdf5_logging = False
logging_mode = 'w'

EV_2_AU = 1/27.2114079527
coupled_mol = CoupledMolecule(5.72882098*EV_2_AU, [0,1,2,3], natom, [1.0, 0.0, 0.0], rwa=True, dse=False, pdt=False, subset_states='single')
coupled_mol.set_gc_from_coupling(0.1*EV_2_AU, 1.4855)
mol = Molecule.from_file(fname_tc_xyz)
tc_runner_opts = TCRunnerOptions()
tc_runner_opts.host = tcr_host
tc_runner_opts.port = tcr_port
tc_runner_opts.job_options = tcr_job_options
tc_runner_opts.state_options = {'grads': [0, 1, 2, 3]}
tc_runner_opts.server_root = tcr_server_root
QC_RUNNER = TCPolaritonRunner(coupled_mol, mol.symbols, tc_runner_opts)
# QC_RUNNER._rk4_inteprolation = (integrator == 'RK4_Interpolation')
# extra_loggers = [QC_RUNNER.polariton_logger]
mol_input_format = 'terachem'
QC_RUNNER.set_print_level(0)

input_seed = seednumber
