from .colordescriptor import ColorDescriptor
import glob
import cv2
from mysite.settings import MEDIA_URL

blog_dir = "media_cdn/blog"
expose_dir = "media_cdn/expose"
directories = [blog_dir, expose_dir]
output_dir = "index.csv"


def create():
    cd = ColorDescriptor((8, 12, 3))
    # open the output index file for writing
    output = open(output_dir, "w")
    # use glob to grab the image paths and loop over them
    for directory in directories:
        for imagePath in glob.glob(directory + "/*/*.*g"):
            # extract the image ID (i.e. the unique filename) from the image
            # path and load the image itself
            imageID = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            # describe the image
            features = cd.describe(image)
            #correct the url
            imagePath = imagePath.replace("media_cdn/", MEDIA_URL)
            print(imagePath)
            print(imageID)
            # write the features to file
            features = [str(f) for f in features]
            output.write("%s,%s\n" % (imagePath, ",".join(features)))
    # close the index file
    output.close()

# $ python createdataset.py --dataset media_cdn/blog --index index.csv

