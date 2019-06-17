import os
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
from sklearn.decomposition import PCA
import numpy as np
import random
import pickle
from scipy.spatial import distance
from igraph import *
from PIL import Image, ImageDraw
import sys
import argparse


def load_image(path):
    img = image.load_img(path, target_size=model.input_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

# get concatenated images
def get_concatenated_images(input_img_name, output_img_name, indexes, thumb_height):
    thumbs = []
    img = Image.open(input_img_name)
    img = img.convert('RGB')
    img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
    thumbs.append(img)
    for idx in indexes:
        img = Image.open(images[idx])
        img = img.convert('RGB')
        img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
        thumbs.append(img)
    img = Image.open(output_img_name)
    img = img.convert('RGB')
    img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
    thumbs.append(img)
    concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)
    return concat_image



parser = argparse.ArgumentParser(description="Get Image Path")

parser.add_argument("-i", "--input", dest="input", help="Input image path", default='')
parser.add_argument("-o", "--output", dest="output", help="Output image path", default='')
args = parser.parse_args()

inputImgName = args.input.split(',')[:-1]
outputImgName = 'public/images/' + args.output

for name in inputImgName:
    print(name)
    print(type(name))

print(outputImgName)

model = keras.applications.VGG16(weights='imagenet', include_top=True)
feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)

output_img, y = load_image(outputImgName)
output_feat = feat_extractor.predict(y)[0]
feature = []

for name in inputImgName:
    filepath = 'public/images/' + name
    print(filepath)
    input_img, x = load_image(filepath)
    print(type(input_img))
    # put the image into the feature prediction model
    # the model is the same as the model we first loaded but removed the last layer

    input_feat = feat_extractor.predict(x)[0]
    feature.append(input_feat)

feature.append(output_feat)


images, pca_features, pca = pickle.load(open('features_caltech256.p', 'rb'))

feature = np.array(feature)
pca_new_feature = pca.transform(feature)

print(pca_features.shape)
print(pca_new_feature.shape)

similar_idx = [ distance.cosine(pca_new_feature[-1], feat) for feat in pca_features ]
idx2 = sorted(range(len(similar_idx)), key=lambda k: similar_idx[k])[0]

# output_closest_img = image.load_img(images[idx2])
# output_closest_img.save('output_closest.jpg')

_ , graph = pickle.load(open('graph_caltech256_30knn.p', 'rb'))

for i, new_feature in enumerate(pca_new_feature[:-1]):
    similar_idx = [ distance.cosine(new_feature, feat) for feat in pca_features ]
    idx1 = sorted(range(len(similar_idx)), key=lambda k: similar_idx[k])[0]

    # input_closest_img = image.load_img(images[idx1])
    # input_closest_img.save('input_closest.jpg')


    # run get_shortest_paths
    path = graph.get_shortest_paths(idx1, to=idx2, mode=OUT, output='vpath', weights='weight')[0]

    # retrieve the images, concatenate into one, and display them
    results_image = get_concatenated_images('public/images/' + inputImgName[i], outputImgName, path, 200)

    img = Image.fromarray(results_image)
    img.save('public/images/result_%d.jpg' % i)