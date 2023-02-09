import pandas as pd
import numpy as np
import re


def normalize_column_names(columns):
	'''
	Normalize column names.
	The following transformations will be applied:

	- Remove parenthesis and their content
	- Convert all letters to lower case
	- Replace whitespaces with underlines (' ' -> '_')
	- Remove leading/trailing whitespaces, tabs and newlines

	Args:
		columns: List of column names
	Return:
		List of normalized columns
	'''
	norm_columns = []

	for col in columns:
		col = re.sub('([a-z])([A-Z])', r'\1_\2', col)
		col = col.strip().lower().replace(' ', '_')
		col = re.sub('[^\w_]', r'', col)
		norm_columns.append(col)

	return norm_columns




def get_nan_values(data):
	c = []
	v = []
	n = []

	for col in data.columns:
		nn = data[col].isna().sum()

		if nn:
			c.append(col)
			v.append("{:.1f}%".format(nn*(100/len(data))))
			n.append(nn)

	return pd.DataFrame({"Name":c, "Nans": n, "Percent": v}).sort_values(
			by="Nans", ascending=False).set_index("Name")
