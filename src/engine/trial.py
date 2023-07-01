import integrated
import sys
print("Hello World")
sys.stdout.flush()

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
for file in fileArray:
    # print(file)
    print(f"sd:{current_number_of_completed_images}")
    sys.stdout.flush()
    integrated.TakeImg(file)
    integrated.calculate()
    current_number_of_completed_images += 1
    # print(f"cd:{current_number_of_completed_images}")
    # sys.stdout.flush()


print(f"er:{0}")  # error message to show finished without errors
sys.stdout.flush()


