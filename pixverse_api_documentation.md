Документация API Pixverse

Описание  
Данный API предоставляет методы для генерации видео из текста или изображения с помощью Pixverse, а также для получения статуса готовности видео.

Методы

1. POST /text2video  
   Описание: Генерация видео по текстовому описанию.  
   Параметры:  
   - prompt (string, обязательный) — текстовый запрос для генерации видео  
   - app_bundle_id (string, обязательный) — уникальный идентификатор приложения  
   - apphud_user_id (string, обязательный) — уникальный идентификатор пользователя
   Ответ (JSON):  
   - video_id (integer) — идентификатор созданного видео  
   Пример ответа: {"video_id": 123}  
   Ограничения:  
   - Длина prompt — не более 2048 знаков
   - Частота запросов — не более 10 в минуту  
   Возможные ошибки:  
   - 400 — неверные параметры запроса  
   - 500 — внутренняя ошибка сервиса

2. POST /image2video  
   Описание: Генерация видео по изображению и текстовому описанию.  
   Параметры:  
   - file (file, обязательный) — изображение в формате "PNG", "WEBP", "JPEG", "JPG"
   - prompt (string, обязательный) — текстовый запрос для генерации видео  
   - app_bundle_id (string, обязательный) — уникальный идентификатор приложения  
   - apphud_user_id (string, обязательный) — уникальный идентификатор пользователя   
   Ответ (JSON):  
   - video_id (integer) — идентификатор созданного видео  
   Пример ответа: {"video_id": 123}  
   Ограничения:  
   - Максимальный размер файла — меньше 20 МБ, не более 4000*4000 пикселей
   Возможные ошибки:  
   - 400 — неверные параметры или формат файла  
   - 413 — файл слишком большой  
   - 500 — внутренняя ошибка сервиса

3. GET /get_status  
   Описание: Получение статуса генерации видео.  
   Параметры (query parameters):  
   - video_id (integer, обязательный) — идентификатор видео  
   - app_bundle_id (string, обязательный) — идентификатор приложения  
   - apphud_user_id (string, обязательный) — идентификатор пользователя  
   Ответ (JSON):  
   В случае успешного завершения генерации:  
   { "status": "Generation successful", "url": "..." }  
   Если видео еще генерируется:  
   { "status": "Generating" }  
   Возможные статусы:  
   - Generation successful — генерация завершена успешно  
   - Generating — в процессе генерации  
   - Deleted — видео удалено  
   - Contents moderation failed — проверка содержимого не пройдена  
   - Generation failed — ошибка при генерации  
   Возможные ошибки:  
   - 400 — неверные параметры запроса  
   - 404 — видео не найдено  
   - 500 — внутренняя ошибка сервиса

Общие ограничения и информация:  
- Все запросы требуют API-ключ, передаваемый в заголовке 'API-KEY'.   
- Частота запросов ограничена в зависимости от метода.  
- В случае превышения лимитов возвращается ошибка 429 Too Many Requests.
- Конкретно количество максимальных запросов за период времени не указано, но в зависимости от тарифа ограничено количество одновременных запросов
- API_KEY и DATABASE_URL хранится в .env файле

Основные ошибки:  
- 400 Bad Request — неверные или отсутствующие параметры запроса  
- 401 Unauthorized — отсутствует или неверный API-ключ  
- 404 Not Found — запрошенный ресурс не найден  
- 413 Payload Too Large — файл превышает максимальный размер  
- 429 Too Many Requests — превышена частота запросов  
- 500 Internal Server Error — внутренняя ошибка сервиса
