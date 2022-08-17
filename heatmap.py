import sys

from gimmemotifs.maelstrom import MaelstromResult
import matplotlib.pyplot as plt

maelstrom_dir = sys.argv[1]
mr = MaelstromResult(maelstrom_dir)

heatmap_filename = sys.argv[2]
heatmap = "%s.png" % heatmap_filename


#Create a heatmap of the results & save
mr.plot_heatmap(threshold=4)
plt.savefig(maelstrom_dir+"/"+heatmap, dpi=300)
