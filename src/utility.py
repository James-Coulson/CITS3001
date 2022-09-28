
def clamp(n, minn, maxn):
	"""
	This function is used to clamp the vlaue of n within the specified minimum and maximum

	Paramters:
		n: Number to be clamped
		minn: Minimum bound of n
		maxn: Maximum bound of n

	Returns:
		The clamped value of n
	"""
	return max(min(maxn, n), minn)
