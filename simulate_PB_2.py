from os.path import join
import sys
from time import time
from numba import jit
import numpy as np

# @jit(nopython=True)
def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@jit(nopython=True)
def jacobi(u, interior_mask, max_iter, atol=1e-6):
    # Keep two buffers to preserve Jacobi semantics (updates from previous iteration only).
    u_curr = np.copy(u)
    u_next = np.copy(u)

    n_rows = u_curr.shape[0]
    n_cols = u_curr.shape[1]

    for _ in range(max_iter):
        delta = 0.0

        for r in range(1, n_rows - 1):
            mr = r - 1
            for c in range(1, n_cols - 1):
                mc = c - 1
                if interior_mask[mr, mc]:
                    new_val = 0.25 * (
                        u_curr[r, c - 1] + u_curr[r, c + 1] + u_curr[r - 1, c] + u_curr[r + 1, c]
                    )
                    diff = abs(u_curr[r, c] - new_val)
                    if diff > delta:
                        delta = diff
                    u_next[r, c] = new_val

        u_curr, u_next = u_next, u_curr

        if delta < atol:
            break

    return u_curr


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }


if __name__ == '__main__':
    t1 = time()
    print('Starting Jacobi iteration on floor plans...\n')
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    t2 = time()
    print(f"Data loading completed in {format(t2 - t1, '.2f')} seconds. Starting Jacobi iterations...\n")

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u

    t3 = time()
    print(f'Jacobi iteration completed in {format(t3 - t2, ".2f")} seconds. Summary statistics:\n')

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    # print('Jacobi iteration completed. Summary statistics:')
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
    print('Summary statistics printed. Total time elapsed: ', format(time() - t3, '.2f'), " seconds")
    print('Finished in ', format(time() - t1, '.2f'), " seconds")
