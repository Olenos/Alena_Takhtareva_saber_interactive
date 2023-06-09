Тестовое задание
===

Привет! Это мое решение тестового задания

# SQL

## SQL 1

Напишите запрос, который выведет, сколько времени в среднем задачи каждой группы находятся в статусе “Open” 

Условия:

1. Под группой подразумевается первый символ в ключе задачи (например, для ключа “C-40460” группой будет “C”)

2. Задача может переходить в один и тот же статус несколько раз

3. Переведите время в часы с округлением до двух знаков после запятой

### Решение

```
SELECT SUBSTR(issue_key, 1, 1) AS group_key,
       ROUND(AVG(minutes_in_status) / 60, 2) AS avg_time_in_open
FROM history
WHERE status = 'Open'
GROUP BY group_key;
```

## SQL 2

Напишите запрос, который выведет ключ задачи, последний статус и его время создания для задач, 
которые открыты на данный момент времени

Условия:

1. Открытыми считаются задачи, у которых последний статус в момент времени не “Closed” и не “Resolved”

2. Задача может переходить в один и тот же статус несколько раз

3. Оформите запрос таким образом, чтобы, изменив дату, его можно было использовать для поиска 
открытых задач в любой момент времени в прошлом

4. Переведите время в текстовое представление

### Решение

Для начала я сделала запрос по принципу "сделай, чтобы работало, а потом оптимизируй":

```
SELECT issue_key,
       status,
       CAST(DATETIME(started_at / 1000, 'unixepoch') AS TEXT) AS started_at
FROM history h
WHERE status NOT IN ('Closed',
                     'Resolved')
  AND started_at <= DATETIME('now')
  AND started_at =
    (SELECT MAX(started_at)
     FROM history AS h2
     WHERE h.issue_key = h2.issue_key )
ORDER BY started_at DESC
```

Данный запрос не очень эффективен (как минимум по времени выполнения), 
поэтому я сделала второй вариант с использованием оконок:

```
SELECT issue_key,
       status,
       CAST(DATETIME(started_at / 1000, 'unixepoch') AS TEXT) AS started_at
FROM
  (SELECT *,
          ROW_NUMBER() OVER (PARTITION BY issue_key
                             ORDER BY DATETIME(started_at / 1000, 'unixepoch') DESC) AS ROWNUM
   FROM history h) AS x
WHERE ROWNUM = 1
  AND status NOT IN ('Closed',
                     'Resolved')
  AND started_at <= DATETIME('now')
ORDER BY started_at DESC
```

На всякий случай скажу, что написанные мною запросы - не предел моих знаний, если вы хотели увидеть какие-то
определенные структуры и конструкции, то я об этом не знала, в требованиях не указано

Так что вы можете у меня прямо спросить, что я умею, а что нет, а я вам честно отвечу)

# Python

## Слияние логов

Требуется написать скрипт, который объединит два файла с логами в один

При этом сообщения в получившемся файле тоже должны быть упорядочены в порядке возрастания по полю `timestamp`

К заданию прилагается вспомогательный скрипт на python3, который создает два файла `log_a.jsonl` и `log_b.jsonl`

Командлайн для запуска:

```
log_generator.py <path/to/dir>
```

Ваше приложение должно поддерживать следующий командлайн:

```
<your_script>.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>
```

### Решение

Я сделала структуру и оформление, подобную вашему вспомогательному скрипту 
(предположила, что это должны быть файлы одного проекта)

Также я использовала для выполнения только встроенные библиотеки, хотя, 
конечно, тут очень к месту были бы `pydantic` или `pandas`, но нужно было бы
прописывать их в локальное окружение, а моя цель не усложнять жизнь пользователю)

Я не имею в виду, что это сложно или я не смогла бы, но вы использовали только 
встроенные функции и я решила поступить также (ну и не забывала про "сделай, чтобы работало,
а потом оптимизируй")

К слову об оптимизации, для двух файлов по 1GB сортировка и вывод в скрипте выполняется 
ооочень долго (сжирается вся ОП, у меня даже процесс explorer дропнулся), как это можно было бы решить:

1. Как я и сказала выше, можно воспользоваться другими библиотеками (как правило, если
обработка выполняется очень долго, то `pandas` это сделает за пару секунд)

2. Можно распараллеливать процессы и попробовать сделать обработку в несколько потоков (ни разу 
этого не делала, но знаю, что можно, и при желании научусь)

3. Если подумать именно о разгрузке ОП, то можно подключить библиотеку sqlite3 (она кстати встроенная), 
создать табличку, записать файлы туда, там же их отсортировать и сделать выгрузку (плюсы - освободим ОП, 
минусы - начнем заполнять диск)

В общем, решений достаточно много, и как мне кажется, этап оптимизации уже должен быть непосредственно 
в среде запуска (кто знает, может ОП будет достаточно, а дисковое пространство наоборот захлебывается)

Я сделала наверняка не самое эффективное решение, но рабочее и удовлетворяющее условиям задачи

Командлайн для запуска:

```
log_merged.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>
```

Спасибо за прочтение моего решения! Очень надеюсь получить обратную связь)