import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


def logistic_regression(terminal):
	# Load the datasets
	multitask = pd.read_csv('../Data/multitask.csv').assign(Label=-1)
	bmi = pd.read_csv('../Data/bmi.csv').assign(Label=1)

	# Concatenate the datasets
	df = pd.concat([multitask, bmi])

	terminal.write_text("df size: "+str(df.shape))

	# Separate features and target
	X = df.iloc[:, :-1]
	y = df.iloc[:, -1]

	terminal.write_text("X:"+ str(X.shape))

	# Create a scaler object
	scaler = MinMaxScaler(feature_range=(-1, 1))

	#sc_x = scaler.fit_transform(X)
	X = scaler.fit_transform(X)
	terminal.write_text("X_train size: "+str(len(X[0])))

	# Convert the target into binary categories
#	y = pd.cut(y, bins=[y.min(), y.median(), y.max()], include_lowest=True, labels=[0, 1])

	# Split the data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	# Create a Logistic Regression model
	model = LogisticRegression(max_iter=1000)

	# Train the model
	model.fit(X_train, y_train)

	# Evaluate the model
	train_score = model.score(X_train, y_train)
	test_score = model.score(X_test, y_test)

	terminal.write_text("Training accuracy: ", train_score)
	terminal.write_text("Testing accuracy: ", test_score)
	return model 
