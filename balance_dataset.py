import pandas as pd
import random

# Disorders we want to add
new_disorders = [
    'stress', 'self-esteem', 'grief', 'bipolar', 'ocd', 'adhd',
    'eating-disorder', 'addiction', 'loneliness', 'panic attack', 'daydreaming'
]

# Answer levels (simulate realistic user answers)
answer_levels = ['Never', 'Rarely', 'Sometimes', 'Often']

def generate_random_entry(disorder):
    # Simulate pattern variations for each disorder
    if disorder == 'stress':
        answers = ['Often', 'Often', 'Sometimes', 'Often', 'Often', 'Sometimes', 'Rarely', 'Often', 'Sometimes', 'Often']
    elif disorder == 'self-esteem':
        answers = ['Rarely', 'Sometimes', 'Rarely', 'Rarely', 'Sometimes', 'Rarely', 'Rarely', 'Sometimes', 'Rarely', 'Rarely']
    elif disorder == 'grief':
        answers = ['Sometimes', 'Rarely', 'Rarely', 'Never', 'Sometimes', 'Rarely', 'Sometimes', 'Never', 'Sometimes', 'Sometimes']
    elif disorder == 'bipolar':
        answers = ['Often', 'Rarely', 'Often', 'Rarely', 'Often', 'Rarely', 'Often', 'Rarely', 'Often', 'Rarely']
    elif disorder == 'ocd':
        answers = ['Often', 'Often', 'Rarely', 'Often', 'Often', 'Often', 'Often', 'Rarely', 'Often', 'Often']
    elif disorder == 'adhd':
        answers = ['Often', 'Sometimes', 'Often', 'Rarely', 'Often', 'Sometimes', 'Often', 'Rarely', 'Often', 'Sometimes']
    elif disorder == 'eating-disorder':
        answers = ['Sometimes', 'Often', 'Sometimes', 'Sometimes', 'Often', 'Rarely', 'Sometimes', 'Rarely', 'Often', 'Sometimes']
    elif disorder == 'addiction':
        answers = ['Often', 'Often', 'Sometimes', 'Often', 'Often', 'Often', 'Rarely', 'Often', 'Often', 'Often']
    elif disorder == 'loneliness':
        answers = ['Sometimes', 'Rarely', 'Sometimes', 'Sometimes', 'Sometimes', 'Rarely', 'Sometimes', 'Rarely', 'Sometimes', 'Sometimes']
    elif disorder == 'panic attack':
        answers = ['Often', 'Often', 'Rarely', 'Often', 'Often', 'Sometimes', 'Often', 'Sometimes', 'Often', 'Often']
    elif disorder == 'daydreaming':
        answers = ['Often', 'Sometimes', 'Often', 'Sometimes', 'Often', 'Sometimes', 'Often', 'Often', 'Sometimes', 'Often']
    else:
        answers = random.choices(answer_levels, k=10)

    padded = answers + random.choices(answer_levels, k = 10)
    return padded + [disorder]

# Create the new data entries
new_rows = []
for disorder in new_disorders:
    for _ in range(5):
        new_rows.append(generate_random_entry(disorder))

# Create DataFrame
columns = [f"Q{i+1}" for i in range(20)] + ["labels"]
new_df = pd.DataFrame(new_rows, columns=columns)

# Load the original dataset and append new entries
original_df = pd.read_csv("quiz_dataset.csv")
combined_df = pd.concat([original_df, new_df], ignore_index=True)

# Drop duplicates
combined_df = combined_df.drop_duplicates()

# Save the balanced dataset
combined_df.to_csv("quiz_dataset.csv", index=False)
print("✅ Added balanced entries for missing disorders.")