from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

# 預載情感分類模型（這裡先用通用分類器替代，之後可換成 BioBERT）
#classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")#換小一點的model

# 這些是我們預設的疾病分類（可以自己改）
disease_labels = [
    "Respiratory disorders",
    "Cardiovascular diseases",
    "Neurological disorders",
    "Gastrointestinal issues",
    "Endocrine disorders",
    "Musculoskeletal problems"
]

def classify_medical_note(note):
    result = classifier(note, disease_labels)
    top_label = result['labels'][0]
    score = result['scores'][0]
    return top_label, round(score * 100, 2)

# 範例用法
if __name__ == "__main__":
    example_note = "Patient reports shortness of breath and mild chest pain."
    label, confidence = classify_medical_note(example_note)
    print(f"Predicted: {label} ({confidence}%)")
