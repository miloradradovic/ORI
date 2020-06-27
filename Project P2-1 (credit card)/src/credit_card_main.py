from src.load_and_process_data import load
from src.k_means import the_elbow_method, silhouette_scores, pca
from src.exploratory_data_analysis import eda

if __name__ == '__main__':
    data = load()
    the_elbow_method(data)
    silhouette_scores(data)
    # After the elbow method and silhouette scores we can deduct that 6 is a good number of clusters
    pca(data)
    eda(data)
    print("All done!")
