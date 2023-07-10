import sys
import time

sys.path.append('D:\\Projects\\ImageDetection\\Lib\\site-packages')
import os
import cv2 as cv
import pandas as pd
from PIL import Image
from outputCSV import writeOutput
import sys
from scipy.spatial import distance as dist

# ------------------------------ARUCO setup------------------------------------
desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"

# The different ArUco dictionaries built into the OpenCV library.
ARUCO_DICT = {
    "DICT_4X4_50": cv.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL,
}


class arucoClass:
    def main():
        returnDict = {}
        """
        Main method of the program.
        """
        # Check that we have a valid ArUco marker
        if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
            print("[INFO] ArUCo tag of '{}' is not supported".format(sys.args["type"]))
            sys.exit(0)

        # Load the ArUco dictionary

        this_aruco_dictionary = cv.aruco.Dictionary_get(
            ARUCO_DICT[desired_aruco_dictionary]
        )
        this_aruco_parameters = cv.aruco.DetectorParameters_create()

        # Start the video stream
        cap = cv.imread(imgPath)

        frame = cap

        # Detect ArUco markers in the video frame
        try:
            (corners, ids, rejected) = cv.aruco.detectMarkers(
                frame, this_aruco_dictionary, parameters=this_aruco_parameters
            )

            # Check that at least one ArUco marker was detected
            if len(corners) > 0:
                # Flatten the ArUco IDs list
                ids = ids.flatten()

                # Loop over the detected ArUco corners
                marker_corner = corners[0]
                marker_id = ids[0]

                # Extract the marker corners
                corners = marker_corner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                # Convert the (x,y) coordinate pairs to integers
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))

                # print("Aruco Top Left:", top_left)
                # print("Aruco Top Right:", top_right)
                # print("Aruco Bottom Right:", bottom_right)
                # print("Aruco Bottom Left:", bottom_left)

                # Draw the bounding box of the ArUco detection
                cv.line(frame, top_left, top_right, (0, 255, 0), 2)
                cv.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                cv.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                cv.line(frame, bottom_left, top_left, (0, 255, 0), 2)

                # show_images(frame)

                # Calculate and draw the center of the ArUco marker
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

                # Draw the ArUco marker ID on the video frame
                # The ID is always located at the top_left of the ArUco marker
                cv.putText(
                    frame,
                    str(marker_id),
                    (top_left[0], top_left[1] - 15),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

                # Aruco Perimeter
                aruco_perimeter = cv.arcLength(corners, True) / 4

                # print(aruco_perimeter)
                # Pixel to cm ratio
                pixel_mm_ratio = aruco_perimeter / marker_id

                returnDict["ratio"] = pixel_mm_ratio
                returnDict["id"] = marker_id
                returnDict["bottom_right"] = bottom_right

                # Display the resulting frame
                # cv2.imshow('frame', frame)
        except:
            print("No markers detected")
            # print(pixel_mm_ratio, aruco_perimeter)

        # If "q" is pressed on the keyboard,
        # exit this loop

        cv.waitKey(0)

        # Close down the video stream

        cv.destroyAllWindows()
        return returnDict


# -----------------------------show image function------------------------------
def show_images(image):
    scale_percent = 20
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    cv.imshow("a", cv.resize(image, dim, interpolation=cv.INTER_AREA))
    cv.waitKey(0)
    # cv2.imwrite("moiz_cal.jpeg", image)


# ----------------------------------function to detect whole bit-------------------------
def custom_detect(image):
    global max_height, full_width

    # Load image
    # image = cv2.imread("smt_new_try/3\IMG_0006.JPG")

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # convert to grayscale for threshold
    # cv.imwrite("gray.jpeg", gray)
    # imgBlur = cv2.medianBlur(gray, 5)
    # ret, thresholded = cv2.threshold(imgBlur, 30, 50, cv2.THRESH_BINARY)
    # mask = cv2.adaptiveThreshold(thresholded, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 35, 15)  # or try GaussianBlur
    # # imgBlur = cv2.GaussianBlur(imgFile, (5,5), cv2.BORDER_DEFAULT)

    # imgCanny = cv2.Canny(mask, 50, 200, True)
    # imgDial = cv2.dilate(imgCanny, None, iterations=3)
    # imgErode = cv2.erode(imgDial, None, iterations=2)

    # Convert image to grayscale
    #   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #   ret, thresholded = cv2.threshold(gray, 40, 180, cv2.THRESH_BINARY)
    #   mask = cv2.adaptiveThreshold(thresholded, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 49, 35)  # og: (29,15)
    # #   mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 29, 15)  # og: (29,15)

    #   # Use Canny edge detection to find object
    #   edged = cv2.Canny(mask, 45, 80)
    #   imgErode = cv2.dilate(edged, None, iterations=2)
    # imgErode = cv2.erode(dilation, None, iterations=2)

    # Threshold the image to create a binary image
    #   ret, thresholded = cv2.threshold(gray, 30, 200, cv2.THRESH_BINARY)
    #   mask = cv2.adaptiveThreshold(thresholded, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 49, 19)  # og: (29,15)

    #   lines detection got better
    ret, thresholded = cv.threshold(gray, 40, 180, cv.THRESH_BINARY)
    mask = cv.adaptiveThreshold(
        thresholded, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 59, 19
    )  # og: (29,15)

    #   ret, thresholded = cv2.threshold(gray, 40, 180, cv2.THRESH_BINARY)
    #   mask = cv2.adaptiveThreshold(thresholded, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 69, 13)  # og: (29,15)

    # Perform morphological operations to isolate the object
    # kernel = np.ones((3,3), np.uint8)
    # dilation = cv2.erode(mask, kernel, iterations=1)
    # imgErode = cv2.dilate(dilation, kernel, iterations=1)

    erosion = cv.dilate(mask, None, iterations=2)
    # cv.imwrite("erosion.jpeg", erosion)
    imgErode = cv.erode(erosion, None, iterations=2)
    # cv.imwrite("imgErode.jpeg", imgErode)
    # show_images(imgErode)
    #   detectLongestLine(imgErode)

    # Find contours in the image
    contours, _ = cv.findContours(imgErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv.contourArea)

    # Draw a bounding box around the largest contour
    x, y, w, h = cv.boundingRect(largest_contour)
    cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 3)
    # cv.imwrite("bounding_box.jpeg", image)
    # Calculate the coordinates of the four corners of the bounding box
    top_left = (x, y)
    top_right = (x + w, y)
    bottom_right = (x + w, y + h)
    bottom_left = (x, y + h)

    # Show the image with the bounding box
    # show_images(image)
    # cv2.imshow("Object Detection", image)

    # Return the coordinates of the corners
    #   print("Top Left:", top_left)
    #   print("Top Right:", top_right)
    #   print("Bottom Right:", bottom_right)
    #   print("Bottom Left:", bottom_left)

    # the_length_non_design = dist.euclidean(box[0], coordinates[0])/pixelsPerMetric
    # print(f"The non design len is --> {the_length_non_design}")

    the_length_comp = dist.euclidean(top_left, top_right) / pixelsPerMetric
    the_height_comp = dist.euclidean(top_left, bottom_left) / pixelsPerMetric
    print(f"The Complete len is --> {the_length_comp}")
    print(f"The max height is --> {the_height_comp}")
    print(f"cd:{0.3}")
    sys.stdout.flush()
    full_width = the_length_comp
    max_height = the_height_comp
    # cv.imwrite("moiz_cal.jpeg", image)


def detectMinGruve(croppedImgFile):
    global min_height
    imgFile = croppedImgFile
    # imgFile = cv.imread(f"{saveFolder}\cropped_img.jpg")
    ## ------------------------------Manipulation starts here----------------------
    gray = cv.cvtColor(imgFile, cv.COLOR_BGR2GRAY)  # convert to grayscale for threshold
    imgBlur = cv.medianBlur(gray, 5)
    # or try GaussianBlur
    imgBlur = cv.GaussianBlur(imgFile, (5, 5), cv.BORDER_DEFAULT)
    blurPath = f"{saveFolder}/blurimg.jpg"

    cv.imwrite(blurPath, imgBlur)
    imgCanny = cv.Canny(imgBlur, 50, 200, True)
    
    imgDial = cv.dilate(imgCanny, None, iterations=3)
    imgErode = cv.erode(imgDial, None, iterations=2)

    print("Saving manupilated img")
    # cv.imshow("Manipulated", imgErode)
    cv.imwrite(savePath, imgDial)
    
    print(f"cd:{0.3}")
    sys.stdout.flush()

    ##----------------------------------Converting to Binary---------------------------------

    prcImg = cv.imread(savePath)
    # prcImg = imgDial
    prcGray = cv.cvtColor(prcImg, cv.COLOR_BGR2GRAY)
    (thresh, binary) = cv.threshold(prcGray, 127, 255, cv.THRESH_BINARY)

    print(binary.shape)  # (height, width, channels)
    height, width = binary.shape
    cv.imwrite(f"{saveFolder}\Binary.jpg", binary)
    ## ---------------------------------Binary Ends here-------------------------------------

    ## ---------------------------------Manipulation ends here ------------------------------

    ## --------------------------------Detecting the points ---------------------------------

    UpperList = [None] * width
    LowerList = [None] * width
    start = time.time()


    for x in range(0, (width - 1)):
        yLower = height - 1
        yUpper = 0
        while yUpper < (height * 0.66):
            if binary[yUpper, x] == 255:
                UpperList[x] = yUpper
                break
            else:
                yUpper += 2

        while yLower > height * 0.33:
            if binary[yLower, x] == 255:
                LowerList[x] = yLower
                break
            else:
                yLower -= 2


    filterUpper = list(filter(lambda x: x is not None, UpperList))
    filterLower = list(filter(lambda x: x is not None, LowerList))

    Upperdf = pd.DataFrame(filterUpper, columns=["Upper"])
    Lowerdf = pd.DataFrame(filterLower, columns=["Lower"])
    
    startY = Upperdf[50:150].mean(axis=0)
    endY = Lowerdf[50:150].mean(axis=0)
    startY = int(startY)
    endY = int(endY)
    end = time.time()

    print("Time: ", end - start)

    print("Upper Pixel", startY)
    print("Lower Pixel", endY)

    ## -------------------------------------Detecting Points Ends here-----------------------------

    ## -------------------------------------Plotting the points------------------------------------

    plotimg = cv.imread(imgPath)
    # plotimg = fullImgFile


    # selectUp.to_csv("out/csv/selectUp.csv")
    # selectDown.to_csv("out/csv/selectDown.csv")
    
    start = (150, startY)
    end = (150, endY)
    the_height = dist.euclidean(start, end) / pixelsPerMetric
    print(f"The min height is --> {the_height}")
    min_height = the_height
    

    cv.line(plotimg, (0, startY), (width, startY), (0, 0, 255), 2)
    cv.line(plotimg, (0, endY), (width, endY), (0, 255, 0), 2)

    cv.imwrite(f"{saveFolder}/line.jpg", plotimg)
    
    print(f"cd:{0.4}")
    sys.stdout.flush()

    ## -------------------------------------Plotting Ends here---------------------------------


## -----------------------------paths ---------------------------------------------

outputName = "output"
directory = os.path.dirname(os.path.abspath(outputName))
outputPath = os.path.join(directory, outputName)
os.makedirs(outputPath, exist_ok=True)
imgPath = "./src/assets/IMG_00016.JPG" # use during development
# imgPath = "./resources/app/src/assets/IMG_00016.JPG"  # use during build
saveFolderName = "save_folder"
saveFolder = os.path.join(outputPath, saveFolderName)
savePath = f"{saveFolder}/outImgOut.jpg"
imgMain = cv.imread(imgPath)
imgFile = imgMain.copy()
imgCustom = imgMain.copy()
full_width = 0
max_height = 0
min_height = 0
img_shape = imgMain.shape
pixelsPerMetric = 0


# --------------------------aurco marker detect and ppm calculate and crop-------------------------
def arucoSetup():
    global pixelsPerMetric, imgFile, imgCustom
    dict = arucoClass.main()
    # cv.imwrite("imgFile.jpg", imgFile)
    arucoLen = dict["id"]
    print(f"arucoLen: {arucoLen}")
    pixelsPerMetric = dict["ratio"]
    imgFile = imgFile[0 : img_shape[0], 0 : dict["bottom_right"][0] - 50]
    imgCustom = imgCustom[0 : img_shape[0], 0 : dict["bottom_right"][0] - 50]
    # cv.imwrite("imgCustom.jpg", imgCustom)

def getImg(path):
    """
    Reads the image
    """

    global imageTaken, imgPath, imgMain, imgFile, imgCustom
    try:
        # imageTaken = cv.imread(path)
        imgPath = path
        print(f"this is imgPath -> {imgPath}")
        imgMain = cv.imread(imgPath)
        imgFile = imgMain.copy()
        imgCustom = imgMain.copy()
        
        return Image.open(path)
        # imwrite("trimtest_temp.png", imageTaken, [int(IMWRITE_PNG_COMPRESSION), 5])

    except:
        print("Problem with image")


def TakeImg(path):
    return getImg(path)


def calculate():
    arucoSetup()
    custom_detect(imgCustom)

    print("this is the img for custom")
    # show_images(imgCustom)
    print("this is the passed img for snehil")
    # show_images(imgFile)

    # os.makedirs(tempFolder, exist_ok=True)
    # os.path.join(tempFolder, "temp.jpg")
    os.makedirs(saveFolder, exist_ok=True)
    print("save Folder at", saveFolder)
    writePath = os.path.join(saveFolder, "cropped_img.jpg")
    cv.imwrite(writePath, imgFile)
    detectMinGruve(imgFile)
    writeOutput(imgPath, outputPath, full_width, max_height, min_height)

