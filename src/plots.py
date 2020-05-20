import pandas as pd
from src.statistics import joined_list, overall_pearson_r 
def plot_todos():
    f,ax=plt.subplots(4,1,figsize=(14,14), dpi=90)
    plt.subplots_adjust(hspace=0.8)
    plt.sca(ax[0])
    plt.plot(joined_list[0][["normalized_pol", "normalized_twe"]])
    plt.title('2017')
    plt.sca(ax[1])
    plt.plot(joined_list[1][["normalized_pol", "normalized_twe"]])
    plt.title('2018')
    plt.sca(ax[2])
    plt.plot(joined_list[2][["normalized_pol", "normalized_twe"]])
    plt.title('2019')
    plt.sca(ax[3])
    plt.plot(joined_list[3][["normalized_pol", "normalized_twe"]])
    plt.title('2020')
    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image