import re
import pandas as pd
import numpy as np

# Dictionary Slang / Kata Tidak Baku Bahasa Indonesia & Youtube Comment Jargon
SLANG_DICT = {
    "gak": "tidak", "ga": "tidak", "gk": "tidak", "g": "tidak", "tdk": "tidak", "enggak": "tidak", "kaga": "tidak", "kagak": "tidak",
    "bgt": "banget", "bngt": "banget", "bgttt": "banget",
    "dgn": "dengan", "dg": "dengan",
    "sdh": "sudah", "udah": "sudah", "dh": "sudah", "dah": "sudah",
    "bs": "bisa", "bisaa": "bisa",
    "krn": "karena", "karna": "karena", "krena": "karena",
    "tp": "tapi", "tpi": "tapi", "tetep": "tetap",
    "klo": "kalau", "kalo": "kalau", "klw": "kalau", "kl": "kalau",
    "dri": "dari", "driku": "dari saya",
    "sm": "sama", "sma": "sama",
    "utk": "untuk", "untk": "untuk",
    "bkn": "bukan",
    "blm": "belum", "belom": "belum",
    "dr": "dokter", "dr.": "dokter", "dok": "dokter", "dokternya": "dokter",
    "jir": "astaga", "anjir": "astaga", "anjrit": "astaga", "njir": "astaga", "anjay": "astaga",
    "lg": "lagi", "lgi": "lagi",
    "jg": "juga", "jga": "juga",
    "dapet": "dapat", "dpet": "dapat",
    "pengen": "ingin", "penn": "ingin", "pingin": "ingin",
    "bang": "abang", "bng": "abang", "bg": "abang",
    "bro": "kawan", "cuy": "kawan", "guys": "kawan", "gaes": "kawan", "gays": "kawan",
    "aja": "saja", "aj": "saja",
    "sy": "saya", "akuu": "saya", "gwa": "saya", "gua": "saya", "gw": "saya", "gue": "saya",
    "lu": "kamu", "elo": "kamu", "elu": "kamu", "lo": "kamu",
    "kuy": "ayo",
    "mantap": "bagus", "mantul": "bagus", "mantab": "bagus",
    "makasih": "terima kasih", "trims": "terima kasih", "thx": "terima kasih", "thanks": "terima kasih",
    "smg": "semoga", "moga": "semoga",
    "bknnya": "bukannya", "seharusnya": "harusnya",
    "bener": "benar", "beneran": "beneran",
    "org": "orang", "orng": "orang",
    "gimana": "bagaimana", "gmn": "bagaimana",
    "kenapa": "mengapa", "knp": "mengapa",
    "pake": "pakai", "pakek": "pakai",
    "dapet": "dapat",
    "banyak": "banyak",
    "podcast": "podcast",
    "sepatu": "sepatu", "spt": "sepatu",
    "running": "lari", "larii": "lari"
}

# Negation words to be paired with subsequent word
NEGATION_WORDS = {"tidak", "bukan", "belum", "kurang", "tanpa", "jangan"}

# Curated Indonesian stopword list (excluding negation words to preserve context)
INDONESIAN_STOPWORDS = {
    "yang", "di", "ke", "dari", "ini", "itu", "dan", "atau", "adalah", "yaitu",
    "ialah", "pada", "untuk", "dengan", "oleh", "secara", "sebagai", "bahwa",
    "akan", "telah", "sudah", "sedang", "bisa", "dapat", "ada", "banyak", "jika",
    "maka", "bahkan", "serta", "saja", "juga", "hanya", "sangat", "amat", "nih",
    "si", "sang", "nah", "dong", "deh", "kok", "kan", "pun", "ya", "yah", "oh",
    "ah", "wah", "wkwk", "wkwkwk", "haaha", "haha", "hehe"
}

def clean_raw_text(text):
    if not isinstance(text, str):
        return ""
    # Convert lower
    text = text.lower()
    # Remove HTML tags / entities
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[^;\s]+;', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    # Remove mentions & hashtags
    text = re.sub(r'[@#]\S+', ' ', text)
    # Normalize repeated characters (e.g. baaaagus -> bagus, mantapnnn -> mantap)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    # Remove non-alphabetical characters except space
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_slang(tokens):
    normalized = []
    for token in tokens:
        word = SLANG_DICT.get(token, token)
        normalized.append(word)
    return normalized

def handle_negation(tokens):
    result = []
    i = 0
    n = len(tokens)
    while i < n:
        token = tokens[i]
        if token in NEGATION_WORDS and i + 1 < n:
            next_token = tokens[i + 1]
            if next_token not in INDONESIAN_STOPWORDS:
                result.append(f"{token}_{next_token}")
                i += 2
                continue
        result.append(token)
        i += 1
    return result

def remove_stopwords(tokens):
    return [t for t in tokens if t not in INDONESIAN_STOPWORDS or "_" in t]

def preprocess_pipeline(text):
    cleaned = clean_raw_text(text)
    tokens = cleaned.split()
    tokens_slang = normalize_slang(tokens)
    tokens_negated = handle_negation(tokens_slang)
    tokens_final = remove_stopwords(tokens_negated)
    processed_text = " ".join(tokens_final)
    return cleaned, processed_text, tokens_final

def main():
    print("Loading raw YouTube comments dataset...")
    df = pd.read_csv("youtube_comments_dr_tirta.csv")
    print(f"Total raw rows: {len(df)}")
    
    # Drop empty or NaN comments
    df['text'] = df['text'].fillna('')
    df = df[df['text'].str.strip() != ''].copy()
    print(f"Total valid non-empty rows: {len(df)}")
    
    print("Running preprocessing pipeline (Cleaning, Slang Normalization, Negation Handling, Stopwords)...")
    cleaned_texts = []
    processed_texts = []
    token_counts = []
    
    for text in df['text']:
        cleaned, proc_text, tokens = preprocess_pipeline(text)
        cleaned_texts.append(cleaned)
        processed_texts.append(proc_text)
        token_counts.append(len(tokens))
        
    df['cleaned_text'] = cleaned_texts
    df['processed_text'] = processed_texts
    df['token_count'] = token_counts
    
    # Filter out empty processed text (e.g. comments with only emojis or punctuation)
    df_clean = df[df['processed_text'].str.strip() != ''].copy()
    print(f"Total preprocessed valid rows: {len(df_clean)}")
    
    # Save to processed_comments.csv
    output_path = "processed_comments.csv"
    df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Successfully saved preprocessed dataset to '{output_path}'!")
    
    # Generate Sample Before vs After Table
    sample_df = df_clean[['text', 'processed_text']].sample(n=10, random_state=42)
    sample_df.columns = ['Teks Asli (Sebelum Preprocessing)', 'Teks Bersih (Sesudah Preprocessing & Normalisasi Slang/Negasi)']
    
    sample_df.to_csv("preprocessing_sample_table.csv", index=False, encoding="utf-8-sig")
    print("\n--- SAMPLE PREPROCESSING BEFORE VS AFTER ---")
    for idx, row in enumerate(sample_df.itertuples(), 1):
        raw = str(row[1]).encode('ascii', 'ignore').decode('ascii')
        proc = str(row[2]).encode('ascii', 'ignore').decode('ascii')
        print(f"\n[{idx}] SEBELUM : {raw}")
        print(f"    SESUDAH : {proc}")

if __name__ == "__main__":
    main()
