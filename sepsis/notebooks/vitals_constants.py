
# dropped MAP need to handle NaN
NUMERICAL_FEATURES = ['HR','Temp','Resp', 'isSepsis']

# Number of buckets used by tf.transform for encoding each feature.
FEATURE_BUCKET_COUNT = 10

# Keys
LABEL_KEY = 'isSepsis'

print(LABEL_KEY)

def t_name(key):
  """
  Rename the feature keys so that they don't clash with the raw keys when
  running the Evaluator component.
  Args:
    key: The original feature key
  Returns:
    key with '_xf' appended
  """
  return key + '_xf'
