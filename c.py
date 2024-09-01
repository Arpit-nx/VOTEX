
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

# # Load data
# data = pd.read_csv('your_dataset.csv')

# # Preprocess data (example)
# X = data.drop('target_column', axis=1)
# y = data['target_column']

# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Normalize data
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)
# from sklearn.linear_model import LogisticRegression

# # Initialize the model
# model = LogisticRegression()

# # Train the model
# model.fit(X_train, y_train)
# import tensorflow as tf
# from tensorflow.keras import layers, models

# # Build a simple neural network
# model = models.Sequential([
#     layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(1, activation='sigmoid')  # For binary classification
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
# # Evaluate the model
# accuracy = model.score(X_test, y_test)
# print(f'Accuracy: {accuracy:.2f}')
# test_loss, test_acc = model.evaluate(X_test, y_test)
# print(f'Test Accuracy: {test_acc:.2f}')
# predictions = model.predict(X_test)
# predictions = model.predict(X_test)


# # import phonenumbers
# # from Mynum import number
# # from phonenumbers import geocoder

# # pepnumber = phonenumbers.parse(number)
# # location = geocoder.description_for_number(pepnumber,"en")
# # # print(location)
# import phonenumbers
# import opencage
# import folium
# from Mynum import number
# from phonenumbers import geocoder

# pepnumber = phonenumbers.parse(number)
# location = geocoder.description_for_number(pepnumber,"en")
# print(location)

# from phonenumbers import carrier

# service = phonenumbers .parse(number)
# print(carrier.name_for_number(service,"en"))

# from opencage.geocoder import OpenCageGeocode

# key = '8ae55ac957fe443c96ec4a877cb03c44'

# geocoder = OpenCageGeocode(key)
# query = str(location)
# results = geocoder.geocode(query)

# print(results)
# lat = results[0]['geometry']['lat']
# lng = results[0]['geometry']['lng']

# myMap = folium.Map(location=[lat,lng], zoom_start = 9)
# folium.Marker([lat,lng], popup=location).add_to(myMap)
# myMap.save("mylocation.html")