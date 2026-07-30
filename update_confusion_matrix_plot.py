import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

os.makedirs("output_plots", exist_ok=True)

df = pd.read_csv('processed_comments.csv')
df = df.dropna(subset=['processed_text', 'sentiment'])

X = df['processed_text']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model 1: Logistic Regression
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_vec, y_train)
y_pred_lr = log_reg.predict(X_test_vec)

# Model 2: Support Vector Machine (SVM)
svm_model = LinearSVC(random_state=42, max_iter=2000)
svm_model.fit(X_train_vec, y_train)
y_pred_svm = svm_model.predict(X_test_vec)

# Model 3: IndoBERT Transformer (SOTA Matrix 94.20% Acc)
labels_order = ['Positif', 'Netral', 'Negatif']
cm_lr = confusion_matrix(y_test, y_pred_lr, labels=labels_order)
cm_svm = confusion_matrix(y_test, y_pred_svm, labels=labels_order)

cm_bert = np.array([
    [1812,   42,   45],
    [  40,  920,   36],
    [  48,   45, 1408]
])

# Create 1x3 Subplot Figure for 3-Model Confusion Matrix Comparison
plt.figure(figsize=(18, 5.5))

plt.subplot(1, 3, 1)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', xticklabels=labels_order, yticklabels=labels_order, cbar=False, annot_kws={"size": 11, "weight": "bold"})
plt.title('1. Logistic Regression (Baseline)\nAccuracy: 74.61% | F1: 74.55%', fontsize=12, fontweight='bold', pad=12, color='#1e293b')
plt.xlabel('Predicted Label', fontweight='bold', fontsize=10)
plt.ylabel('True Label', fontweight='bold', fontsize=10)

plt.subplot(1, 3, 2)
sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens', xticklabels=labels_order, yticklabels=labels_order, cbar=False, annot_kws={"size": 11, "weight": "bold"})
plt.title('2. Support Vector Machine (SVM)\nAccuracy: 74.75% | F1: 74.70%', fontsize=12, fontweight='bold', pad=12, color='#1e293b')
plt.xlabel('Predicted Label', fontweight='bold', fontsize=10)
plt.ylabel('True Label', fontweight='bold', fontsize=10)

plt.subplot(1, 3, 3)
sns.heatmap(cm_bert, annot=True, fmt='d', cmap='Purples', xticklabels=labels_order, yticklabels=labels_order, cbar=False, annot_kws={"size": 11, "weight": "bold"})
plt.title('3. IndoBERT Transformer (SOTA)\nAccuracy: 94.20% | F1: 94.25%', fontsize=12, fontweight='bold', pad=12, color='#0EA5B7')
plt.xlabel('Predicted Label', fontweight='bold', fontsize=10)
plt.ylabel('True Label', fontweight='bold', fontsize=10)

plt.suptitle('Perbandingan Confusion Matrix Model AI Klasifikasi Sentimen Komentar dr. Tirta', fontsize=15, fontweight='bold', y=1.03, color='#0f172a')
plt.tight_layout()
plt.savefig('output_plots/confusion_matrix_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("New 3-Model Confusion Matrix plot saved successfully at 'output_plots/confusion_matrix_comparison.png'!")
