# enter your python code here
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Function to extract MFCC features from an audio file
def extract_mfcc(audio_file, num_mfcc=13):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=num_mfcc)
    return mfccs.T

# Example audio files (replace these with your own files)
sound_clip1 = 'sound1.wav'
sound_clip2 = 'sound2.wav'

# Extract MFCC features from both sound clips
mfcc1 = extract_mfcc(sound_clip1)
mfcc2 = extract_mfcc(sound_clip2)

# Reshape the MFCC features for classification
X = np.vstack((mfcc1, mfcc2))
y = np.hstack((np.zeros(len(mfcc1)), np.ones(len(mfcc2))))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple classifier (Random Forest as an example)
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Predict labels for the test set
y_pred = classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Determine if the two sound clips are spoken by the same person based on accuracy
if accuracy > 0.5:
    print("The two sound clips are likely spoken by the same person.")
else:
    print("The two sound clips are likely spoken by different persons.")
