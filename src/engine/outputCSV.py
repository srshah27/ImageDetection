import sys
sys.path.append('D:\\Projects\\ImageDetection\\Lib\\site-packages')


import pandas as pd
import os.path
import json
from datetime import datetime
        
        
def writeOutput(imgName, outputPath, width, maxHeight):
    fileName = "Output.csv"
    filePath = os.path.join(outputPath, fileName)
    imgName = os.path.basename(imgName)
    
    json_file_path = 'project-settings.json'
    
    try:
        f = open (json_file_path, "r")
        data = json.loads(f.read())
        # 'data' is already a Python dictionary

        # Access specific values from the dictionary
        name = data['name']
        operator = data['operator']
        note = data['note']
        

        # You can use these values as needed
        print(f'Name: {name}')
        print(f'Operator: {operator}')
        print(f'Note: {note}')

    except:
        print("No json file found")
        name = ''
        operator = ''
        note = ''
        
        
    # check to include file header
    file_exists = os.path.isfile(filePath)
    # representing data in accordance with pandas dataFrame
    df = pd.DataFrame(
        {
            "imgName": [imgName],
            "width": [width],
            "length": [maxHeight],
            "name": [name],
            "operator": [operator],
            "date": [datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")],
            "note": [note],
            # "Dmin": [minHeight],
        },
    )

    # Appending to csv
    # only include header for new csv files
    df.to_csv(filePath, mode="a", index=False, header=not file_exists)
    print(f"finished:{filePath}")   
    sys.stdout.flush()
    