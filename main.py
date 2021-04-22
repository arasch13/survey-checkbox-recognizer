from functions import *
import os

# survey folder
folder_containing_surveys = "./surveys/"

# get all file names in folder
filenames = [f for f in os.listdir(folder_containing_surveys)
             if os.path.isfile(os.path.join(folder_containing_surveys, f))]

# show filled boxes for each survey image
for filename in filenames:
    survey_image_path = f"{folder_containing_surveys}{filename}"
    show_filled_boxes(survey_image_path)
