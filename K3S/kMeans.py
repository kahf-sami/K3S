import tensorflow as tf
from random import choice, shuffle
import numpy
import sys
import math
#from functions import *

class KMeans():


    def __init__(self, identifier, numberOfClusters = 2, iteration = 1):
        self.identifier = identifier
        self.numberOfClusters =  numberOfClusters
        self.numberOfVectors = 0
        self.vectorDimension = 0
        self.vectors = None
        self.iteration = iteration
        return


    def setVectors(self, matrix):
        matrix = matrix.todense()

        self.vectors = []
        for row in range(matrix.shape[0]):
            vector = numpy.array(matrix[row][0])
            self.vectors.append(vector[0])
        
        self.vectorDimension = len(self.vectors[0])
        self.numberOfVectors = len(self.vectors)
        return


    def setNumberClusters(self, numberOfClusters):
        self.numberOfClusters =  numberOfClusters
        return


    def isValidVectors(self):
        if self.numberOfClusters < self.numberOfVectors:
            return False

        return True


    def computeCluster(self):
        vectorIndices = list(range(self.numberOfVectors))
        shuffle(vectorIndices)

        graph = tf.Graph()
        with graph.as_default():
            sess = tf.Session()

            centroids = []
            centroidValue = tf.placeholder("float64", [self.vectorDimension])
            centAssigns = []
            for i in range(self.numberOfClusters):
                centroid = tf.Variable(self.vectors[vectorIndices[i]])
                centroids.append(centroid)
                centAssigns.append(tf.assign(centroid, centroidValue))

            assignments = []
            assignmentValue = tf.placeholder("int32")
            clusterAssigns = []
            for i in range(self.numberOfVectors):
                assignment = tf.Variable(0)
                assignments.append(assignment)
                clusterAssigns.append(tf.assign(assignment, assignmentValue))

            meanInput = tf.placeholder("float", [None, self.vectorDimension])
            meanOperation = tf.reduce_mean(meanInput, 0)

            v1 = tf.placeholder("float", [self.vectorDimension])
            v2 = tf.placeholder("float", [self.vectorDimension])
            euclideanDistances = tf.sqrt(tf.reduce_sum(tf.pow(tf.sub(v1, v2), 2)))

            centroidDistances = tf.placeholder("float", [self.numberOfClusters])
            clusterAssignment = tf.argmin(centroidDistances, 0)

            initOperation = tf.initialize_all_variables()

            sess.run(initOperation)

            for i in range(self.iteration):
                for vectorIndex in range(self.numberOfVectors):
                    currentVector = self.vectors[vectorIndex]
                    
                    distances = []
                    for centroid in centroids:
                        centroiedVector = sess.run(centroid)
                        distances.append(sess.run(euclideanDistances, feed_dict={v1: currentVector, v2: centroiedVector}))

                    assignment = sess.run(clusterAssignment, feed_dict = {centroidDistances: distances})
                    sess.run(clusterAssigns[vectorIndex], feed_dict={assignmentValue: assignment})

                for clusterIndex in range(self.numberOfClusters):
                    assignedVectors = []
                    for vectorIndex in range(self.numberOfVectors):
                        if sess.run(assignments[vectorIndex]) == clusterIndex:
                            assignedVectors.append(self.vectors[vectorIndex])
                                
                    assignedVectors = numpy.array(assignedVectors)

                    newLocation = sess.run(meanOperation, feed_dict={meanInput: assignedVectors})
                    sess.run(centAssigns[clusterIndex], feed_dict={centroidValue: newLocation})

            centroids = sess.run(centroids)
            assignments = sess.run(assignments)

        return centroids, assignments



