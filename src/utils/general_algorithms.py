import math as m 

def binary_search(target, array, func=None):
	'''
		Searches for the target in the array either using the function specified
		or by performing default comparison (i.e., comparing target with element of array).
		Returns the index of the target if it is found, otherwise returns (-(insertion point) - 1).
	'''
	if func is None:
		func = default_comparison

	return binary_search_recursive(target, array, 0, len(array) - 1, func)

def default_comparison(value, target):
	if (target < value):
		return -1
	elif (value == target):
		return 0
	else:
		return 1
	
def binary_search_recursive(target, array, low, high, func):
	if (low > high): return -1 * low - 1

	mid = m.floor((high + low) / 2)

	result = func(array[mid], target)
	if (result < 0):
		return binary_search_recursive(target, array, low, mid - 1, func)
	elif (result == 0):
		return mid
	else:
		return binary_search_recursive(target, array, mid + 1, high, func)