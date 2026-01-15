## Требования
- Установленный Docker Desktop

## Как запустить
1. Запустите Docker Desktop.
2. Откройте командную строку и по порядку запустите следующие команды.

**На MacOS / Linux**:
```bash
git clone https://github.com/Azidalus/Test-Task-People-Detection
cd Test-Task-People-Detection
docker build -t people-detection .
docker run --rm -v $(pwd)/assets:/app/assets -v $(pwd)/outputs:/app/outputs people-detection
```

**На Windows**:

```bash
git clone https://github.com/Azidalus/Test-Task-People-Detection
cd Test-Task-People-Detection
docker build -t people-detection .
docker run --rm ` -v ${PWD}\assets:/app/assets ` -v ${PWD}\outputs:/app/outputs ` people-detection
```

## Результат
Обработанное видео *crowds_tracked.mp4* будет в папке *Test-Task-People-Detection/outputs*.