import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

# Create directory for plots if not exists
os.makedirs("output_plots", exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'

def generate_ngrams(tokens_list, n=2):
    ngrams = []
    for tokens in tokens_list:
        if len(tokens) >= n:
            for i in range(len(tokens) - n + 1):
                ngram = " ".join(tokens[i:i+n])
                ngrams.append(ngram)
    return ngrams

def main():
    print("Loading preprocessed comments dataset...")
    df = pd.read_csv("processed_comments.csv")
    df['processed_text'] = df['processed_text'].fillna('')
    
    tokens_series = df['processed_text'].apply(lambda x: x.split())
    all_tokens = [token for tokens in tokens_series for token in tokens]
    
    print(f"Total vocabulary words extracted: {len(all_tokens):,}")
    
    # 1. Word Frequency Analysis
    word_counts = Counter(all_tokens)
    top_words = word_counts.most_common(20)
    top_words_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi'])
    top_words_df.to_csv("output_plots/top_words_frequency.csv", index=False)
    
    print("\n--- TOP 10 KATA PALING FREKUEN ---")
    for word, freq in top_words[:10]:
        print(f"{word:20s}: {freq:,}")
        
    # 2. N-Gram Analysis (Unigram, Bigram, Trigram)
    bigrams = generate_ngrams(tokens_series, n=2)
    trigrams = generate_ngrams(tokens_series, n=3)
    
    top_bigrams = Counter(bigrams).most_common(15)
    top_trigrams = Counter(trigrams).most_common(15)
    
    pd.DataFrame(top_bigrams, columns=['Bigram', 'Frekuensi']).to_csv("output_plots/top_bigrams.csv", index=False)
    pd.DataFrame(top_trigrams, columns=['Trigram', 'Frekuensi']).to_csv("output_plots/top_trigrams.csv", index=False)
    
    # 3. TF-IDF Analysis
    print("\nCalculating TF-IDF Matrix...")
    tfidf = TfidfVectorizer(max_features=50, ngram_range=(1, 2))
    tfidf_matrix = tfidf.fit_transform(df['processed_text'])
    feature_names = tfidf.get_feature_names_out()
    mean_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    
    tfidf_df = pd.DataFrame({'Term': feature_names, 'Mean_TFIDF': mean_tfidf})
    tfidf_df = tfidf_df.sort_values(by='Mean_TFIDF', ascending=False).reset_index(drop=True)
    tfidf_df.to_csv("output_plots/top_tfidf_features.csv", index=False)
    
    # 4. VISUALIZATION 1: Overall Word Cloud
    print("\nGenerating Word Cloud...")
    wc = WordCloud(
        width=1200, height=600,
        background_color='white',
        colormap='viridis',
        max_words=150,
        random_state=42
    ).generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud Keseluruhan Komentar YouTube dokter Tirta', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('output_plots/wordcloud_overall.png', dpi=300)
    plt.close()
    
    # 5. VISUALIZATION 2: N-gram Bar Charts
    print("Generating N-gram Bar Charts...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Bigrams Plot
    bg_df = pd.DataFrame(top_bigrams[:10], columns=['Bigram', 'Frekuensi'])
    sns.barplot(data=bg_df, y='Bigram', x='Frekuensi', palette='crest', ax=axes[0])
    axes[0].set_title('Top 10 Bigram Paling Sering Muncul', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Frekuensi')
    
    # Trigrams Plot
    tg_df = pd.DataFrame(top_trigrams[:10], columns=['Trigram', 'Frekuensi'])
    sns.barplot(data=tg_df, y='Trigram', x='Frekuensi', palette='viridis', ax=axes[1])
    axes[1].set_title('Top 10 Trigram Paling Sering Muncul', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Frekuensi')
    
    plt.tight_layout()
    plt.savefig('output_plots/barchart_ngrams.png', dpi=300)
    plt.close()
    
    # 6. VISUALIZATION 3: TF-IDF Bar Chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=tfidf_df.head(15), y='Term', x='Mean_TFIDF', palette='mako')
    plt.title('Top 15 Term Berdasarkan Skor Rata-rata TF-IDF', fontsize=14, fontweight='bold')
    plt.xlabel('Skor TF-IDF Rata-rata')
    plt.tight_layout()
    plt.savefig('output_plots/tfidf_top_features.png', dpi=300)
    plt.close()
    
    # 7. VISUALIZATION 4: Co-occurrence Network Graph
    print("Generating Co-occurrence Network Graph...")
    # Get top 20 bigrams to construct network graph
    G = nx.Graph()
    for bigram, count in top_bigrams[:25]:
        words = bigram.split()
        if len(words) == 2:
            G.add_edge(words[0], words[1], weight=count)
            
    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    weights = [G[u][v]['weight'] / max([d['weight'] for u, v, d in G.edges(data=True)]) * 5 for u, v in G.edges()]
    
    nx.draw_networkx_nodes(G, pos, node_size=2200, node_color='#1f77b4', alpha=0.85)
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='#888888', alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=11, font_color='white', font_weight='bold')
    
    plt.title('Co-occurrence Network Graph (Jaringan Asosiasi Kata)', fontsize=15, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('output_plots/co_occurrence_network.png', dpi=300)
    plt.close()
    
    print("Text exploration and all visualizations generated successfully in 'output_plots/'!")

if __name__ == "__main__":
    main()
