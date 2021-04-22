import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


def show_filled_boxes(survey_image_path):
    # ------------------------------------------- read survey image --------------------------------------------------
    survey_image = cv2.imread(survey_image_path)

    # ------------------------------------------- binarisation of image ----------------------------------------------
    gray_scale = cv2.cvtColor(survey_image, cv2.COLOR_BGR2GRAY)
    th1, survey_image_binary = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)
    survey_image_binary = ~survey_image_binary

    # ----------------------------------------- detect check boxes ---------------------------------------------------
    # specify approximate check box width relative to image width
    approx_check_box_width = math.floor(survey_image.shape[1] * 0.02)
    print(approx_check_box_width)
    # get image with horizontal lines
    horizontal_kernel = np.ones((1, approx_check_box_width - 10), np.uint8)
    vertical_kernal = np.ones((approx_check_box_width - 10, 1), np.uint8)
    # get image with vertical lines
    horizontal_lines_image = cv2.morphologyEx(survey_image_binary, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines_image = cv2.morphologyEx(survey_image_binary, cv2.MORPH_OPEN, vertical_kernal)
    # combine both images
    combined_lines_image = horizontal_lines_image | vertical_lines_image
    # add dilation to combined image to prevent broken check box images by making the image thicker
    combined_kernel = np.ones((3, 3), np.uint8)
    combined_lines_image = cv2.dilate(combined_lines_image, combined_kernel, iterations=1)
    # apply connected component analysis to detect connected image parts
    # output labels is a grayscale image of the source image with each connected part having a different gray scale
    # output stats describes all parts as a tuple with a list for each part containing x-postion, y-position,
    # width, height and area
    _, labels, stats, _ = cv2.connectedComponentsWithStats(~combined_lines_image, connectivity=8, ltype=cv2.CV_32S)
    # only check boxes from all detected boxes
    checkboxes = []
    for box in stats:
        box_width = box[2]
        box_height = box[3]
        if approx_check_box_width - 30 < box_height < approx_check_box_width + 30 and \
                approx_check_box_width - 30 < box_width < approx_check_box_width + 30:
            checkboxes.append(box)

    # ----------------------------------------- check box value detection -------------------------------------------
    # check amount of inc in each checkbox
    checked_boxes = []
    for checkbox in checkboxes:
        box_x_start = checkbox[0]
        box_x_end = checkbox[0] + checkbox[2]
        box_y_start = checkbox[1]
        box_y_end = checkbox[1] + checkbox[3]

        fill = 0
        for x in range(box_x_start, box_x_end):
            for y in range(box_y_start, box_y_end):
                fill += survey_image_binary[y][x]
        if fill / (checkbox[2] * checkbox[3]) > 35:
            checked_boxes.append(checkbox)

    # apply green box to source image for each check box
    for x, y, w, h, area in checked_boxes:
        cv2.rectangle(survey_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # plot image with recognized check boxes
    plt.imshow(survey_image)
    plt.show()
