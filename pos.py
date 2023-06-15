# mylibrary.py
import sys
from transformers import BertTokenizer, BertForTokenClassification
import torch
import numpy as np

def split_sentence(sentence):
    words = []
    word = ''
    
    for c in sentence:
        if c.isalnum():
            word += c
        else:
            if word:
                words.append(word)
                word = ''
            if not c.isspace():
                words.append(c)
                
    if word:
        words.append(word)
        
    return words

tag2idx = {'X': 0, 'NUM': 1, 'PART': 2, 'SCONJ': 3, 'PUNCT': 4, 'PRON': 5, 'AUX': 6, 'DET': 7, 'ADJ': 8, 'SYM': 9, 'INTJ': 10, 'ADV': 11, 'CCONJ': 12, 'PROPN': 13, 'VERB': 14, 'NOUN': 15, 'ADP': 16}

# Đường dẫn và tên file đã lưu mô hình
saved_model_file = "model.bin"

# Tải lại mô hình từ file
model = BertForTokenClassification.from_pretrained(saved_model_file, num_labels=len(tag2idx))

# Tải lại trạng thái của tokenizer
tokenizer = BertTokenizer.from_pretrained(saved_model_file, do_lower_case=True)

def predict_sentence(sentence):
    model.eval()

    # Tiền xử lý câu đầu vào
    original_words = split_sentence(sentence)
    tokenized_sentence = tokenizer.tokenize(sentence)
    input_ids = torch.tensor([tokenizer.convert_tokens_to_ids(tokenized_sentence)])

    # Tạo tensor input masks để chỉ ra các vị trí thực sự chứa từ và padding
    attention_masks = [[int(i > 0) for i in input_ids[0]]]

    # Chuyển đổi dữ liệu thành tensors PyTorch
    attention_masks = torch.tensor(attention_masks)

    # Dự đoán nhãn cho câu
    with torch.no_grad():
        outputs = model(input_ids, token_type_ids=None, attention_mask=attention_masks)
        logits = outputs.logits

    # Chuyển đổi kết quả dự đoán thành nhãn
    predicted_labels = np.argmax(logits.detach().cpu().numpy(), axis=2)[0]
    predicted_labels = [idx2tag[idx] for idx in predicted_labels]

    combined = [f"{original_words[i]} ({predicted_labels[i]})" for i in range(len(tokenized_sentence))]
    combined_string = " ".join(combined)

    return combined_string

# Chuẩn bị các từ điển ngược
idx2tag = {i: tag for tag, i in tag2idx.items()}

# Dùng một câu tiếng Anh mới để dự đoán
sentence = sys.argv[1]
# sentence = "I love dogs."
result = predict_sentence(sentence)
print(result)