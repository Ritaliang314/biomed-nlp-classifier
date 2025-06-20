from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline

# 載入模型
model_name = "Bohanlu/Taigi-Llama-2-Translator-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 建立翻譯管線
translator = TextGenerationPipeline(model=model, tokenizer=tokenizer, max_new_tokens=100)

def chinese_to_tailo(text):
    result = translator(f"<ch2tl> {text}")
    return result[0]["generated_text"].replace(f"<ch2tl> {text}", "").strip()

# 使用範例
tailo = chinese_to_tailo("心臟科")
print("台羅拼音：", tailo)