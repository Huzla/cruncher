from sklearn.cluster import Birch
from sklearn.decomposition import PCA
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

target_file_path = "./result/result-yle.json"

data = {}

def choose_closest(points, indices, reference):
    print(points.shape, indices.shape, reference)
    distances = euclidean_distances(points, [reference])
    return indices[np.argmin(distances)]
    

with open(target_file_path, encoding="utf-8") as f:
    data = json.loads(f.read())

values = list(data["members"].values())
keys = np.array(list(data["members"].keys()))

pca = PCA(n_components=2)
transformed = pca.fit_transform(values)

clustering = Birch(n_clusters=None)
clustering.fit(transformed)

centroids = clustering.subcluster_centers_

center_indices = [ choose_closest(np.array([transformed[i] for i, value in enumerate(clustering.labels_) if value == label ]),np.array([i for i, value in enumerate(clustering.labels_) if value == label ]), centroids[label]) for label in np.arange(len(centroids)) ]

for label in range(len(centroids)):
    print(keys[[i for i, value in enumerate(clustering.labels_) if value == label ]])
    print("")

x = transformed.T[0,:]
y = transformed.T[1,:]

fig, ax = plt.subplots()
im = ax.scatter(x, y, c=clustering.labels_)
ax.add_artist(ax.legend(*im.legend_elements(), loc="lower left", title="Classes"))

plt.show()