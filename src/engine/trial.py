import integrated
import sys
import os

file_paths = []

# Read input from stdin until an empty line is encountered
while True:
    line = sys.stdin.readline().rstrip()
    if line == "":
        break
    file_paths.append(line)

fileArray = file_paths[0].split(",")
number_of_images = len(fileArray)
print(f"tn:{number_of_images}")  # total no of images sent to js file
sys.stdout.flush()

current_number_of_completed_images = 0
currently_working_on = 0

for file in fileArray:
    try:
        print(f"sd:{currently_working_on}")
        sys.stdout.flush()
        integrated.TakeImg(file)
        integrated.calculate()
        current_number_of_completed_images += 1

        
    except:
        current_number_of_completed_images += 1
        print(f"cd:{current_number_of_completed_images}")
        sys.stdout.flush()
        file_name = os.path.basename(file)
        print(f"er_msg:{file_name}")  # error message to show finished with errors
        sys.stdout.flush()
        print("An error occured while processing the image")
        sys.stdout.flush()
        
        
    currently_working_on += 1
    


print(f"er:{0}")  # error message to show finished without errors
sys.stdout.flush()


