from requests import get, post

address = 'http://127.0.0.1:5000/api/update_job'

print(' Было:', get('http://127.0.0.1:5000/api/jobs').json())
print()

# ['team_leader', 'job', 'work_size', 'collaborators']
news = [
    {     # Такой id не существует
        'id': 12315,
        'team_leader': 1,
        'job': 'Какая-то работа',
        'work_size': 20,
        'collaborators': '1, 2, 3, 4, 5'
     },
    {     # Пустой json
    },
    {     # Не хватает id
        'team_leader': 1,
        'job': 'Какая-то работа',
        'work_size': 20,
     },
    {     # Правильный
        'id': 4,
        'job': 'Не какая-то там работа',
        'work_size': 50,
     },
]

for json_news in news:
    try:
        print(post(address, json=json_news).json())
    except Exception as er:
        print('Ошибка:', er)

print()
print('Стало:', get('http://127.0.0.1:5000/api/jobs').json())

"""
 Было: {'jobs': [{'collaborators': '2, 3', 'end_date': '2021-03-28 15:02:28', 'id': 1, 'is_finished': True, 'job': 'deployment of residential modules 1 and 2', 'start_date': '2021-03-28 15:02:28', 'team_leader': 1, 'work_size': 15}, {'collaborators': '3, 4', 'end_date': '2021-03-28 19:21:56', 'id': 2, 'is_finished': True, 'job': 'Exploration of mineral resources', 'start_date': '2021-03-28 19:21:56', 'team_leader': 2, 'work_size': 15}, {'collaborators': '4', 'end_date': '2021-03-28 19:23:13', 'id': 3, 'is_finished': True, 'job': 'Development of a management system', 'start_date': '2021-03-28 19:23:13', 'team_leader': 4, 'work_size': 24}, {'collaborators': '1, 2, 3, 4, 5', 'end_date': '2021-03-31 21:02:16', 'id': 4, 'is_finished': False, 'job': 'Какая-то работа', 'start_date': '2021-03-30 21:02:16', 'team_leader': 1, 'work_size': 20}]}

{'error': 'Job not exists'}
{'error': 'Empty request'}
{'error': 'Bad request'}
{'success': 'OK'}

Стало: {'jobs': [{'collaborators': '2, 3', 'end_date': '2021-03-28 15:02:28', 'id': 1, 'is_finished': True, 'job': 'deployment of residential modules 1 and 2', 'start_date': '2021-03-28 15:02:28', 'team_leader': 1, 'work_size': 15}, {'collaborators': '3, 4', 'end_date': '2021-03-28 19:21:56', 'id': 2, 'is_finished': True, 'job': 'Exploration of mineral resources', 'start_date': '2021-03-28 19:21:56', 'team_leader': 2, 'work_size': 15}, {'collaborators': '4', 'end_date': '2021-03-28 19:23:13', 'id': 3, 'is_finished': True, 'job': 'Development of a management system', 'start_date': '2021-03-28 19:23:13', 'team_leader': 4, 'work_size': 24}, {'collaborators': '1, 2, 3, 4, 5', 'end_date': '2021-03-31 21:02:16', 'id': 4, 'is_finished': False, 'job': 'Не какая-то там работа', 'start_date': '2021-03-30 21:02:16', 'team_leader': 1, 'work_size': 50}]}

"""
