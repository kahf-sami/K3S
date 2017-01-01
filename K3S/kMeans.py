import tensorflow as tf
from random import choice, shuffle
import numpy
import sys
import math
import pickle
from .file import File
from .config import Config

class KMeans():


    def __init__(self, identifier, numberOfClusters = 2, iteration = 1):
        self.config = Config()
        self.identifier = identifier
        self.numberOfClusters =  numberOfClusters
        self.numberOfVectors = 0
        self.vectorDimension = 0
        self.vectors = None
        self.iteration = iteration
        self.path = File.join(self.config.DATA_PATH, self.identifier, 'kmeans.plk')
        self.centroids = None
        self.assignments = None
        return


    def getCentroids(self):
        return self.centroids


    def getAssignments(self):
        return self.assignments


    def setVectors(self, matrix):
        matrix = matrix.todense()
        #print(matrix.shape)

        index = 0
        self.vectors = []
        for column in range(matrix.shape[1]):
            vector = matrix[:, column]
            vector = numpy.array(vector.T)
            self.vectors.append(vector[0])
            index += 1

        self.vectorDimension = len(self.vectors[0])
        self.numberOfVectors = len(self.vectors)
        #print(self.vectorDimension)
        #print(self.numberOfVectors)
        return


    def setNumberClusters(self, numberOfClusters):
        self.numberOfClusters =  numberOfClusters
        return


    def isValidVectors(self):
        if self.numberOfClusters < self.numberOfVectors:
            return False

        return True


    def computeCluster(self):
        self.centroids = None
        self.assignment = None

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

            self.centroids = sess.run(centroids)
            self.assignments = sess.run(assignments)

        return self.centroids, self.assignments


    def save(self):
        file = File(self.path)
        file.remove()
        file.write(pickle.dumps(self), 'wb')
        return


    @classmethod
    def restore(cls, identifier):
        config = Config()
        path = File.join(config.DATA_PATH, identifier, 'kmeans.plk')
        file = File(path)
        if file.exists():
            return pickle.loads(file.read('rb'))
        return KMeans(identifier)


