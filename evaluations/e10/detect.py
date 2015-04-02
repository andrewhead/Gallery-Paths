"""
Platform-independent module for locating faces in images and determining whether they
are the same faces from one iteration to the next.
"""

import numpy as np
import cv2
import time


INVALID_CLASS = -1


def get_color(image, rect):
    ''' Compute the average color of a rectangle in an image. '''
    left, top, width, height = rect
    patch = image[top:top+height,left:left+width]
    color = np.average(patch, axis=(0,1))
    return color


class Visitor(object):
    ''' Stores information about a visitor and when they were last sighted. '''

    def __init__(self, index, scolor, last_seen):
        self.index = index
        self.scolor = scolor
        self.last_seen = last_seen


class ShirtRecognizer(object):

    COLOR_MATCH = 20  # Closeness of clothing color for person to be considered the same

    def __init__(self, decay=None):
        ''' Create a new shirt recognizer.
            decay = amount of time between sightings before we forget a visitor. '''
        self.class_counter = 0
        self.visitors = []
        self.decay = decay
        
    def add_visitor(self, color, time):
        visitor = Visitor(index=self.class_counter, scolor=color, last_seen=time)
        self.class_counter += 1
        self.visitors.append(visitor)
        return visitor

    def classify(self, image, shirt):
        ''' Classify image as being a person based on colors of clothing. '''

        # Find the color of clothing
        shirt_color = get_color(image, shirt)

        # Find the closest matching color
        best_dist = 1000000 # This can be any arbitrary large number
        best_class = INVALID_CLASS
        visitor = None
        for v in self.visitors:
            matches, color_dist = self.match(shirt_color, v)
            if matches and color_dist < best_dist:
                visitor = v
                best_dist = color_dist
                best_class = v.index

        # Log a new color if it hasn't been seen before.
        if best_class == INVALID_CLASS:
            visitor = self.add_visitor(shirt_color, 0)
            best_class = visitor.index

        visitor.last_seen = time.time()

        return best_class

    def get_shirt(self, image, face, ratio=.75, heads_below=1.5):
        ''' Get box around center of shirt. Return None if the the box containing the shirt is
            out of bounds or of 0 in size'''

        ih, iw, _ = image.shape
        fl, ft, fw, fh = face

        # Compute prediction of shirt location
        width, height = (int(fw * ratio), int(fh * ratio))
        top = ft + fh + int(heads_below * fh)
        left = fl + int((fw - width) / 2)

        # Move shirt within image bounds if it's outside
        top = ih if top > ih else 0 if top < 0 else top
        left = iw if left > iw else 0 if left < 0 else left
        bottom = min(top + height, ih)
        right = min(left + width, iw)
        width = right - left
        height = bottom - top

        # Return the bounding box of the shirt we found
        if width == 0 or height == 0:
            return None
        return [left, top, right - left, bottom - top]

    def match(self, color, visitor):
        ''' Determine whether a color found matches a past visitor. '''
        color_dist = np.average(np.abs(color - visitor.scolor))
        if not self.decay or (self.decay and time.time() - visitor.last_seen <= self.decay):
            visitor_recent = True
        else:
            visitor_recent = False
        matches = color_dist <= self.COLOR_MATCH and visitor_recent
        return matches, color_dist


class FaceRecognizer(object):

    NEIGHBORS_NEEDED = 5
    DETECT_SCALING_FACTOR = 1.1
    TRAINING_DATA = 'lbpcascade_frontalface.xml'

    def __init__(self, decay=None):
        ''' Prepare face classifier. '''
        self.face_cascade = cv2.CascadeClassifier()
        self.face_cascade.load(self.TRAINING_DATA)
        self.shirt_recognizer = ShirtRecognizer(decay)

    def find_faces(self, image):
        ''' Find all faces in an image. '''
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(grey, self.DETECT_SCALING_FACTOR, self.NEIGHBORS_NEEDED)
        id_faces = []
        for face in faces:
            shirt = self.shirt_recognizer.get_shirt(image, face)
            classId =  INVALID_CLASS if shirt is None else self.shirt_recognizer.classify(image, shirt)
            id_faces.append(tuple(face) + (classId,))
        return id_faces

