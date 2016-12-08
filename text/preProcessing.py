import sys
import pandas
import math
import numpy as np
import tensorflow as tf
from tensorflow.contrib import learn
from tensorflow.python.framework import ops

ops.reset_default_graph()

# Start a graph session
sess = tf.Session()

# Load data from a csv file
csv_reader = pandas.read_csv('data/text/processed/samplePfizerText7Row.csv', sep=',',header=[1,2])
text_data = csv_reader.values


print("Total number of rows fetched: ", len(text_data))
text_input = []
target_output = []
max_block_length = 0
categories = []
category_blocks = {}

index = 0
for _, input, output in text_data:
    targets = [x for x in output.split(',') if x]
    for target in targets:
        text_input.append(input)
        if target not in categories:
            categories.append(target)
        category_index = categories.index(target)
        target_output.append(category_index)
        category_blocks[category_index].append(input)
    number_of_words_in_input = len(input.split(' '))
    if number_of_words_in_input > max_block_length:
        max_block_length = number_of_words_in_input


for category_index, text_blocks in category_blocks:
    print(category_index)
    print(len(text_blocks))
    sys.exit()

