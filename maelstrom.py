# Ignore warnings (just for clarity of tutorial)
import warnings
warnings.filterwarnings('ignore')

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import fcluster, cut_tree, linkage
from scipy.spatial.distance import pdist

from gimmemotifs.maelstrom import run_maelstrom
from gimmemotifs import __version__

print("GimmeMotifs version:", __version__)

# Read the command-line argument passed to the interpreter when invoking the script
tsv_filename = sys.argv[1]

#read first six columns, the last column for some reason has NAs so ignore it
df = pd.read_table(tsv_filename, index_col=0, usecols=range(6))

# Set region size to 200
w = 200
new_index = pd.DataFrame(df.index.to_series().str.split('[:-]', expand=True))
new_index.columns = ["chrom", "start", "end"]
new_index["start"] = ((new_index["start"].astype(int) + new_index["end"].astype(int)) / 2 - w / 2).astype(int)
new_index["end"] = new_index["start"] + w
new_index["loc"] = new_index["chrom"] + ":" + new_index["start"].astype(str) + "-" + new_index["end"].astype("str")
df["loc"] = new_index["loc"]
df = df.set_index("loc")


# Log-transform count data
df = np.log2(df + 1)

# Normalize
df_norm = df[:]
df_norm[:] = scale(df, axis=0)

#save table
gz_filename = sys.argv[2]

filename = "%s.withHeader_tsv.gz" % gz_filename
df_norm.to_csv(filename, sep="\t", compression="gzip")
