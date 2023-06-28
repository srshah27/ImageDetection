import sys
sys.path.append('D:\\Projects\\ImageDetection\\Lib\\site-packages')


import pandas as pd
import os.path


def writeOutput(imgName, width, maxHeight, minHeight):
    fileName = "Output.csv"

    # check to include file header
    file_exists = os.path.isfile(fileName)
    # representing data in accordance with pandas dataFrame
    df = pd.DataFrame(
        {
            "imgName": [imgName],
            "width": [width],
            "Dmax": [maxHeight],
            "Dmin": [minHeight],
        },
    )

    # Appending to csv
    # only include header for new csv files
    df.to_csv("Output.csv", mode="a", index=False, header=not file_exists)