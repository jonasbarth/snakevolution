import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt

from util.analysis import CsvLoader


def plot_min_mean_max(min_data: np.array, mean_data: np.array, max_data: np.array, smoothed: bool = False):
    """
    Plots the minimum, mean, and max data arrays in the same plot.
    :param min_data: the min data to be plotted
    :param mean_data: the mean data to be plotted
    :param max_data: the max data to be plotted
    :param smoothed: True if the lines should be smoothed, False if the data should be plotted as it comes in
    :return:
    """
    if smoothed:
        min_data = medfilt(min_data, 7)
        mean_data = medfilt(mean_data, 7)
        max_data = medfilt(max_data, 7)
    min_mean_max_data = np.stack([min_data, mean_data, max_data], axis=1)
    plt.plot(min_mean_max_data)

    plt.show()


def min_mean_max_split(data: np.array) -> (np.array, np.array, np.array):
    """
    Splits the data into an array containing the minimum value per column, an array containing the mean value per column,
    and an array containing the maximum value per column.
    :param data: The data to be split
    :return: 3 nump arrays (min, mean, max). The output arrays will have the same dimension in axis=1 as the input array.
    If data.shape=(50, 1000), then each of the output arrays will have data.shape=(, 1000)
    """
    return np.amin(data, axis=0), np.mean(data, axis=0), np.amax(data, axis=0)


if __name__ == "__main__":

    loader = CsvLoader("../models/genetic/10_01_2021__15_18_06")

    if loader.load():
        data = loader.as_numpy()
        min_data, mean_data, max_data = min_mean_max_split(data)

        plot_min_mean_max(min_data, mean_data, max_data)
