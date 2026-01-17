# Описание проекта
В этом репозитории лежит программа для детекции людей на тестовом видео crowd.mp4, а также dockerfile для возможности запуска программы на любой машине (Windows, Linux, MacOS) с помощью Docker.

# Как запустить программу у себя

## Требования
- Установленный Docker Desktop

Ссылка для скачивания: [https://docs.docker.com/desktop/](https://docs.docker.com/desktop/)

## Шаги запуска
1. Запустите Docker Desktop.
2. Откройте командную строку на компьютере и по порядку запустите следующие команды.

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
Обработанное видео *crowd_annotated.mp4* будет в папке *Test-Task-People-Detection/outputs/*.