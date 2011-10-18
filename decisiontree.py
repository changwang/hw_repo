#!/opt/python/bin/python

import math

"""
The input is a list of list, each item in the outer list is an example in training set, 
each item in the inner list is the value of cooresponding feature.
e.g:
    | F1 | F2 | F3 | Outcome |
eg1 | T  | F  | T  | A       |
eg2 | T  | T  | F  | B       | => [[F1, F2, F3, Outcome], [T, F, T, A], [T, T, F, B], [F, F, F, C]]
eg3 | F  | F  | F  | C       |

"""
class Node(object):
  """ 
  node represents a node in the decision tree.
  children holds all the branches starting from this node, 
  it is a list of dictionary, I want to use the key to indicate the value of the feature.
  """
  def __init__(self, *args):
    self.label = ''
    self.children = []
    
  def add_child(self, key, node):
    """ add a new child node to current node"""
    self.children.append({key: node})
  
  def __repr__(self):
    return self.label + '\t' + str(self.children)

def _log2(num):
  """ customized log2 function, because if num is 0, we want it to return 0 as well. """
  if num <= 0: return 0
  return math.log(num, 2)

def _entropy(values):
  """ calculates the entropy with given data. """
  denominator = len(values)
  entropy = 0.0
  categories = list(set(values)) # how many categories are here?

  for item in categories:
    count = len([v for v in values if v == item])
    p = float(count)/float(denominator)
    entropy += p * _log2(p)
    
  return -entropy

def _feature_entropy(features, size):
  """ 
  calculates features' entropy based on feed dictionary.
  size indicates the size of input examples
  """
  entropy = 0.0
  for key in features.keys():
    entropy += (float(len(features[key]))/size * _entropy(features[key]))

  return -entropy

def _info_gain(input, feature):
  """ 
  calculate the information gain based on the given training set and selected feature.
  the feature argument here is the index where it is in the input.
  """
  entropy = _entropy([eg[-1] for eg in input])  
  denominator = len(input)
  features = {}
  
  for eg in input:
    if eg[feature] in features:
      features[eg[feature]].append(eg[-1])
    else:
      features[eg[feature]] = [eg[-1],]
      
  return entropy + _feature_entropy(features, denominator)
  
def _filter(input, feature, value):
  """
  removes the examples out of the training set after finishing calcuating the given feature.
  it returns a new set.
  feature argument is the index of selected feature
  """
  copy = []
  
  for eg in input:
    if eg[feature] == value:
      copy.append(eg)
  
  return copy
  
def _best_feature(input, features):
  """ 
  cycles through all features and returns the attribute 
  with the highest information gain (or lowest entropy).
  features argument is a list contains all candidate features;
  exclusions argument is a list contains all the features have been visited;
  """
  best_gain = 0.0
  best_attr = -1
  
  for feat in features:
    gain = _info_gain(input, feat)
    if gain >= best_gain:
      best_gain = gain
      best_attr = feat
      
  return best_attr

def _best_feature_values(input, feature):
  """
  creates a list of values in the chosen feature for each record in input,
  prunes out all of the redundant values, and returns the list.
  """
  unique = []
  for eg in input:
    unique.append(eg[feature])
    
  return list(set(unique))
  
def _majority_value(input, target):
  """
  creates a list of all values in the target feature for each record
  in the data list object, and returns the value that appears in this list
  the most frequently.
  """
  lst = [eg[target] for eg in input]
  highest_freq = 0
  most_freq = None

  for val in list(set(lst)):
    if lst.count(val) > highest_freq:
      most_freq = val
      highest_freq = lst.count(val)

  return most_freq
  
def create_decision_tree(input, features, target, titles):
  """ returns a new decision tree based on the feeded examples. """
  data = input[:]
  vals = [eg[target] for eg in data]
  default = _majority_value(data, target)
  
  # if the dataset is empty or the features list is empty,
  # return the default value. 
  if not data or len(features) < 1:
    node = Node()
    node.label = default
    return node
  # if all the records in the dataset have the same classification,
  # returns that classification.
  elif vals.count(vals[0]) == len(vals):
    node = Node()
    node.label = vals[0]
    return node
  else:
    # choose the feature with max information gain
    best = _best_feature(data, features)
  
    node = Node()
    node.label = titles[best]
  
    f = features[:]
    f.remove(best)
    
    # creates a new decision tree/sub-node for each of the values in the features selected
    for val in _best_feature_values(data, best):
      subtree = create_decision_tree(_filter(data, best, val), f, target, titles)
      node.add_child(val, subtree)
   
    return node

ROOT = 5
INTENTATION = 17

def print_tree(tree, key='', depth=0):
  """ prints out the decision tree with readable format. """
  if tree is None:
    return
  else:
    if not depth:
      print " " * ROOT, tree.label
    else:
      print " " * (INTENTATION * (depth-1) + ROOT), "|-- (", key, ") -->", tree.label
    for pair in tree.children:
      for (key, val) in pair.items():
        print_tree(val, key, depth+1)


if __name__ == '__main__':
  titles = ['Deadline', 'Party', 'Lazy', 'Activity']
  training_set = [
    ['urgent', 'True',   'True',   'party'],
    ['urgent', 'False',  'True',   'study'],
    ['near',   'True',   'True',   'party'],
    ['none',   'True',   'False',  'party'],
    ['none',   'False',  'True',   'pub'  ],
    ['none',   'True',   'False',  'party'],
    ['near',   'False',  'False',  'study'],
    ['near',   'False',  'True',   'TV'   ],
    ['near',   'True',   'True',   'party'],
    ['urgent', 'False',  'False',  'study']
  ]

  titles2 = ['Alternate', 'Bar', 'Fri & Sat', 'Hungry', 'Patrons', 'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate', 'WillWait']
  training_set2 = [
    ['yes',  'no',   'no',   'yes',  'some', '$$$',  'no',   'yes',  'French',   '0-10',   'yes'],
    ['yes',  'no',   'no',   'yes',  'full', '$',    'no',   'no',   'Thai',     '30-60',  'no' ],
    ['no',   'yes',  'no',   'no',   'some', '$',    'no',   'no',   'Burger',   '0-10',   'yes'],
    ['yes',  'no',   'yes',  'yes',  'full', '$',    'yes',  'no',   'Thai',     '10-30',  'yes'],
    ['yes',  'no',   'yes',  'no',   'full', '$$$',  'no',   'yes',  'French',   '>60',    'no' ],
    ['no',   'yes',  'no',   'yes',  'some', '$$',   'yes',  'yes',  'Italian',  '0-10',   'yes'],
    ['no',   'yes',  'no',   'no',   'none', '$',    'yes',  'no',   'Burger',   '0-10',   'no' ],
    ['no',   'no',   'no',   'yes',  'some', '$$',   'yes',  'yes',  'Thai',     '0-10',   'yes'],
    ['no',   'yes',  'yes',  'no',   'full', '$',    'yes',  'no',   'Burger',   '>60',    'no' ],
    ['yes',  'yes',  'yes',  'yes',  'full', '$$$',  'no',   'yes',  'Italian',  '10-30',  'no' ],
    ['no',   'no',   'no',   'no',   'none', '$',    'no',   'no',   'Thai',     '0-10',   'no' ],
    ['yes',  'yes',  'yes',  'yes',  'full', '$',    'no',   'no',   'Burger',   '30-60',  'yes'],
  ]

  feats = range(len(training_set[0]))
  tree = create_decision_tree(training_set, feats[:-1], -1, titles)
  print_tree(tree)
