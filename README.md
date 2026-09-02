**post-запрос** - содержит:
- **URL**(Адрес страницы, куда отправляется запрос)
- **data** - Словарь или байты для отправки данных
- **json** - Словарь
- **headers** - доп. данные(токен, тип контента и тд)
- **params** - параметры строки запросы, дополнит Url

```query_parameters = {
    "api_key": "secret_123",
    "version": "v2"
}

response = requests.post(
    "https://example.com", 
    params=query_parameters
)

print("Итоговый URL:", response.url)

# Вывод: https://example.com?api_key=secret_123&version=v2

```

