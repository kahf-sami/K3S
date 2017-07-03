import tensorflow as tf
import mnist_input_data as inputRawData
import sys

mnist = inputRawData.read_data_sets("/tmp/data/", one_hot=True)
print('Total : ' + str(mnist.train.num_examples))

# Set parameters
learningRate = 0.01
trainingIteration = 30
batchSize = 500
displayStep = 2


# TF graph input
inputData = tf.placeholder("float", [None, 784]) # MNIST data image of shape 28*28=784
outputCategory = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes

# Create a model
	 
# Set model weights
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
	 

# Construct a linear model
model = tf.nn.softmax(tf.matmul(inputData, W) + b) # Softmax

# Minimize error using cross entropy
# Cross entropy
costFunction = -tf.reduce_sum(outputCategory*tf.log(model))

# Gradient Descent
optimizer = tf.train.GradientDescentOptimizer(learningRate).minimize(costFunction)
	 
# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
	sess.run(init)

	# Training cycle
	for iteration in range(trainingIteration):
		avgCost = 0
		totalBatch = int(mnist.train.num_examples/batchSize)

		# Loop over all batches
		for i in range(batchSize):
			batchInputs, batchOutputs = mnist.train.next_batch(batchSize)
			#print('----------in----------------')
			#print(batchInputs)
			#print('------------out--------------')
			#print([batchOutputs])

			# Fit training using batch data
			sess.run(optimizer, feed_dict={inputData: batchInputs, outputCategory: batchOutputs})

			# Compute average loss
			avgCost += sess.run(costFunction, feed_dict={inputData: batchInputs, outputCategory: batchOutputs})/totalBatch

			# Display logs per eiteration step
			if iteration % displayStep == 0:
				print("Iteration:", '%04d' % (iteration + 1), "cost=", "{:.9f}".format(avgCost))

		print("Tuning completed!")

		# Test the model
		predictions = tf.equal(tf.argmax(model, 1), tf.argmax(outputCategory, 1))

		print('Predicted: ')
		print(tf.argmax(model, 1).eval({inputData: mnist.test.images, outputCategory: mnist.test.labels}))
		print('Accurate: ')
		print(tf.argmax(outputCategory, 1).eval({inputData: mnist.test.images, outputCategory: mnist.test.labels}))

		# Calculate accuracy
		accuracy = tf.reduce_mean(tf.cast(predictions, "float"))
		print("Accuracy:", accuracy.eval({inputData: mnist.test.images, outputCategory: mnist.test.labels}))
