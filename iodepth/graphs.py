import matplotlib.pyplot as plt

# X and Y axis values to be present on graph.
x_ticks = [1000, 2000, 3000, 4000]
y_ticks = [0, 25, 50, 75, 100]

# Constant number of entries for x axis
num_of_entries = [128, 1024, 4096]


def plot_benchmark(name, local_accuracy, gshare_accuracy, tournament_accuracy):
    fig = plt.figure()

    # Plot the data
    plt.plot(num_of_entries, local_accuracy, label="Local Predictor", marker='x')
    plt.plot(num_of_entries, gshare_accuracy, label="Gshare Predictor", marker='x')
    plt.plot(num_of_entries, tournament_accuracy, label="Tournament Predictor", marker='x')

    # plt.xticks(x_ticks)
    # plt.yticks(y_ticks, ['0.00%', '25.00%', '50.00%', '75.00%', '100.00%'])

    # Add a legend
    plt.legend()

    # Label the x-axis & y-axis
    plt.xlabel("PHT Entries")
    plt.ylabel("Prediction Accuracy")
    
    # Add title to graph
    plt.title(name)

    # Show the plot
    # plt.show()

    # Save the figure
    fig.savefig("{0}.png".format(name.replace(" ", "_")))


def sjeng():
    Sjeng_local_128 = 78.8667
    Sjeng_local_1024 = 81.2021
    Sjeng_local_4096 = 82.3824
    Sjeng_local = [ Sjeng_local_128, Sjeng_local_1024, Sjeng_local_4096 ]

    Sjeng_gshare_128 = 68.7212
    Sjeng_gshare_1024 = 78.5808
    Sjeng_gshare_4096 = 86.0448
    Sjeng_gshare = [ Sjeng_gshare_128, Sjeng_gshare_1024, Sjeng_gshare_4096 ]

    Sjeng_Tournament_128 = 78.1657
    Sjeng_Tournament_1024 = 83.7628
    Sjeng_Tournament_4096 = 87.711
    Sjeng_Tournament = [ Sjeng_Tournament_128, Sjeng_Tournament_1024, Sjeng_Tournament_4096 ]
    
    plot_benchmark("Benchmark Sjeng", Sjeng_local, Sjeng_gshare, Sjeng_Tournament)


def gobmk():
    Gobmk_local_128 = 74.0507
    Gobmk_local_1024 = 75.1141
    Gobmk_local_4096 = 75.7733
    Gobmk_local = [ Gobmk_local_128, Gobmk_local_1024, Gobmk_local_4096 ]

    Gobmk_gshare_128 = 69.0445
    Gobmk_gshare_1024 = 75.4056
    Gobmk_gshare_4096 = 80.2168
    Gobmk_gshare = [ Gobmk_gshare_128, Gobmk_gshare_1024, Gobmk_gshare_4096 ]

    Gobmk_Tournament_128 = 74.1412
    Gobmk_Tournament_1024 = 78.5362
    Gobmk_Tournament_4096 = 81.939
    Gobmk_Tournament = [ Gobmk_Tournament_128, Gobmk_Tournament_1024, Gobmk_Tournament_4096 ]

    plot_benchmark("Benchmark GOBMK", Gobmk_local, Gobmk_gshare, Gobmk_Tournament)


def matrix_mul():
    Matrix_Mul_local_128 = 99.6393
    Matrix_Mul_local_1024 = 99.6454
    Matrix_Mul_local_4096 = 99.6393
    Matrix_Mul_local = [ Matrix_Mul_local_128, Matrix_Mul_local_1024, Matrix_Mul_local_4096 ]

    Matrix_Mul_gshare_128 = 99.2759
    Matrix_Mul_gshare_1024 = 99.5476
    Matrix_Mul_gshare_4096 = 99.6116
    Matrix_Mul_gshare = [ Matrix_Mul_gshare_128, Matrix_Mul_gshare_1024, Matrix_Mul_gshare_4096 ]

    Matrix_Mul_Tournament_128 = 99.6268
    Matrix_Mul_Tournament_1024 = 99.6529
    Matrix_Mul_Tournament_4096 = 99.6688
    Matrix_Mul_Tournament = [ Matrix_Mul_Tournament_128, Matrix_Mul_Tournament_1024, Matrix_Mul_Tournament_4096 ]
    
    plot_benchmark("Benchmark Matrix Multiplication", Matrix_Mul_local, Matrix_Mul_gshare, Matrix_Mul_Tournament)


sjeng()
gobmk()
matrix_mul()
