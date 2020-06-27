from sklearn.cluster import KMeans
from src.load_and_process_data import load
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np


def the_elbow_method(data, minimum=2, maximum=18):

    plot = []
    for i in range(minimum, maximum):
        k_m = KMeans(n_clusters=i)
        k_m.fit_predict(data)
        plot.append(k_m.inertia_)
    plt.plot(range(minimum, maximum), plot, marker='D')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')
    plt.xticks(list(range(minimum, maximum)))
    plt.show()


def silhouette_scores(data, minimum=2, maximum=7, metric='euclidean'):
    # Used to study the separation distance between the resulting clusters.
    # Displays a measure of how close each point in one cluster is to points
    # in the neighboring clusters and provides a way to assess parameters like number of clusters visually.
    # This measure has a range of [-1, 1].

    # Code found on :
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
    # and modified for our usage

    for n in range(minimum, maximum):
        # Create a subplot with 1 row and 1 columns
        f, axs = plt.subplots(1, 1)

        # The silhouette coefficient can range from -1, 1 but in this example all
        axs.set_xlim([-1, 1])

        # Initialize the k_m with i value and a random generator
        k_m = KMeans(n_clusters=n)
        labels = k_m.fit_predict(data)
        print('Silhouette score for', n, 'clusters: ', silhouette_score(data, labels))

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed clusters
        avg = silhouette_score(data, labels)

        # Compute the silhouette scores for each sample
        sample_values = silhouette_samples(data, labels)

        y_lower = 10
        for k in range(n):
            # Aggregate the silhouette scores for samples belonging to cluster i, and sort them
            kth_values = sample_values[labels == k]
            kth_values.sort()

            size = kth_values.shape[0]
            y_upper = y_lower + size

            color = cm.jet(float(k) / n)
            axs.fill_betweenx(np.arange(y_lower, y_upper), 0, kth_values, facecolor=color, edgecolor="black", alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            axs.text(-0.05, y_lower + 0.5 * size, str(k))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        axs.set_xlabel("The Silhouette coefficient values")

        # The vertical line for average silhouette score of all the values
        axs.axvline(x=avg, color="red", linestyle=":")

        axs.set_yticks([])  # Clear the yaxis labels / ticks
        axs.set_xticks([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.title(("Silhouette analysis for KMeans clustering with %d clusters" % n))

    plt.show()


if __name__ == '__main__':
    data = load()
    the_elbow_method(data)
    silhouette_scores(data)
    # After the elbow method and silhouette scores we can deduct that 6 is a good number of clusters
