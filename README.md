# Sheremetyevo Weather Parser 🌤️


# Обычный способ
### Клонирование Репозитория

```git clone https://github.com/Valdislavprog88/sheremetyevo_weather_parser.git```


```cd sheremetyevo_weather_parser```


## Настройка Виртуального Окружения
### Создание виртуального окружения
```python -m venv venv```

### Активация виртуального окружения
```source venv/bin/activate```

## Установка Зависимостей

### Установите зависимости из requirements.txt
```pip install -r requirements.txt```

### Запуск Сервера Uvicorn
```uvicorn main:app --host 0.0.0.0 --port 8000 # порт и хост поменяй на свои```

# Способ через Docker
### Установка
Docker должен быть уже установлен! Ссылка на установку: https://docs.docker.com/engine/install/

## Скачивание и запуск
### Скачайте образ с dockerhub:
```sudo docker pull dockerhub.timeweb.cloud/evmexaprog88 weather_parser```

### Создайте docker-volume для хранения данных из контейнера
```sudo docker volume create --name weather_volume```

### Запустите проект
Вместо 8080 поставьте тот, порт, на котором будет работать сервис!


```sudo docker run -p 8000:8080 -d --mount source=weather_volume,target=/app dockerhub.timeweb.cloud/evmexaprog88/weather_parser```

