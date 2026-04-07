from qcelemental.models import Molecule
from pysces.qcRunners.TeraChem import TCRunner, TCJob, TCJobBatch, TCRunnerOptions
import numpy as np
import pickle

def test_compare_dicts(d1: dict, d2: dict, name: str = '') -> None:
    assert set(d1.keys()) == set(d2.keys()), \
        f"{name} keys mismatch: {set(d1.keys())} != {set(d2.keys())}"
    for key in d1:
        v1, v2 = d1[key], d2[key]
        if isinstance(v1, np.ndarray):
            np.testing.assert_array_almost_equal(v1, v2, err_msg=f"{name}['{key}'] mismatch")
        else:
            assert v1 == v2, f"{name}['{key}'] mismatch: {v1} != {v2}"

def test_compare_tc_jobs(job1: TCJob, job2: TCJob) -> None:
    np.testing.assert_array_almost_equal(job1.geom, job2.geom, err_msg="geom mismatch")
    assert job1.job_type     == job2.job_type,     f"job_type mismatch:     {job1.job_type} != {job2.job_type}"
    assert job1.excited_type == job2.excited_type, f"excited_type mismatch: {job1.excited_type} != {job2.excited_type}"
    assert job1.state        == job2.state,        f"state mismatch:        {job1.state} != {job2.state}"
    assert job1.name         == job2.name,         f"name mismatch:         {job1.name} != {job2.name}"
    assert job1.start_time   == job2.start_time,   f"start_time mismatch:   {job1.start_time} != {job2.start_time}"
    assert job1.end_time     == job2.end_time,     f"end_time mismatch:     {job1.end_time} != {job2.end_time}"

    assert set(job1.opts.keys()) == set(job2.opts.keys()), \
        f"opts keys mismatch: {set(job1.opts.keys())} != {set(job2.opts.keys())}"    

    #   file names can differ at the end
    if 'cisrestart' in job1.opts:
        restart_1 = job1.opts.pop('cisrestart')
        restart_2 = job2.opts.pop('cisrestart')
        assert 'cis_restart' in restart_1, "cisrestart missing 'cis_restart' key"
        assert 'cis_restart' in restart_2, "cisrestart missing 'cis_restart' key"

    if 'cisproperties' in job1.opts:
        with open(job1.opts.pop('cisproperties'), 'r') as f:
            props1 = f.read()
        with open(job2.opts.pop('cisproperties'), 'r') as f:
            props2 = f.read()
        assert props1 == props2, "cisproperties file content mismatch"

    job1.results.pop('cisrestart', None)
    job2.results.pop('cisrestart', None)

    test_compare_dicts(job1.opts, job2.opts, name='opts')
    test_compare_dicts(job1.results, job2.results, name='results')


def test_compare_job_batches(batch1: TCJobBatch, batch2: TCJobBatch) -> None:
    assert len(batch1.jobs) == len(batch2.jobs), f"Number of jobs mismatch: {len(batch1.jobs)} != {len(batch2.jobs)}"

    for j1 in batch1.jobs:
        client1 = j1.client
        client1_signature = (client1.host, client1.port, client1.server_root)
        for j2 in batch2.jobs:
            client2 = j2.client
            client2_signature = (client2.host, client2.port, client2.server_root)
            if client1_signature == client2_signature:
                test_compare_tc_jobs(j1, j2)
                break
        else:
            assert False, f"No matching client found for job with client signature {client1_signature}"

if __name__ == "__main__":
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
    tc_runner_opts = TCRunnerOptions(
        host=['localhost']*2,
        port=[12345, 12346],
        server_root=['/tmp/server1', '/tmp/server2'],
        job_options=tcr_job_options,
        state_options={'grads': [0, 1, 2, 3]}
    )
    mol = Molecule.from_file('mol.xyz')
    tc_runner = TCRunner(mol.symbols.tolist(), tc_runner_opts, server_disabled=True)
    job_batch = tc_runner.create_jobs(mol.geometry, False, (1,2,3), ((1, 2), (2, 3), (1, 3)))

    # with open('job_batch.pkl', 'wb') as f:
    #     pickle.dump(job_batch, f)

    with open('job_batch.pkl', 'rb') as f:
        job_batch_ref: TCJobBatch = pickle.load(f)

    tc_runner._send_jobs_to_clients(job_batch)
    test_compare_job_batches(job_batch, job_batch_ref)
    print('\nPass')