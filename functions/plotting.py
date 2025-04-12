import matplotlib.pyplot as plt

def hourly_pv_plot(pv_data, title, y_label, x_label, filename):
    """
    Plots the hourly PV data.

    :param pv_data: The PV data to plot.
    :param title: The title of the plot.
    :param y_label: The y-axis label.
    :param x_label: The x-axis label.
    :param filename: The filename to save the plot to.
    """
    file_path = f"plots/{filename}.pdf"
    plt.figure()
    plt.plot(pv_data)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.grid()
    plt.savefig(file_path)
    plt.close()
    print(f"Plot saved to: {file_path}")
    return file_path, title