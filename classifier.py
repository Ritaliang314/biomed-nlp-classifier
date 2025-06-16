# classifier.py
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "OzzeY72/biobert-medical-specialities"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

def classify_medical_note(note):
    inputs = tokenizer(note, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    predicted_label = model.config.id2label[predicted_class_id]
    confidence = torch.softmax(logits, dim=1)[0][predicted_class_id].item()
    return predicted_label, round(confidence * 100, 2)



# 範例用法
if __name__ == "__main__":
    example_note = "Patient reports shortness of breath and mild chest pain."
    label, confidence = classify_medical_note(example_note)
    print(f"Predicted: {label} ({confidence}%)")
