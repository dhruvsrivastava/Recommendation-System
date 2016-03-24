import random
import math
import time
import numpy

#voted contains list of all items that a user has rated
voted = {}

#list of ID's of all users

matrix = [[0 for _ in range(1700)] for _ in range(1000)]
avg_item_rating = []

def read():
	starting_time = time.time()
	data = []
	with open("u.data" , "r") as file:
		for line in file :
			n = line.split('\t')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[1])
			d['rating'] = int(n[2])

			assert(d['uid'] <= 1000)
			assert(d['iid'] <= 1700)

			matrix[d['uid']][d['iid']] = d['rating']

			# if d['uid'] not in voted:
			# 	voted[d['uid']] = []
			# voted[d['uid']].append(d['iid'])
			# data.append(d)


	# for i in range(len(data)):
	# 	print data[i]
	# print "max uid %d max iid %d" %(max_uid , max_iid)
	ending_time = time.time()

	print ("time taken is %f"  %(ending_time - starting_time))
	# print "length of data %d" %(len(data))


	# for i in range(10):
	# 	for j in range(10):
	# 		print matrix[i][j] , 
	# 	print ""

def metrics():
	avg_user_rating = []
	for i in range(len(matrix)):
		sum = 0
		n = 0
		for j in range(len(matrix[i])):
			if matrix[i][j] > 0:
				sum += matrix[i][j];
				n += 1
		if n > 0:
			avg_user_rating.append(float(sum) / float(n))
		else:
			avg_user_rating.append(0)

	# for i in range(len(avg_user_rating)):
	# 	if avg_user_rating[i] > 0:
	# 		print "user %d rating %f" %(i , avg_user_rating[i])
	
	
	for j in range(len(matrix[i])):
		sum = 0
		n = 0
		for i in range(len(matrix)):
			if matrix[i][j] > 0:
				sum += matrix[i][j]
				n += 1
		if n > 0:
			sum = sum / float(n)
		avg_item_rating.append(sum)

	# for i in range(len(avg_item_rating)):
	# 	if avg_item_rating[i] > 0:
	# 		print "item %d rating %f" %(i , avg_item_rating[i])

def PearsonCorrelation(xitem , yitem):
	numerator = 0
	fden = 0
	sden = 0
	for i in range(len(matrix)):
		if matrix[i][xitem] > 0 and matrix[i][yitem] > 0:
			a  = (matrix[i][xitem] - avg_item_rating[xitem])
			fden += a * a
			b = (matrix[i][yitem] - avg_item_rating[yitem])
			sden += b * b
			numerator += a * b

	fden = math.sqrt(fden)
	sden = math.sqrt(sden)
	denominator = fden * sden
	if denominator == 0:
		return 0
	return (numerator / denominator)


def WeightedSum(points , user):
	numerator = 0
	denominator = 0
	for i in range(min(30 , len(points))):
		# print "%f %d " %(points[i][0] , points[i][1])
		numerator += points[i][0] * matrix[user][points[i][1]] 
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator

#Item-Item Collaborative Filtering
def IICF(user , item):
	#Predict rating for user "user" for item "item"

	#iterate over all items that user has voted upon
	d = []
	for j in range(len(matrix[user])):
		if j != item and matrix[user][j] > 0:
			d.append( (PearsonCorrelation(j , item) , j) )
		#append a tuple <distance , iid>
	# print ("movies voted by %d is %d" %(user , len(d)) )
	d.sort(reverse = True)
	# print d
	return WeightedSum(d , user)

def test():
	correct = float(0)
	incorrect = float(0)
	counter = 0
	while counter < 100:
		# print "counter %d" %(counter)
		x = int(random.random() * 500)
		y = int(random.random() * 500)

		if matrix[x][y] == 0:
			continue
		rating =  IICF(x , y)
		if rating >= 1:
			counter += 1
			r = int(rating)
			print "Predicting %d %d" %(x , y)
			print "Predicted %d Actual %d " %(r , matrix[x][y])
			if abs(r - matrix[x][y]) <= 1:
				correct += 1
				# print "correct found"
			else:
				incorrect += 1

	incorrect += correct
	if incorrect > 0:
		print "Accuracy %f" %(correct / incorrect)


read()
metrics()
test()
