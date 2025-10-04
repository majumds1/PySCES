import numpy as np
import h5py
from pysces.common import PhaseVars, ESVars
import qcelemental as qcel

# Physical constants and unit conversion factors
pi       = np.pi
hplanck  = 6.62607015*10**-34   # Planck's constant in SI
hbar     = hplanck/(2*pi)       # reduced Planck's constant in SI
clight   = 2.99792458*10**8     # speed of light in SI
kb       = 1.380649*10**-23     # Boltzmann constant
eh2j     = 4.359744650*10**-18  # Hartree to Joule
amu2au   = 1.822888486*10**3    # atomic mass unit to atomic unit 
autime2s = hbar/eh2j            # atomic unit time to second
au2fs    = autime2s*10**15      # atomic unit time to second
ang2bohr = 1.8897259886         # angstroms to bohr
k2autmp  = kb/eh2j              # Kelvin to atomic unit temperature
beta     = 1.0/(300 * k2autmp)  # inverse temperature in atomic unit



class DebugRunner:
    def __init__(self, atoms: list[str], model_params: dict):
        self.k1 = model_params.get("k1", 0.1)          # force constant for state 1
        self.k2 = model_params.get("k2", 0.1)          # force constant for state 2
        self.R1 = model_params.get("R1", 1.0)           # equilibrium bond length for state 1
        self.R2 = model_params.get("R2", 1.5)           # equilibrium bond length for state 2
        self.V12 = model_params.get("V12", 0.005)       # constant electronic coupling
        self.atoms = atoms

        self._prev_evecs = None

    def set_logger_file(self, logger_file: h5py.File):
        """Set the logger file for storing results."""
        self.logger_file = logger_file

    def save_restart(self):
        out_data = {
            'k1': self.k1,
            'k2': self.k2,
            'R1': self.R1,
            'R2': self.R2,
            'V12': self.V12,
        }
        return out_data
    
    def load_restart(self, data: dict):
        self.k1 =  data.get("k1", 0.1)
        self.k2 =  data.get("k2", 0.1)
        self.R1 =  data.get("R1", 1.0)
        self.R2 =  data.get("R2", 1.5)
        self.V12 = data.get("V12", 0.005)

    def get_geoo_hess(self, options: dict):
        data = self.get_molecule_props(None)

        atomic_symbols = data.get('atoms')
        xyz_ang = np.array(data.get('xyz')).reshape((-1, 1))
        hessian_vecs = data.get('hessian_vecs')
        frq = np.array(data.get('freq')) * 2.0*pi*clight*100*autime2s
        redmas = data.get('reduced_mass')
        L = np.zeros_like(hessian_vecs)
        U = np.zeros_like(hessian_vecs)

        # TODO: Debug
        U = np.zeros((7, 6))
        U[-1:] = np.array([[1, 0, 0, -1, 0, 0]])

        amu_masses = [qcel.periodictable.to_mass(sym) for sym in atomic_symbols for _ in range(3)]
        amu_mat = np.diag(amu_masses)
        atom_number_mat = [] # not necesary for non-GAMESS runners

        # return(amu_mat, xyz_ang, frq, redmas, L, U, atom_number_mat)
        # atom_number_mat is only used by GAMESS
        return(amu_mat, xyz_ang, frq, U, atom_number_mat)

    @staticmethod
    def get_molecule_props(prams):
        data = {
            'atoms': ['H', 'H'],
            'xyz': np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
            'hessian_vecs': np.zeros((2, 2)),
            'freq': np.ones(6) * 3000,
            'reduced_mass': np.ones(6)
        }
        return data

    def run_new_geom(self, phase_vars: PhaseVars) -> ESVars:
        ''' run a new calculation '''
        nuc_coords = phase_vars.nuc_q.reshape(-1, 3)

        if len(nuc_coords) != 2:
            raise ValueError("DebugRunner requires exactly two nuclear coordinates.")

        energy, U = self._diagonalize(nuc_coords)
        dH = self._dHdx(nuc_coords)
        grads = self._gradients(nuc_coords, dH, U)
        nacs = self._nac(nuc_coords, dH, energy, U)

        return ESVars(
            all_energies=energy,
            elecE=energy,
            grads=grads,
            nacs=nacs,
        )


    def _H(self, coords: np.ndarray) -> np.ndarray:
        
        R = np.linalg.norm(coords[0] - coords[1])
        print(f' ######     {R:8.4f}     ######')
        V11 = 0.5 * self.k1 * (R - self.R1)**2
        V22 = 0.5 * self.k2 * (R - self.R2)**2
        return np.array([[V11, self.V12], [self.V12, V22]])

    def _dHdx(self, coords: np.ndarray) -> np.ndarray:
        R = np.linalg.norm(coords[0] - coords[1])
        dV11dx = self.k1 * (R - self.R1)
        dV22dx = self.k2 * (R - self.R2)
        return np.array([[dV11dx, 0.0], [0.0, dV22dx]])

    
    def _diagonalize(self, coords: np.ndarray):
        H = self._H(coords)
        evals, evecs = np.linalg.eigh(H)
        order = np.argsort(evals)
        evals = evals[order]
        evecs = evecs[:, order]

        if self._prev_evecs is not None:
            sign_flips = np.sign(np.sum(self._prev_evecs * evecs, axis=0))
            evecs *= sign_flips
        self._prev_evecs = evecs.copy()

        return evals, evecs

    def _gradients(self, coords: np.ndarray, dHx: np.ndarray, U: np.ndarray) -> tuple[float, float]:
        """Return energy gradients dE1/dx and dE2/dx using Hellmann–Feynman theorem."""

        dX = coords[0] - coords[1]
        dX_norm = dX / np.linalg.norm(dX)

        grad_E1 = U[:, 0] @ dHx @ U[:, 0]
        grad_E2 = U[:, 1] @ dHx @ U[:, 1]

        grads = np.zeros((2, 6))
        grads[0, 0:3] =  grad_E1 * dX_norm
        grads[0, 3:6] = -grad_E1 * dX_norm
        grads[1, 0:3] =  grad_E2 * dX_norm
        grads[1, 3:6] = -grad_E2 * dX_norm

        return grads

    def _nac(self, coords: np.ndarray, dHx: np.ndarray, E: np.ndarray, U: np.ndarray) -> float:

        dX = coords[0] - coords[1]
        dX_norm = dX / np.linalg.norm(dX)

        phi1 = U[:, 0]
        phi2 = U[:, 1]
        delta_E = E[1] - E[0]
        if abs(delta_E) < 1e-8:
            return 0.0  # Avoid division by zero
        d12 = phi1 @ dHx @ phi2 / delta_E

        nacs = np.zeros((2, 2, 6)) 
        nacs[0, 1, 0:3] =  d12 * dX_norm
        nacs[0, 1, 3:6] = -d12 * dX_norm
        nacs[1, 0] = -nacs[0, 1] 

        return nacs
