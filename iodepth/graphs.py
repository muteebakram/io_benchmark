import pandas as pd
import matplotlib.pyplot as plt


def read_iops():
    # queue_depth = ["1", "2", "4", "8"]
    queue_depth = ["1", "2", "4", "8", "16", "32", "64", "128"]

    read_iops = pd.DataFrame(
        {
            "libaio": [
                39445.443645,
                13702.119152,
                16390.121976,
                22657.337065,
                30037.584966,
                10663.467307,
                6628.074385,
                20300.739852,
            ],
            "iouring": [
                20928.014397,
                39835.665734,
                6535.092981,
                10971.205759,
                16407.518496,
                14633.873225,
                31114.954018,
                20203.118752,
            ],
            "iouring_iopoll": [10, 20, 30, 40, 50, 60, 70, 80],
            "iouring_sqpoll": [
                6929.014197,
                31330.867653,
                19967.426059,
                16248.75025,
                13470.211915,
                39993.802479,
                10736.252749,
                21177.364527,
            ],
        },
        index=queue_depth,
    )

    read_iops.plot(kind="bar", figsize=(15, 8))
    plt.xlabel("Queue depth")
    plt.ylabel("Read KFLOPs")
    plt.title("I/O protocol vs Queue depth")

    fig = plt.figure()
    plt.show()
    # fig.savefig("figs/read_iops_vs_iodepth.png")


def write_iops():
    # queue_depth = ["1", "2", "4", "8"]
    queue_depth = ["1", "2", "4", "8", "16", "32", "64", "128"]

    write_iops = pd.DataFrame(
        {
            "libaio": [
                39335.931255,
                13721.111555,
                16491.10178,
                22661.935226,
                30180.327869,
                10607.678464,
                6596.880624,
                20350.129974,
            ],
            "iouring": [
                20962.807439,
                39711.115554,
                6503.69926,
                10912.617477,
                16497.90042,
                14673.665267,
                31228.308677,
                20215.313874,
            ],
            "iouring_iopoll": [10, 20, 30, 40, 50, 60, 70, 80],
            "iouring_sqpoll": [
                6877.624475,
                31498.20072,
                20018.984812,
                16328.534293,
                13476.009596,
                39875.84966,
                10687.262547,
                21185.962807,
            ],
        },
        index=queue_depth,
    )

    write_iops.plot(kind="bar", figsize=(15, 8))
    plt.xlabel("Queue depth")
    plt.ylabel("Write KFLOPs")
    plt.title("I/O protocol vs Queue depth")

    fig = plt.figure()
    plt.show()
    # fig.savefig("figs/write_iops_vs_iodepth.png")


read_iops()
write_iops()
