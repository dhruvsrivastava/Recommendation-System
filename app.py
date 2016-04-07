from flask import Flask , render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ratings')
def ratings():
	file = open('u.data' , 'r')
	rating = [0 , 0 , 0 , 0 , 0]
	for line in file:
		# print line
		data = map(int , line.split('	'))
		# print data
		rating[data[2] - 1] += 1
	return render_template('ratings.html' , data = map(json.dumps , rating))

@app.route('/KNN')
def KNN():
	file = open("ecfile" , "r")
	ec = []
	for line in file:
		data = map(int , line.split(' '))
		ec.append(data[1])
	return render_template('linegraph.html' , data = map(json.dumps , ec))

@app.route('/testpoints')
def testpoints():
	testpoints = []
	file = open("testpoints" , "r")
	for line in file:
		points = map(int , line.split(' '))
		testpoints.append(points[0])
		testpoints.append(points[1])
	return render_template('scatterplot.html' , data = map(json.dumps , testpoints))


@app.route('/predictions')
def predictions():
	testpoints = []
	correct = 0
	file = open("predictions.txt" , "r")
	for line in file:
		points = map(int , line.split(' '))
		testpoints.append(points[0])
		testpoints.append(points[1])
		testpoints.append(points[2])
		if points[2] == 0:
			correct += 1
	return render_template('predictions.html' , data = map(json.dumps , testpoints) , correct = correct)


@app.route('/d3')
def d3():
	data = [5 , 10 , 15 , 20 , 25]
	return render_template('d3.html' , data =  map(json.dumps , data) )

if __name__ == '__main__':
	app.run(debug = True)
