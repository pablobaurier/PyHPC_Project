import numpy as np
import matplotlib.pyplot as plt
from os.path import join

def visualize_inputs(n_buildings=3):
    load_dir = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(load_dir, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:n_buildings]

    fig, axes = plt.subplots(n_buildings, 2, figsize=(10, 5 * n_buildings))
    
    for i, bid in enumerate(building_ids):
        domain = np.load(join(load_dir, f"{bid}_domain.npy"))
        mask = np.load(join(load_dir, f"{bid}_interior.npy"))
        
        # Plot Domain (Initial conditions)
        im0 = axes[i, 0].imshow(domain, cmap='coolwarm')
        axes[i, 0].set_title(f"Building {bid}: Initial Domain")
        plt.colorbar(im0, ax=axes[i, 0], label='Temp ºC')
        
        # Plot Mask (Where simulation happens)
        im1 = axes[i, 1].imshow(mask, cmap='gray')
        axes[i, 1].set_title(f"Building {bid}: Interior Mask")
        
    plt.tight_layout()
    plt.savefig('input_visualization.png')
    print("Visualization saved as input_visualization.png")

if __name__ == "__main__":
    visualize_inputs()