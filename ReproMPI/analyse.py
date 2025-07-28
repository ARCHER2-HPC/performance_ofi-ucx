import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def parse_benchmark_data(file_name):
    """
    Parses a benchmark output file to extract performance data.

    Args:
        file_name (str): The path to the benchmark output file.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed performance data,
                      with columns representing message sizes and rows
                      representing iterations.
    """
    df_main = None
    df_current_iteration = None
    iteration_count = 0
    
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith("method="):
                pass 
            if line.startswith("========="):
                if df_current_iteration is not None:
                    df_current_iteration = df_current_iteration.drop(
                        ['test', 'total_nrep', 'valid_nrep', 'mean_sec'], axis=1
                    ).T
                    
                    header = df_current_iteration.iloc[0]
                    df_current_iteration = df_current_iteration[1:]
                    df_current_iteration.columns = header
                    
                    if iteration_count == 1:
                        df_main = df_current_iteration
                    else:
                        df_main.loc[iteration_count - 1] = df_current_iteration.iloc[0]
                
                df_current_iteration = None
                iteration_count += 1
                continue
            
            if not line.startswith("#") and line.startswith("      "):
                if df_current_iteration is None:
                    df_current_iteration = pd.DataFrame(columns=line.split())
                else:
                    df_current_iteration.loc[len(df_current_iteration)] = line.split()
    
    return df_main.astype(float)


def get_files_in_directory(path):
    """
    Retrieves a sorted list of file names from the specified directory.

    Args:
        path (str): The directory path.

    Returns:
        list: A sorted list of file names.
    """
    if not os.path.exists(path):
        print(f"Warning: Directory not found: {path}. Returning empty list.")
        return []
    return sorted(os.listdir(path))


# --- Configuration ---
MPI_METHODS = [
    "MPI_Allgather", "MPI_Allreduce", "MPI_Alltoall", "MPI_Bcast", "MPI_Gather", "MPI_Scan", "MPI_Scatter"
]
PATH_BASE_OFI = 'data/ofi/'
PATH_BASE_UCX = 'data/ucx/'

# New base directory for all analysis outputs
ANALYSIS_OUTPUT_ROOT = 'analysis_output/'
FIGURE_OUTPUT_BASE_LOG = os.path.join(ANALYSIS_OUTPUT_ROOT, 'log_scale_plots/')
FIGURE_OUTPUT_BASE_LINEAR = os.path.join(ANALYSIS_OUTPUT_ROOT, 'linear_scale_plots/')
CSV_OUTPUT_PATH = os.path.join(ANALYSIS_OUTPUT_ROOT, 'csv_data/')

# Ensure base output directories exist
os.makedirs(ANALYSIS_OUTPUT_ROOT, exist_ok=True)
os.makedirs(FIGURE_OUTPUT_BASE_LOG, exist_ok=True)
os.makedirs(FIGURE_OUTPUT_BASE_LINEAR, exist_ok=True)
os.makedirs(CSV_OUTPUT_PATH, exist_ok=True)

# Define markers for plotting
markers = ['x', '^', 'h', 'd', 'p', 's', 'o', '>', '<']

# --- Process each MPI method ---
for method_name in MPI_METHODS:
    print(f"\n--- Processing method: {method_name} ---")
    
    # Ensure method-specific output directories exist within the new structure
    os.makedirs(os.path.join(FIGURE_OUTPUT_BASE_LOG, method_name), exist_ok=True)
    os.makedirs(os.path.join(FIGURE_OUTPUT_BASE_LINEAR, method_name), exist_ok=True)

    # --- Data Loading and Processing ---
    ofi_data_dir = os.path.join(PATH_BASE_OFI, method_name)
    ucx_data_dir = os.path.join(PATH_BASE_UCX, method_name)

    ofi_files = get_files_in_directory(ofi_data_dir)
    ucx_files = get_files_in_directory(ucx_data_dir)

    if not ofi_files or not ucx_files:
        print(f"Skipping {method_name}: Missing data files in either OFI ({ofi_data_dir}) or UCX ({ucx_data_dir}) directories.")
        continue

    processed_data_collections = {} 

    # Find one example DataFrame to get column names (message sizes)
    example_df_ofi = parse_benchmark_data(os.path.join(ofi_data_dir, ofi_files[0]))

    for ofi_file in ofi_files:
        try:
            node = int(ofi_file.split('-')[0])
        except ValueError:
            print(f"Skipping malformed OFI file: {ofi_file}")
            continue

        ucx_file = next((f for f in ucx_files if f.startswith(f"{node}-")), None)

        if ucx_file is None:
            print(f"[NOTE-ERROR]: Equivalent file for node {node} in OFI data not found in UCX data. Skipping.")
            continue

        df_ofi = parse_benchmark_data(os.path.join(ofi_data_dir, ofi_file))
        df_ucx = parse_benchmark_data(os.path.join(ucx_data_dir, ucx_file))

        for col in df_ofi.columns: 
            ofi_mean, ofi_std = np.average(df_ofi[col]), np.std(df_ofi[col])
            ucx_mean, ucx_std = np.average(df_ucx[col]), np.std(df_ucx[col])

            new_row = pd.DataFrame({
                'Node': node,
                'OFI': ofi_mean,
                'OFI_err': ofi_std,
                'UCX': ucx_mean,
                'UCX_err': ucx_std,
            }, index=[0])

            if col not in processed_data_collections:
                processed_data_collections[col] = new_row
            else:
                processed_data_collections[col] = pd.concat(
                    [processed_data_collections[col], new_row], ignore_index=True
                )

    for key in processed_data_collections:
        processed_data_collections[key] = processed_data_collections[key].sort_values('Node')

    # --- Generate CSV Output ---
    csv_df = pd.DataFrame(columns=['Node', 'OFI', 'OFI_err', 'UCX', 'UCX_err', 'message_bytes'])
    for key, df in processed_data_collections.items():
        tmp_df = df.copy()
        tmp_df['message_bytes'] = [key] * len(df)
        csv_df = pd.concat([csv_df, tmp_df])

    csv_file_name = os.path.join(CSV_OUTPUT_PATH, f"{method_name}-median-time.csv")
    if os.path.exists(csv_file_name):
        os.remove(csv_file_name) # Remove existing file to ensure clean write
    csv_df.to_csv(csv_file_name, index=False)
    print(f"CSV data for {method_name} saved to: {csv_file_name}")

    # --- Plotting - Log scale (all message sizes on one graph) ---
    fig_log, ax_log = plt.subplots(figsize=(10, 6))

    i = 0
    for col in example_df_ofi.columns: 
        if col in processed_data_collections: 
            ax_log.plot(processed_data_collections[col]['Node'], processed_data_collections[col]['OFI'],
                        marker=markers[i % len(markers)], fillstyle='none', label=f'OFI {col}B')
            ax_log.plot(processed_data_collections[col]['Node'], processed_data_collections[col]['UCX'],
                        linestyle='--', marker=markers[i % len(markers)], fillstyle='none', label=f'UCX {col}B')
            i += 1

    ax_log.set(xlabel='Number of Nodes',
               ylabel='Median Runtime (seconds) (log scale)',
               title=f'{method_name} Performance by Message Size')
    ax_log.grid(True)
    ax_log.set_yscale('log')

    box_log = ax_log.get_position()
    ax_log.set_position([box_log.x0, box_log.y0 + box_log.height * 0.15,
                          box_log.width, box_log.height * 0.85])

    ax_log.legend(
        ncol=len(example_df_ofi.columns),
        loc='lower center', 
        bbox_to_anchor=(0.5, -0.2),  
        fontsize=8, 
        frameon=True,)

    fig_log.tight_layout()
    plt.autoscale()

    figure_log_file_name = os.path.join(FIGURE_OUTPUT_BASE_LOG, method_name, f"{method_name}-log.png")
    plt.savefig(figure_log_file_name, dpi=300, bbox_inches="tight")
    print(f"Log-scale plot for {method_name} saved to: {figure_log_file_name}")
    plt.close(fig_log)

    # --- Plotting - Linear scale (individual plots per message size with error bars) ---
    for col in example_df_ofi.columns:
        if col in processed_data_collections: 
            fig_linear, ax_linear = plt.subplots(figsize=(8, 5))

            ax_linear.errorbar(processed_data_collections[col]['Node'], processed_data_collections[col]['OFI'], 
                               yerr=processed_data_collections[col]['OFI_err'], marker='o',
                               linestyle='-', fillstyle='none', label='OFI', capsize=3)
            ax_linear.errorbar(processed_data_collections[col]['Node'], processed_data_collections[col]['UCX'], 
                               yerr=processed_data_collections[col]['UCX_err'], marker='^',
                               linestyle='--', fillstyle='none', label='UCX', capsize=3)

            ax_linear.set(xlabel='Number of Nodes',
                          ylabel='Median Runtime (seconds)',
                          title=f'{method_name} | Message Size: {col}B')
            ax_linear.grid(True)
            ax_linear.ticklabel_format(useOffset=False, style='plain')
            ax_linear.legend()

            fig_linear.tight_layout()
            
            figure_linear_file_name = os.path.join(FIGURE_OUTPUT_BASE_LINEAR, method_name, f"{method_name}-{col}bytes.png")
            plt.savefig(figure_linear_file_name, dpi=300, bbox_inches="tight")
            print(f"Linear-scale plot for {method_name} - {col}B saved to: {figure_linear_file_name}")
            plt.close(fig_linear)

print("\nAll processing complete.")