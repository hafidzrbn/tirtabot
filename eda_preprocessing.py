import re
import pandas as pd

# Indonesian Slang & Informal Words Dictionary
SLANG_DICT = {
    "gak": "tidak", "ga": "tidak", "gk": "tidak", "g": "tidak", "tdk": "tidak", "enggak": "tidak", "kaga": "tidak", "kagak": "tidak",
    "bgt": "banget", "bngt": "banget", "bgttt": "banget", "dgn": "dengan", "dg": "dengan",
    "sdh": "sudah", "udah": "sudah", "dh": "sudah", "dah": "sudah", "bs": "bisa", "bisaa": "bisa",
    "krn": "karena", "karna": "karena", "tp": "tapi", "tpi": "tapi", "tetep": "tetap",
    "klo": "kalau", "kalo": "kalau", "klw": "kalau", "kl": "kalau", "dri": "dari", "sm": "sama", "sma": "sama",
    "utk": "untuk", "bkn": "bukan", "blm": "belum", "belom": "belum",
    "dr": "dokter", "dr.": "dokter", "dok": "dokter", "jir": "astaga", "anjir": "astaga", "njir": "astaga",
    "lg": "lagi", "jg": "juga", "dapet": "dapat", "pengen": "ingin", "bang": "abang", "bg": "abang",
    "bro": "kawan", "cuy": "kawan", "guys": "kawan", "gaes": "kawan", "aja": "saja", "aj": "saja",
    "sy": "saya", "gw": "saya", "gua": "saya", "lu": "kamu", "elo": "kamu", "kuy": "ayo",
    "mantap": "bagus", "mantul": "bagus", "makasih": "terima kasih", "trims": "terima kasih",
    "smg": "semoga", "bener": "benar", "org": "orang", "gimana": "bagaimana", "knp": "mengapa",
    "pake": "pakai", "spt": "sepatu", "running": "lari"
}

NEGATION_WORDS = {"tidak", "bukan", "belum", "kurang", "tanpa", "jangan"}

INDONESIAN_STOPWORDS = {
    "yang", "di", "ke", "dari", "ini", "itu", "dan", "atau", "adalah", "yaitu",
    "ialah", "pada", "untuk", "dengan", "oleh", "secara", "sebagai", "bahwa",
    "akan", "telah", "sudah", "sedang", "bisa", "dapat", "ada", "banyak", "jika",
    "maka", "bahkan", "serta", "saja", "juga", "hanya", "sangat", "amat", "nih",
    "si", "sang", "nah", "dong", "deh", "kok", "kan", "pun", "ya", "yah", "oh",
    "ah", "wah", "wkwk", "wkwkwk", "haha", "hehe"
}

def clean_raw_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>|&[^;\s]+;', ' ', text)
    text = re.sub(r'http\S+|www\.\S+|[@#]\S+', ' ', text)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def normalize_slang(tokens):
    return [SLANG_DICT.get(t, t) for t in tokens]

# Essential Step: Join negation word with following word (e.g. tidak_bagus)
def handle_negation(tokens):
    result = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if t in NEGATION_WORDS and i + 1 < n:
            next_t = tokens[i + 1]
            if next_t not in INDONESIAN_STOPWORDS:
                result.append(f"{t}_{next_t}")
                i += 2
                continue
        result.append(t)
        i += 1
    return result

def remove_stopwords(tokens):
    return [t for t in tokens if t not in INDONESIAN_STOPWORDS or "_" in t]

def preprocess_pipeline(text):
    cleaned = clean_raw_text(text)
    tokens = cleaned.split()
    tokens = normalize_slang(tokens)
    tokens = handle_negation(tokens)
    tokens_final = remove_stopwords(tokens)
    return cleaned, " ".join(tokens_final), tokens_final

if __name__ == "__main__":
    df = pd.read_csv("youtube_comments_dr_tirta.csv")
    df['text'] = df['text'].fillna('')
    df = df[df['text'].str.strip() != ''].copy()
    
    cleaned_texts, processed_texts, token_counts = [], [], []
    for text in df['text']:
        cleaned, proc_text, tokens = preprocess_pipeline(text)
        cleaned_texts.append(cleaned)
        processed_texts.append(proc_text)
        token_counts.append(len(tokens))
        
    df['cleaned_text'] = cleaned_texts
    df['processed_text'] = processed_texts
    df['token_count'] = token_counts
    
    df_clean = df[df['processed_text'].str.strip() != ''].copy()
    df_clean.to_csv("processed_comments.csv", index=False, encoding="utf-8-sig")
    print(f"Preprocessing complete. Total valid rows: {len(df_clean):,}")

