import random
import math
import time
import numpy

#voted contains list of all items that a user has rated
voted = {}

#list of ID's of all users

matrix = [[0 for _ in range(1700)] for _ in range(1000)]
avg_item_rating = []
avg_user_rating = []

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


#Returns similarity between two items that a user has rated
def ItemPearsonCorrelation(xitem , yitem):
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

#Returns similarity between two users 
def UserPearsonCorrelation(xuser , yuser):
	numerator = 0
	fden = 0
	sden = 0
	for i in range(len(matrix[0])):
		if matrix[xuser][i] > 0 and matrix[yuser][i] > 0:
			a  = (matrix[xuser][i] - avg_user_rating[xuser])
			fden += a * a
			b = (matrix[yuser][i] - avg_user_rating[yuser])
			sden += b * b
			numerator += a * b

	fden = math.sqrt(fden)
	sden = math.sqrt(sden)
	denominator = fden * sden
	if denominator == 0:
		return 0
	return (numerator / denominator)



def ItemWeightedSum(points , user , neighbourCount):
	numerator = 0
	denominator = 0
	for i in range(min(neighbourCount , len(points))):
		# print "%f %d " %(points[i][0] , points[i][1])
		numerator += points[i][0] * matrix[user][points[i][1]] 
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



def UserWeightedSum(points , item , neighbourCount):
	numerator = 0
	denominator = 0
	neighbourCount = int(neighbourCount)
	print "neighbourCount %d " %(neighbourCount)
	for i in range(min(neighbourCount , len(points))):
		numerator += points[i][0] * matrix[points[i][1]][item]
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



#Item-Item Collaborative Filtering
def IICF(user , item , neighbourCount):
	#Predict rating for user "user" for item "item"
	#iterate over all items that user has voted upon
	d = []
	for j in range(len(matrix[user])):
		if j != item and matrix[user][j] > 0:
			d.append( (ItemPearsonCorrelation(j , item) , j) )
		#append a tuple <distance , iid>
	# print ("movies voted by %d is %d" %(user , len(d)) )
	d.sort(reverse = True)
	# print d
	return ItemWeightedSum(d , user , neighbourCount)



#User-User Collaborative Filtering
def UUCF(user , item , neighbourCount):
	rated_users = []	#list of all users that have rated "item"
	for i in range(len(matrix)):
		if matrix[i][item] > 0 and i != user:
			rated_users.append( ( UserPearsonCorrelation(user , i) , i ) )
	rated_users.sort(reverse = True)
	return UserWeightedSum(rated_users , item , neighbourCount)			




#The test function produces random points in the data matrice and predicts the rating that the algorithm would give it and compares it to the actual rating
#Prediction is considered to be accurate if it has a maximum absolute error of 1
def Randomtest(neighbourCount):
	correct = float(0)
	incorrect = float(0)
	counter = 0
	invalid = 0
	file = open("testpoints" , "w")
	while counter < 100:
		print "counter %d" %(counter)
		x = int(random.random() * 500)
		y = int(random.random() * 500)
		if matrix[x][y] == 0:
			continue
		rating =  UUCF(x , y , neighbourCount)
		if rating >= 0.5:
			counter += 1
			# print "before %f" %(rating)
			r = int(rating)
			if rating - r >= 0.5:
				r += 1
			f = 0
			# print "Predicting %d %d" %(x , y)
			# print "Predicted %d Actual %d " %(r , matrix[x][y])
			if abs(r - matrix[x][y]) == 0:
				correct += 1
				f = 1
				# print "correct found"
			else:
				incorrect += 1
			file.write(str(x) + " " + str(y) + " " + str(f) + "\n")
		else:
			invalid += 1
	print str(neighbourCount) + " " + str(incorrect) + "\n"
	# ecfile.write(str(int(neighbourCount)) + " " + str(int(incorrect)) + "\n")
	incorrect += correct
	correct *= 100
	if incorrect > 0:
		print "Accuracy Percentage %f" %(correct / incorrect)
	# print "Invalid entries %d" %(invalid)



def test(neighbourCount):
	correct = float(0)
	incorrect = float(0)
	counter = 0
	invalid = 0
	input_file = open("testpoints" , "r")
	output_file = open("predictions.txt" , "w")
	for line in input_file:
		points = map(int , line.split(' '))
		x = points[0]
		y = points[1]
		output_file.write( str(x) + " " + str(y) + " " )
		rating =  UUCF(x , y , neighbourCount)
		if rating >= 0.5:
			counter += 1
			r = int(rating)
			if rating - r >= 0.5:
				r += 1
			if abs(r - matrix[x][y]) == 0:
				correct += 1
				output_file.write("0\n")
			else:
				output_file.write("1\n")
				incorrect += 1
		else:
			invalid += 1
	# ecfile.write(str(int(neighbourCount)) + " " + str(int(incorrect)) + "\n")
	incorrect += correct
	correct *= 100
	if incorrect > 0:
		print "Accuracy Percentage %f" %(correct / incorrect)

def linegraph():
	#vary neighbourhood of KNN algorithm
	neighbourCount = 20
	ecfile = open("ecfile" , "w")
	for i in xrange(1 , neighbourCount + 1):
		test(i , ecfile)
	ecfile.close()

def main():
	read()
	metrics()
	# linegraph()
	test(5)
	
	


if __name__ == '__main__':
	main()
