from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
import torch
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# Ограничение количества потоков CPU
torch.set_num_threads(4)

def run_pipeline():

    # Получение абсолютного пути к текущему файлу
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Создание директории для сохранения результатов, если она не существует
    results_dir = os.path.join(script_dir, '../data/output')
    os.makedirs(results_dir, exist_ok=True)

    # Загрузка данных из CSV-файла
    input_data_path = os.path.join(script_dir, '../data/input/train.csv')
    df = pd.read_csv(input_data_path)

    # Проверка на пропущенные значения в столбце 'Text'
    print(df['Text'].isnull().sum())

    # Замена пропущенных значений на пустые строки
    df['Text'] = df['Text'].fillna('')

    # Извлечение текстов и меток
    content = df['Text'].values
    sentiments = df['Sentiment'].values

    # Преобразование меток в числовой формат
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(sentiments)

    # Разделение данных на обучающую и тестовую выборки
    train_content, test_content, train_labels, test_labels = train_test_split(content, encoded_labels, test_size=0.8, random_state=42)

    # Загрузка токенизатора
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    # Подготовка данных для модели
    def preprocess_data(texts, labels, tokenizer, max_len=64):
        encoded_inputs = tokenizer(texts.tolist(), return_tensors='pt', padding=True, truncation=True, max_length=max_len)
        dataset = TensorDataset(encoded_inputs['input_ids'],encoded_inputs['attention_mask'],torch.tensor(labels))
        return dataset

    train_data = preprocess_data(train_content, train_labels, tokenizer)
    test_data = preprocess_data(test_content, test_labels, tokenizer)

    # Сохранение обработанных данных
    train_data_path = os.path.join(results_dir, 'train_dataset.pt')
    test_data_path = os.path.join(results_dir, 'val_dataset.pt')
    torch.save(train_data, train_data_path)
    torch.save(test_data, test_data_path)
    print("preprocessing completed. data saved to data/output.")

if __name__ == '__main__':
    run_pipeline()