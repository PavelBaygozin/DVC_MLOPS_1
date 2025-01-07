# Управление данными с помощью DVC

Цель: настраиваем DVC для управления данными и создания ML-пайплайнов, интегрируем удаленное хранилище и автоматизируем процесс через CI/CD.

## Инициализация DVC

1. Инициализируем DVC:
   ```bash
   dvc init
   ```
2. Добавляем данные:
   ```bash
   dvc add data/input/train.csv
   ```
3. Фиксируем изменения в Git:
   ```bash
   git add data/input/train.csv.dvc .gitignore
   git commit -m ""
   ```

## Настройка удаленного хранилища (Yandex Object Storage)

1. Создаем бакет с именем `mlops-bpa-1`.
2. Устанавливаем и настраиваем DVC для работы с Yandex Object Storage.
3. Получаем `Access Key ID` и `Secret Access Key`.

### Синхронизация с хранилищем

1. Добавляем удаленное хранилище:
   ```bash
   dvc remote add -d myremote s3:/........
   ```
2. Настраиваем параметры доступа:
   ```bash
   dvc remote modify myremote endpointurl https://storage.yandexcloud.net
   dvc remote modify myremote access_key_id <your-access-key-id>
   dvc remote modify myremote secret_access_key <your-secret-access-key>
   ```
3. Проверяем конфигурацию:
   ```bash
   dvc remote list
   dvc remote modify myremote --list
   ```
4. Загружаем данные:
   ```bash
   dvc push
   ```
5. Получаем данные:
   ```bash
   dvc pull
   ```

## Создание и запуск пайплайна

1. Создаем папку `src` и файл `appy.py` для обработки данных.
2. Создаем файл `dvc.yaml` для описания пайплайна.
3. Запускаем пайплайн:
   ```bash
   dvc repro
   ```
   DVC автоматически обновляет только необходимые этапы. В папке `data/input` появляются файлы `train_dataset.pt` и `val_dataset.pt`.

4. Загружаем данные в удаленное хранилище:
   ```bash
   dvc push
   ```

## Интеграция с CI/CD (GitHub Actions)

1. Создаем файл `.github/workflows/dvc-pipeline.yml`.
2. Настраиваем секреты в GitHub:
   - `DVC_REMOTE_ACCESS_KEY_ID`: Access Key ID.
   - `DVC_REMOTE_SECRET_ACCESS_KEY`: Secret Access Key.
3. Добавляем логирование в CI/CD.

## Итоговый процесс

1. Обновляем данные (например, изменяем `train.csv`).
2. Проверяем статус:
   ```bash
   dvc status
   ```
3. Пересоздаем данные:
   ```bash
   dvc repro
   ```
4. Фиксируем изменения в Git:
   ```bash
   git commit
   ```
5. Загружаем данные в хранилище:
   ```bash
   dvc push
   ```
6. Отправляем код на GitHub:
   ```bash
   git push
   ```
   Это запускает CI/CD пайплайн.

# Итоги

В этой части мы настроили DVC для управления данными, интегрировали удаленное хранилище и автоматизировали процесс через CI/CD. Основные шаги включали добавление данных, настройку хранилища, создание пайплайна и автоматизацию через GitHub Actions.
```