# Working with Bag of Words
#---------------------------------------
#
#
#
#
#
#
#

import sys
import pandas
import math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.contrib import learn
from tensorflow.python.framework import ops

ops.reset_default_graph()

# Start a graph session
sess = tf.Session()

# Load data from a csv file
csv_reader = pandas.read_csv('data/text/processed/sample0.csv', sep=',',header=[1,2])
text_data = csv_reader.values

print("Total number of rows fetched: ", len(text_data))
text_input = []
target_output = []
max_block_length = 0


for row in text_data:
    text_input.append(row[1])
    target_output.append(row[2])
    number_of_words_in_input = len(row[1].split(' '))
    if number_of_words_in_input > max_block_length:
        max_block_length = number_of_words_in_input


print("Total number of rows after extraction: ", len(target_output))
print("Max block length: ",  max_block_length)

# If a word appears in 50% of the document ignore it
min_word_freq = math.ceil(len(text_data) * 1 / 100)

print("Min word frequency: ", min_word_freq)

# Setup vocabulary processor
vocab_processor = learn.preprocessing.VocabularyProcessor(max_block_length, min_frequency=min_word_freq)

# Have to fit transform to get length of unique words.
vocab_processor.fit_transform(text_input)
embedding_size = len(vocab_processor.vocabulary_)
print('Embedding size:', embedding_size)

# Split up data set into train/test (80% - 20%)
train_indices = np.random.choice(len(text_input), round(len(text_input)*0.8), replace=False)
test_indices = np.array(list(set(range(len(text_input))) - set(train_indices)))
texts_train = [x for ix, x in enumerate(text_input) if ix in train_indices]
texts_test = [x for ix, x in enumerate(text_input) if ix in test_indices]
target_train = [x for ix, x in enumerate(target_output) if ix in train_indices]
target_test = [x for ix, x in enumerate(target_output) if ix in test_indices]

# Setup Index Matrix for one-hot-encoding
identity_mat = tf.diag(tf.ones(shape=[embedding_size]))

# Create variables for logistic regression
A = tf.Variable(tf.random_normal(shape=[embedding_size,1]))
b = tf.Variable(tf.random_normal(shape=[1,1]))

# Initialize placeholders
x_data = tf.placeholder(shape=[max_block_length], dtype=tf.int32)
y_target = tf.placeholder(shape=[1, 1], dtype=tf.float32)

# Text-Vocab Embedding
x_embed = tf.nn.embedding_lookup(identity_mat, x_data)
x_col_sums = tf.reduce_sum(x_embed, 0)

# Declare model operations
x_col_sums_2D = tf.expand_dims(x_col_sums, 0)
model_output = tf.add(tf.matmul(x_col_sums_2D, A), b)

# Declare loss function (Cross Entropy loss)
loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(model_output, y_target))

# Prediction operation
prediction = tf.sigmoid(model_output)

# Declare optimizer
my_opt = tf.train.GradientDescentOptimizer(0.001)
train_step = my_opt.minimize(loss)

# Intitialize Variables
init = tf.initialize_all_variables()
sess.run(init)

# Start Logistic Regression
print('Starting Training Over {} Sentences.'.format(len(texts_train)))
loss_vec = []
train_acc_all = []
train_acc_avg = []
for ix, t in enumerate(vocab_processor.fit_transform(texts_train)):
    y_data = [[target_train[ix]]]
    
    sess.run(train_step, feed_dict={x_data: t, y_target: y_data})
    temp_loss = sess.run(loss, feed_dict={x_data: t, y_target: y_data})
    loss_vec.append(temp_loss)
    
    if (ix+1)%10==0:
        print('Training Observation #' + str(ix+1) + ': Loss = ' + str(temp_loss))
    
    # Keep trailing average of past 50 observations accuracy
    # Get prediction of single observation
    [[temp_pred]] = sess.run(prediction, feed_dict={x_data:t, y_target:y_data})
    # Get True/False if prediction is accurate
    train_acc_temp = target_train[ix]==np.round(temp_pred)
    train_acc_all.append(train_acc_temp)
    if len(train_acc_all) >= 50:
        train_acc_avg.append(np.mean(train_acc_all[-50:]))

tf.train.SummaryWriter('bow', sess.graph)

# Get test set accuracy
print('Getting Test Set Accuracy For {} Sentences.'.format(len(texts_test)))
test_acc_all = []
for ix, t in enumerate(vocab_processor.fit_transform(texts_test)):
    y_data = [[target_test[ix]]]
    
    if (ix+1)%50==0:
        print('Test Observation #' + str(ix+1))
    
    # Keep trailing average of past 50 observations accuracy
    # Get prediction of single observation
    [[temp_pred]] = sess.run(prediction, feed_dict={x_data:t, y_target:y_data})
    # Get True/False if prediction is accurate
    test_acc_temp = target_test[ix]==np.round(temp_pred)
    test_acc_all.append(test_acc_temp)

print('\nOverall Test Accuracy: {}'.format(np.mean(test_acc_all)))


# Plot training accuracy over time
plt.plot(range(len(train_acc_avg)), train_acc_avg, 'k-', label='Train Accuracy')
plt.title('Avg Training Acc Over Past 50 Generations')
plt.xlabel('Generation')
plt.ylabel('Training Accuracy')
plt.show()

