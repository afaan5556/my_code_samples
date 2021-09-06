'''
I often incorporate this function into my data-wrangling scripts to
hit an API with all elements in a list, or one or more dataframe
series while limiting each call to a certain payload limit
'''

API_RESPONSES = {}

def recursive_api_call(request_series, payload_limit):
	'''
	request_series: The list or pandas dataframe column (series)
	payload_limit: The limit to under which a single call should be kept
	'''
	if len(request_series) > payload_limit:
		hit_api(request_series[:payload_limit])
		recursive_api_call(request_series[payload_limit:], payload_limit)
	else:
		hit_api(request_series)


def hit_api(request_series):
	'''
	request_series: The sub-set of request_series that is under the payload limit
	return: none, instead the global API_RESPONSES dictionary is updated with a
	key (request) and value (response) pair
	'''
	for i in list(request_series):
		try:
			# API request code here
			# Save response in a variable response
			API_RESPONSES[i] = response
		except:
			print('An exception occurred')