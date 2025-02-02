# -*- coding: utf-8 -*-
"""ML Project2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14hWjG-P96e4mtev9dUhC4UOvH2Ewegr6
"""

# Mohamed Omar Ahmed 20201154 (S7,8)
# Omar Salama Mostafa 20200344 (S7,8)
# Belal Mohamed Soliman 20200115 (S7,8)
# Rawda Mohammad Hussein 20201074 (S5,6)
# Haneen Ehdaa Ibrahim 20200163 (S5,6)

import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from google.colab import drive

# Load the training dataset
trainData = pd.read_csv("/content/mnist_train.csv")

print("The training data before nothing\n\n", trainData)

# Identify the number of classes for training data
numberOfClasses = trainData['label'].nunique()
print("The number of unique classes of column label in the mnist_train data: ", numberOfClasses)

# Identify the number of features for training data
numberOfFeatures = trainData.shape[1] - 1
print("The number of features in the mnist_train data: ", numberOfFeatures)

# Check for missing values for training data
print("\nThe missing values in the training data:\n")
print(trainData.isnull().sum())

if trainData.isnull().sum().any():
    print(f"\nThe train data has {trainData.isnull().sum().sum()} missing values \n")
else:
    print("\nThe train data has not missing values \n")

# Data types of training data
dataTypes = trainData.dtypes
print("\nThe data types of columns: \n")
print(dataTypes)

# Separate features and target

features = trainData.drop('label', axis=1)
print("Features: \n", features)

target = trainData['label']
print("\nTarget: \n", target)

# Normalize the features
featuresNormalized = features / 255.0

# Resize the features
featuresResized = featuresNormalized.values.reshape(-1, 28, 28)

# Visualize some resized images
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.imshow(featuresResized[i], cmap='gray')
    plt.title(f"Label: {target.iloc[i]}")
    plt.axis('off')
plt.show()

# Split features into train and test
featuresTrain, featuresValidation, targetTrain, targetValidation = train_test_split(featuresNormalized, target, test_size=0.2, random_state=42)

# Define the knn with grid search
knn = KNeighborsClassifier()
parametersGrid = {'n_neighbors': [3, 5, 7]}

gridSearch = GridSearchCV(knn, parametersGrid, cv=3, n_jobs=-1)
gridSearch.fit(featuresTrain, targetTrain)

bestK = gridSearch.best_params_['n_neighbors']

knn = KNeighborsClassifier(n_neighbors=bestK)
knn.fit(featuresTrain, targetTrain)

knnAccuracy = knn.score(featuresValidation, targetValidation)
print(f"KNN Accuracy on Validation Set: {knnAccuracy}")

# Define the first architecture
first_architecture = keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(784,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(numberOfClasses, activation='softmax')
])

# Compile the first architecture
first_architecture.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

# Train the first architecture
first_architecture.fit(featuresTrain, targetTrain, batch_size=64, epochs=10, validation_data=(featuresValidation, targetValidation))

# Define the second architecture
second_architecture = keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(784,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(numberOfClasses, activation='softmax')
])

# Compile the second architecture
second_architecture.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

# Train the second architecture
second_architecture.fit(featuresTrain, targetTrain, batch_size=64, epochs=10, validation_data=(featuresValidation, targetValidation))

# Calculate first architecture accuracy
first_arch_accuracy = first_architecture.evaluate(featuresValidation, targetValidation)[1]
print("First Architecture Accuracy: ", first_arch_accuracy)

# Calculate second architecture accuracy
second_arch_accuracy = second_architecture.evaluate(featuresValidation, targetValidation)[1]
print("Second Architecture Accuracy: ", second_arch_accuracy)

# Compare the outcomes of the first and second experiments
if knnAccuracy > first_arch_accuracy and knnAccuracy > second_arch_accuracy:
    print("K-NN is the best model.")
    best_model = knn

elif first_arch_accuracy > knnAccuracy and first_arch_accuracy > second_arch_accuracy:
    print("ANN First Architecture is the best model.")
    best_model = first_architecture

elif second_arch_accuracy > first_arch_accuracy and second_arch_accuracy > knnAccuracy:
    print("ANN Second Architecture is the best model.")
    best_model = second_architecture

elif first_arch_accuracy == second_arch_accuracy == knnAccuracy:
    print("The three models have the same accuracy")
    best_model = first_architecture

# Confusion matrix of the best model.
best_m_pred = best_model.predict(featuresValidation)
prediction = np.argmax(best_m_pred, axis=1)
confusion_matrix = confusion_matrix(targetValidation, prediction)
print(confusion_matrix)

# Visualize the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=[str(i) for i in range(numberOfClasses)],
            yticklabels=[str(i) for i in range(numberOfClasses)])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Save the best model
if best_model == knn:
    joblib.dump(best_model, 'best_knn_model.joblib')
else:
    best_model.save('best_neural_network_model.h5')

# Load the test dataset
testData = pd.read_csv("/content/mnist_test.csv")
print("\nThe test data before nothing\n\n", testData)

# Identify the number of classes for testing data
numberOfClasses = testData['label'].nunique()
print("The number of unique classes of column label in test data: ", numberOfClasses)

# Identify the number of features for testing data
numberOffeatures = testData.shape[1] - 1
print("The number of features of test data: ", numberOffeatures)

# Check for missing values for testing data
print("\nThe missing values in the test data: \n")
print(testData.isnull().sum())

if testData.isnull().sum().any():
    print(f"The test data have {testData.isnull().sum().sum()} missing values \n")
else:
    print("\nThe test data have not missing values \n")

# Data types of testing data
dataTypes = testData.dtypes
print("\nThe data types of columns of test data:\n")
print(dataTypes)

# Separate features and target
features = testData.drop('label', axis=1)
print("\nFeatures of test data: \n", features)

target = testData['label']
print("\nTarget of test data: \n", target)

# Normalize the features for testing data
X_normalized = features / 255.0

# Reload the best model for testing
if best_model == knn:
    loadedModel = joblib.load('best_knn_model.joblib')
else:
    loadedModel = keras.models.load_model('best_neural_network_model.h5')

# Test the model on the testing data
if best_model == knn:
    testAccuracy = loadedModel.score(X_normalized, target)
    print("KNN ", end='')

else:
    y_pred_prob_test = loadedModel.predict(X_normalized)
    y_pred_test = np.argmax(y_pred_prob_test, axis=1)
    testAccuracy = np.mean(y_pred_test == target)
    print("ANN ", end='')

print(f"Accuracy on Test Set: {testAccuracy}")