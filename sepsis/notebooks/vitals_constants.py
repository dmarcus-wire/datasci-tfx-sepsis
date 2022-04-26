
NUMERICAL_FEATURES = ['HR', 'Resp', 'Temp']

# Keys
LABEL_KEY = 'isSepsis'

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
