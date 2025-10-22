import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import matplotlib.pyplot as plt

# Load the quiz data
df = pd.read_csv("quiz_dataset.csv")
question_cols = [f"Q{i+1}" for i in range(20)]

# Encode answers
answer_map = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3}
for col in question_cols:
    df[col] = df[col].astype(str).str.strip().str.capitalize()
    df[col] = df[col].map(answer_map)
    
df.dropna(subset=question_cols,inplace=True)

# Process multi-label targets
df['labels'] = df['labels'].fillna('').apply(lambda x: x.split(',') if x else [])
df = df[df['labels'].map(len) > 0]
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['labels'])

# X = df.drop(columns=['labels'])
X = df[question_cols]
print("Shape of X:", X.shape)
print("First few rows of X:\n", X.head())
print("Shape of y:", y.shape)
print("First few rows of y:\n", y[:5])

# Train model
base_model = RandomForestClassifier(n_estimators=100, random_state=42)
model = OneVsRestClassifier(base_model)
model.fit(X, y)

# Save model and label encoder
joblib.dump(model, 'model.pkl')
joblib.dump(mlb, 'label_binarizer.pkl')
print("✅ Model and label_binarizer saved successfully.")

all_labels = [label for sublist in df['labels'] for label in sublist]
pd.Series(all_labels).value_counts().plot(kind='bar', title='Disorder Frequency')
plt.tight_layout()
plt.show()