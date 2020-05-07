def clear(request):
	request = request.replace('.','')
	request = request.lower().strip()
	request2 = request
	request = request.replace("  ", " ")
	while request2 != request:
		request2 = request
		request = request.replace("  ", " ")
	return request

print(clear('  Ван       я  .'))