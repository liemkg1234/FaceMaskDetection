import io

import numpy as np
import cv2
from PIL import Image
import pandas as pd
import base64


def draw_bboxs(img, xxyy_pandas, color_mask, color_0mask, thickness):
    for index, row in xxyy_pandas.iterrows():
        xmin = int(row['xmin'])
        ymin = int(row['ymin'])
        xmax = int(row['xmax'])
        ymax = int(row['ymax'])
        conf = round(row['confidence']*100, 1)
        start_p = (xmin,ymin)
        end_p = (xmax,ymax)
        #bbox mask
        if row['name'] == 'mask':
            img = cv2.rectangle(img, start_p, end_p, color_mask, thickness)
            # Class + conf
            img = cv2.putText(img, 'Mask: '+str(conf) + "%", (xmin, ymin - 5), 0, 0.5, color_mask)
        #bbox no_mask
        elif row['name'] == 'no_mask':
            img = cv2.rectangle(img, start_p, end_p, color_0mask, thickness)
            #Class + conf
            img = cv2.putText(img, 'No_mask: '+str(conf)+ "%", (xmin, ymin - 5), 0, 0.5, color_0mask)

    return img

def non_max_suppression_fast(xxyy_pandas, overlapThresh): #pandas
    if xxyy_pandas.empty:
        return xxyy_pandas
    labels = list(xxyy_pandas['name'])
    boxes = []
    for index, row in xxyy_pandas.iterrows():
        xmin = float(row['xmin'])
        ymin = float(row['ymin'])
        xmax = float(row['xmax'])
        ymax = float(row['ymax'])
        conf = float(row['confidence'])
        cls = float(row['class'])
        boxes += [[xmin, ymin, xmax, ymax, conf, cls]]
    boxes = np.asarray(boxes, dtype=np.float32)
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return pd.DataFrame()
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    #
    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type

    final_labels = [labels[idx] for idx in pick]
    final_boxes = boxes[pick].astype("float")

    #create dframe
    cols = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']
    df = pd.DataFrame(final_boxes, columns=cols)
    df['class'] = df['class'].astype('int')
    df['name'] = final_labels
    return df

