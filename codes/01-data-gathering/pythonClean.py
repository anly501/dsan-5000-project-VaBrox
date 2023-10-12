import requests
import pandas as pd
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


url = "http://ergast.com/api/f1/2020/5/pitstops"
output_file = "pitstops_data.xml"  # Specify the name of the output file

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open the output file in binary write mode and write the response content
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"Data downloaded and saved to {output_file}")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

# Load the XML data into a string
with open('/Users/kai/pitstops_data.xml', 'r') as f:
    xml_data = f.read()

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Find the PitStopsList node
    pitstops_list = root.find('.//{http://ergast.com/mrd/1.5}PitStopsList')

    # Extract the information from each PitStop node and store it in a list of dictionaries
    pitstops = []
    for pitstop in pitstops_list.findall('.//{http://ergast.com/mrd/1.5}PitStop'):
        pitstop_dict = {}
        pitstop_dict['driverId'] = pitstop.get('driverId')
        pitstop_dict['stop'] = pitstop.get('stop')
        pitstop_dict['lap'] = pitstop.get('lap')
        pitstop_dict['time'] = pitstop.get('time')
        pitstop_dict['duration'] = pitstop.get('duration')
        pitstops.append(pitstop_dict)


    # Print the list of dictionaries
    df = pd.DataFrame(pitstops)

 # write to csv
df.to_csv('pitstops.csv', index=False)

df = pd.read_csv("pitstops.csv")

# Convert 'lap' column to string because we're using it with CountVectorizer
df['lap'] = df['lap'].astype(str)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['lap'], df['duration'], test_size=0.2, random_state=42)

# Vectorize the data using CountVectorizer
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Linear Regression model
regressor = LinearRegression()
regressor.fit(X_train_vec, y_train)

# Predict on test data
y_pred = regressor.predict(X_test_vec)

# Evaluate the regressor
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))





