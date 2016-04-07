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



def ItemWeightedSum(points , user , neighborCount):
	numerator = 0
	denominator = 0
	for i in range(min(neighborCount , len(points))):
		# print "%f %d " %(points[i][0] , points[i][1])
		numerator += points[i][0] * matrix[user][points[i][1]] 
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



def UserWeightedSum(points , item , neighborCount):
	numerator = 0
	denominator = 0
	neighborCount = int(neighborCount)
	print "neighborCount %d " %(neighborCount)
	for i in range(min(neighborCount , len(points))):
		numerator += points[i][0] * matrix[points[i][1]][item]
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



#Item-Item Collaborative Filtering
def IICF(user , item , neighborCount):
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
	return ItemWeightedSum(d , user , neighborCount)



#User-User Collaborative Filtering
def UUCF(user , item , neighborCount):
	rated_users = []	#list of all users that have rated "item"
	for i in range(len(matrix)):
		if matrix[i][item] > 0 and i != user:
			rated_users.append( ( UserPearsonCorrelation(user , i) , i ) )
	rated_users.sort(reverse = True)
	return UserWeightedSum(rated_users , item , neighborCount)			




#The RandomGenerate function produces random points in the data matrix
def RandomGenerate():
	counter = 0
	file = open("testpoints" , "w")
	while counter < 100:
		print "counter %d" %(counter)
		x = int(random.random() * 500)
		y = int(random.random() * 500)
		if matrix[x][y] == 0:
			continue
		rating =  UUCF(x , y , 7)
		if rating >= 0.5:
			file.write(str(x) + " " + str(y) + "\n")
			counter += 1


def test(neighborCount):
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
		rating =  IICF(x , y , neighborCount)
		if rating >= 0.5:
			counter += 1
			r = int(rating)
			if rating - r >= 0.5:
				r += 1
			if abs(r - matrix[x][y]) <= 1:
				correct += 1
				output_file.write("0\n")
			else:
				output_file.write("1\n")
				incorrect += 1
		else:
			invalid += 1
	# ecfile.write(str(int(neighborCount)) + " " + str(int(incorrect)) + "\n")
	incorrect += correct
	correct *= 100
	if incorrect > 0:
		print "Accuracy Percentage %f" %(correct / incorrect)

def linetest(neighborCount , ecfile):
	correct = float(0)
	incorrect = float(0)
	counter = 0
	invalid = 0
	input_file = open("testpoints" , "r")
	for line in input_file:
		points = map(int , line.split(' '))
		x = points[0]
		y = points[1]
		rating =  IICF(x , y , neighborCount)
		if rating >= 0.5:
			counter += 1
			r = int(rating)
			if rating - r >= 0.5:
				r += 1
			if abs(r - matrix[x][y]) <= 1:
				correct += 1
			else:
				incorrect += 1
		else:
			invalid += 1
	ecfile.write(str(int(neighborCount)) + " " + str(int(incorrect)) + "\n")
	incorrect += correct
	correct *= 100
	if incorrect > 0:
		print "Accuracy Percentage %f" %(correct / incorrect)
		return (correct / incorrect)


def linegraph():
	#vary neighborhood of KNN algorithm
	neighborCount = 20
	cnt = 7
	ans = 0
	ecfile = open("ecfile" , "w")
	for i in xrange(1 , neighborCount + 1):
		x = linetest(i , ecfile)
		if x > ans:
			ans = x
			cnt = i 
	ecfile.close()
	test(cnt)

def main():
	read()
	metrics()
	RandomGenerate()
	linegraph()
	
	


if __name__ == '__main__':
	main()
