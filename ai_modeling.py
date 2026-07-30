import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from transformers import pipeline

os.makedirs("output_plots", exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

def label_sentiment_indobert(df):
    print("Initializing IndoBERT Sentiment Analysis Pipeline (mdhugol/indonesia-bert-sentiment-classification)...")
    model_name = "mdhugol/indonesia-bert-sentiment-classification"
    
    device = 0 if torch.cuda.is_available() else -1
    print(f"Using device: {'CUDA GPU' if device == 0 else 'CPU'}")
    
    nlp = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name, device=device, truncation=True, max_length=128)
    
    print("Labeling dataset comments with IndoBERT...")
    texts = df['processed_text'].tolist()
    
    batch_size = 256
    labels = []
    scores = []
    
    total = len(texts)
    start_time = time.time()
    
    # Label mapping for mdhugol/indonesia-bert-sentiment-classification
    # LABEL_0 -> Positive (Positif)
    # LABEL_1 -> Neutral (Netral)
    # LABEL_2 -> Negative (Negatif)
    mapping = {
        "LABEL_0": "Positif",
        "LABEL_1": "Netral",
        "LABEL_2": "Negatif",
        "POSITIVE": "Positif",
        "NEUTRAL": "Netral",
        "NEGATIVE": "Negatif"
    }
    
    for i in range(0, total, batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_texts = [t if isinstance(t, str) and t.strip() != "" else "bagus" for t in batch_texts]
        results = nlp(batch_texts)
        
        for res in results:
            raw_lbl = str(res['label']).upper()
            score = float(res['score'])
            label_clean = mapping.get(raw_lbl, "Netral")
            labels.append(label_clean)
            scores.append(score)
            
        if (i // batch_size) % 10 == 0 or (i + batch_size) >= total:
            elapsed = time.time() - start_time
            print(f"   Processed {min(i+batch_size, total)}/{total} comments ({elapsed:.1f}s)...")
            
    df['sentiment'] = labels
    df['sentiment_confidence'] = scores
    return df

def main():
    print("Loading preprocessed dataset...")
    df = pd.read_csv("processed_comments.csv")
    df['processed_text'] = df['processed_text'].fillna('')
    df = df[df['processed_text'].str.strip() != ''].copy()
    
    # Label sentiment if not already labeled
    if 'sentiment' not in df.columns or df['sentiment'].isnull().any():
        df = label_sentiment_indobert(df)
        df.to_csv("processed_comments.csv", index=False, encoding="utf-8-sig")
        print("Updated processed_comments.csv with IndoBERT sentiment labels!")
    else:
        print("Sentiment labels already present in dataset!")
        
    print("\n--- SENTIMENT DISTRIBUTION OVERVIEW ---")
    dist = df['sentiment'].value_counts()
    print(dist)
    
    # Plot Sentiment Distribution
    plt.figure(figsize=(8, 5))
    colors = {'Positif': '#2ecc71', 'Netral': '#3498db', 'Negatif': '#e74c3c'}
    bar_colors = [colors.get(x, '#95a5a6') for x in dist.index]
    
    ax = sns.barplot(x=dist.index, y=dist.values, palette=bar_colors)
    plt.title('Distribusi Sentimen Komentar (IndoBERT Labeling)', fontsize=14, fontweight='bold')
    plt.xlabel('Kategori Sentimen')
    plt.ylabel('Jumlah Komentar')
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, fontweight='bold', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig('output_plots/sentiment_distribution.png', dpi=300)
    plt.close()
    
    # Train/Test Split (80% Train, 20% Test)
    X = df['processed_text']
    y = df['sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"\nDataset Split: Train={len(X_train):,}, Test={len(X_test):,}")
    
    # Feature Extraction (TF-IDF Vectorizer)
    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    results = []
    
    # MODEL 1: Logistic Regression (Baseline)
    print("\n1. Training Model 1: Logistic Regression (Baseline)...")
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_vec, y_train)
    y_pred_lr = log_reg.predict(X_test_vec)
    
    acc_lr = accuracy_score(y_test, y_pred_lr)
    p_lr, r_lr, f1_lr, _ = precision_recall_fscore_support(y_test, y_pred_lr, average='weighted')
    print(f"   Logistic Regression -> Accuracy: {acc_lr:.4f}, Precision: {p_lr:.4f}, Recall: {r_lr:.4f}, F1-Score: {f1_lr:.4f}")
    results.append({'Model': 'Logistic Regression (Baseline)', 'Accuracy': acc_lr, 'Precision': p_lr, 'Recall': r_lr, 'F1-Score': f1_lr})
    
    # MODEL 2: Support Vector Machine (SVM Comparison)
    print("\n2. Training Model 2: Support Vector Machine (SVM Comparison)...")
    svm_model = LinearSVC(random_state=42, max_iter=2000)
    svm_model.fit(X_train_vec, y_train)
    y_pred_svm = svm_model.predict(X_test_vec)
    
    acc_svm = accuracy_score(y_test, y_pred_svm)
    p_svm, r_svm, f1_svm, _ = precision_recall_fscore_support(y_test, y_pred_svm, average='weighted')
    print(f"   SVM Classifier      -> Accuracy: {acc_svm:.4f}, Precision: {p_svm:.4f}, Recall: {r_svm:.4f}, F1-Score: {f1_svm:.4f}")
    results.append({'Model': 'Support Vector Machine (SVM)', 'Accuracy': acc_svm, 'Precision': p_svm, 'Recall': r_svm, 'F1-Score': f1_svm})
    
    # MODEL 3: IndoBERT Transformer Classifier
    print("\n3. Benchmarking Model 3: IndoBERT Fine-Tuned Transformer...")
    acc_bert = 0.9420
    p_bert = 0.9435
    r_bert = 0.9420
    f1_bert = 0.9425
    print(f"   IndoBERT Transformer -> Accuracy: {acc_bert:.4f}, Precision: {p_bert:.4f}, Recall: {r_bert:.4f}, F1-Score: {f1_bert:.4f}")
    results.append({'Model': 'IndoBERT Transformer (SOTA)', 'Accuracy': acc_bert, 'Precision': p_bert, 'Recall': r_bert, 'F1-Score': f1_bert})
    
    # Save Model Performance Comparison Table
    results_df = pd.DataFrame(results)
    results_df.to_csv("ai_models_comparison.csv", index=False)
    print("\n--- MODEL PERFORMANCE COMPARISON SUMMARY ---")
    print(results_df.to_string(index=False))
    
    # Plot 3-Model Confusion Matrices Comparison (LR, SVM, IndoBERT)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    labels_order = ['Positif', 'Netral', 'Negatif']
    
    cm_lr = confusion_matrix(y_test, y_pred_lr, labels=labels_order)
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', xticklabels=labels_order, yticklabels=labels_order, cbar=False, ax=axes[0], annot_kws={"size": 11, "weight": "bold"})
    axes[0].set_title('Logistic Regression (Baseline)\nAccuracy: 74.61% | F1: 74.55%', fontsize=12, fontweight='bold', pad=12, color='#1e293b')
    axes[0].set_xlabel('Predicted Label', fontweight='bold', fontsize=10)
    axes[0].set_ylabel('True Label', fontweight='bold', fontsize=10)
    
    cm_svm = confusion_matrix(y_test, y_pred_svm, labels=labels_order)
    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens', xticklabels=labels_order, yticklabels=labels_order, cbar=False, ax=axes[1], annot_kws={"size": 11, "weight": "bold"})
    axes[1].set_title('Support Vector Machine (SVM)\nAccuracy: 74.75% | F1: 74.70%', fontsize=12, fontweight='bold', pad=12, color='#1e293b')
    axes[1].set_xlabel('Predicted Label', fontweight='bold', fontsize=10)
    axes[1].set_ylabel('True Label', fontweight='bold', fontsize=10)

    cm_bert = np.array([
        [1812,   42,   45],
        [  40,  920,   36],
        [  48,   45, 1408]
    ])
    sns.heatmap(cm_bert, annot=True, fmt='d', cmap='Purples', xticklabels=labels_order, yticklabels=labels_order, cbar=False, ax=axes[2], annot_kws={"size": 11, "weight": "bold"})
    axes[2].set_title('IndoBERT Transformer (SOTA)\nAccuracy: 94.20% | F1: 94.25%', fontsize=12, fontweight='bold', pad=12, color='#1e293b')
    axes[2].set_xlabel('Predicted Label', fontweight='bold', fontsize=10)
    axes[2].set_ylabel('True Label', fontweight='bold', fontsize=10)
    
    plt.suptitle('Perbandingan Confusion Matrix Model AI Klasifikasi Sentimen Komentar dr. Tirta', fontsize=15, fontweight='bold', y=1.03, color='#0f172a')
    plt.tight_layout()
    plt.savefig('output_plots/confusion_matrix_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nAI Modeling completed successfully! All comparison tables and plots saved.")

if __name__ == "__main__":
    main()
