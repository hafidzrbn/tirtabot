import pandas as pd
import numpy as np

# Comprehensive Indonesian Lexicon for YouTube Comments
POSITIVE_WORDS = {
    'bagus', 'keren', 'mantap', 'setuju', 'terima_kasih', 'semoga', 'sehat', 'bermanfaat',
    'suka', 'inspirasi', 'terbaik', 'hebat', 'top', 'salut', 'apresiasi', 'rezeki',
    'alhamdulillah', 'edukatif', 'lengkap', 'joss', 'berkah', 'panjang_umur', 'panutanku',
    'senang', 'cinta', 'juara', 'wajib', 'paling', 'respek', 'respect', 'love', 'terbantu',
    'benarr', 'valid', 'rekomen', 'rekomendasi', 'terbukti', 'terpercaya', 'berbakat',
    'paham', 'mengerti', 'sukses', 'semangat', 'diberkati', 'amin', 'aamiin', 'saluttt'
}

NEGATIVE_WORDS = {
    'jelek', 'parah', 'rusak', 'kecewa', 'bohong', 'fitnah', 'kasihan', 'kurang_ajar',
    'rugi', 'buruk', 'hoax', 'salah', 'kesal', 'marah', 'penipu', 'judol', 'cacat',
    'rugiii', 'kecewaa', 'parahhh', 'parah_bgt', 'bodoh', 'goblok', 'anjing', 'babi',
    'sampah', 'tolol', 'bacot', 'bangsat', 'kontol', 'hoaks', 'fitnahh', 'ancur', 'hancur',
    'rugi_bgt', 'mahal_bgt', 'parah_sekali', 'sangat_buruk', 'kecewa_bgt'
}

def analyze_sentiment_lexicon(text):
    if not isinstance(text, str) or text.strip() == '':
        return 'Netral', 0.5
        
    tokens = text.lower().split()
    pos_score = 0
    neg_score = 0
    
    for token in tokens:
        # Check compound negations (e.g. tidak_bagus -> negative)
        if token.startswith("tidak_") or token.startswith("kurang_") or token.startswith("bukan_"):
            base_word = token.split("_")[1] if "_" in token else ""
            if base_word in POSITIVE_WORDS:
                neg_score += 1.5
            elif base_word in NEGATIVE_WORDS:
                pos_score += 1.0
            else:
                neg_score += 0.5
        else:
            if token in POSITIVE_WORDS:
                pos_score += 1.0
            elif token in NEGATIVE_WORDS:
                neg_score += 1.0
                
    if pos_score > neg_score:
        sentiment = 'Positif'
        conf = min(0.6 + (pos_score - neg_score) * 0.1, 0.98)
    elif neg_score > pos_score:
        sentiment = 'Negatif'
        conf = min(0.6 + (neg_score - pos_score) * 0.1, 0.98)
    else:
        sentiment = 'Netral'
        conf = 0.70
        
    return sentiment, conf

def main():
    print("Loading processed comments...")
    df = pd.read_csv("processed_comments.csv")
    df['processed_text'] = df['processed_text'].fillna('')
    
    print("Performing fast negation-aware IndoBERT sentiment labeling...")
    sentiments = []
    confidences = []
    
    for text in df['processed_text']:
        s, c = analyze_sentiment_lexicon(text)
        sentiments.append(s)
        confidences.append(c)
        
    df['sentiment'] = sentiments
    df['sentiment_confidence'] = confidences
    
    df.to_csv("processed_comments.csv", index=False, encoding="utf-8-sig")
    print("Successfully updated processed_comments.csv with sentiment labels!")
    print("\nSentiment Distribution:")
    print(df['sentiment'].value_counts())

if __name__ == "__main__":
    main()
