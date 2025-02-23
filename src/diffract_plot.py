import matplotlib.pyplot as plt
import pandas as pd
import argparse
from pathlib import Path

# Mapping of short names to full column names
COLUMN_MAP = {
    'r': 'Total_Reflection',
    't': 'Total_Transmission',
    'a': 'Absorption',
    'reflection': 'Total_Reflection',
    'transmission': 'Total_Transmission',
    'absorption': 'Absorption'
}

# Valid columns
VALID_COLUMNS = set(COLUMN_MAP.keys())

# Argument parsing
parser = argparse.ArgumentParser(
    description="Plot optical properties from CSV data."
)

parser.add_argument(
    '-f', '-file', '--filename',
    help="Input data file", type=str, required=True
)
parser.add_argument(
    '--xmin', '-xmin',
    help="Minimum x-axis value", type=float, default=None
)
parser.add_argument(
    '--xmax', '-xmax',
    help="Maximum x-axis value", type=float, default=None
)
parser.add_argument(
    '--ymin', '-ymin',
    help="Minimum y-axis value", type=float, default=0.0
)
parser.add_argument(
    '--ymax', '-ymax',
    help="Maximum y-axis value", type=float, default=1.0
)
parser.add_argument(
    '--title', '-title',
    help="Title of the plot (optional)", type=str, default=None
)

parser.add_argument(
    '--columns', '-c', '-col',
    help="Columns to plot (comma-separated: r,a or reflection,absorption)",
    type=str,
    default="r,t,a"
)

args = parser.parse_args()

# Extract filename and check existence
file_path = Path(args.filename)
if not file_path.exists():
    raise FileNotFoundError(f"File {args.filename} not found.")

output_plot = file_path.stem + "_plot.png"

# Load data
try:
    """
        Read data from file with automatic column detection.
    """
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()

    column_names = first_line.lstrip('#').strip().split()
    data = pd.read_csv(file_path, sep=r'\s+', skiprows=1, names=column_names)
except Exception as e:
    raise ValueError(f"Error reading file {args.filename}: {e}")

# Process column selection
selected_keys = args.columns.split(',')
invalid_keys = [col for col in selected_keys if col not in VALID_COLUMNS]

if invalid_keys:
    raise ValueError(
        f"Invalid columns: {invalid_keys}. Choose from: {VALID_COLUMNS}"
    )

selected_columns = {COLUMN_MAP[col] for col in selected_keys}

# Plotting
plt.rc('font', family='Arial', size=14)
plt.rc('legend', fontsize=13)

fig, ax = plt.subplots(figsize=(5.5, 5.5))

ax.set_xlabel('Wavelength (µm)', fontweight='bold')
ax.set_ylabel('Diffraction Efficiency (a.u.)', fontweight='bold')
ax.set_ylim([args.ymin, args.ymax])

if args.xmin is not None:
    ax.set_xlim(left=args.xmin)
if args.xmax is not None:
    ax.set_xlim(right=args.xmax)

# Set optional title
if args.title:
    ax.set_title(args.title, fontsize=16, fontweight='bold')

# Color mapping
colors = {
    'Total_Reflection': 'b',
    'Total_Transmission': 'g',
    'Absorption': 'r'
}

labels = {
    'Total_Reflection': 'Reflection',
    'Total_Transmission': 'Transmission',
    'Absorption': 'Absorption'
}

for col in selected_columns:
    ax.plot(data['wavelength'], data[col], colors[col], label=labels[col])

# Legend inside the figure (bottom-right corner)
# ax.legend(frameon=True, loc='lower right')
ax.legend(frameon=True)

ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
fig.savefig(output_plot, dpi=300)

print(f"Plot saved as {output_plot}")
