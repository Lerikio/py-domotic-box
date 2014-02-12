import RadioTransceiver

rxtx = RadioTransceiver.RadioTransceiver()
rxtx.start()

start = [(1,250),(0,2500)]
end = [(1,250),(0,10000)]
one = [(1,250),(0,1250),(1,250),(0,250)]
zero = [(1,250),(0,250),(1,250),(0,1250)]

def convertToSequence(binSequence):
	sequence = []
	sequence.extend(start)
	for char in binSequence:
		if char == '1': sequence.extend(one)
		elif char == '0': sequence.extend(zero)
	sequence.extend(end)
	return sequence


binSequence = '0000 0000 0000 0000 0000 0000 1101 0000'

for i in range(200):
	rxtx.addToWriteBuffer(convertToSequence(binSequence))
