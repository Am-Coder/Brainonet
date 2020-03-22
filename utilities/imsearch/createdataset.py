from .colordescriptor import ColorDescriptor
import glob
import cv2
from mysite.settings import MEDIA_URL
from expose.models import Expose
from blog.models import Blog

blog_dir = "media_cdn/blog"
expose_dir = "media_cdn/expose"
directories = [blog_dir, expose_dir]
output_dir = "index.csv"


def create_with_fileio():
    cd = ColorDescriptor((8, 12, 3))
    # open the output index file for writing
    output = open(output_dir, "w")
    # use glob to grab the image paths and loop over them
    for directory in directories:
        for imagePath in glob.glob(directory + "/*/*.*g"):
            # extract the image ID (i.e. the unique filename) from the image
            # path and load the image itself
            image = cv2.imread(imagePath)
            # describe the image
            features = cd.describe(image)
            # correct the url
            url = imagePath.replace("media_cdn/", MEDIA_URL)
            # write the features to file
            features = [str(f) for f in features]
            output.write("%s,%s\n" % (url, ",".join(features)))
    # close the index file
    output.close()


def create_with_db():
    expose = Expose.objects.filter(approved=False)
    blogs = Blog.objects.filter(approved=False)
    if blogs:
        make_csv(blogs, 'a')
    if expose:
        make_csv(expose, 'a')


def make_csv(objects, mode):
    cd = ColorDescriptor((8, 12, 3))
    output = open(output_dir, mode)
    for obj in objects:
        obj.approved = True
        url = obj.image.url
        imagePath = url.replace(MEDIA_URL, "media_cdn/")
        imagePath = imagePath.replace("%20", " ")

        image = cv2.imread(imagePath)
        # describe the image
        features = cd.describe(image)
        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (url, ",".join(features)))
        obj.save()
    output.close()

# $ python createdataset.py --dataset media_cdn/blog --index index.csv
