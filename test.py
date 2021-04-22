from requests import get, post, delete

url = "http://127.0.0.1:5000/api/v2/jobs"

print(get(url).json())
print()

# 'team_leader', 'job', 'work_size', 'collaborators', 'category', 'is_finished'
users = [{  # Категории не существует
    "job": "Работка",
    "team_leader": "Scott Ridley",
    "work_size": 30,
    "collaborators": "Chastain Jessica",
    "category": "not Standard",
    "is_finished": True,
}, {        # Лидера не существует
    "job": "Работка",
    "team_leader": "Ноунейм какой-то",
    "work_size": 30,
    "collaborators": "Chastain Jessica",
    "category": "Standard",
    "is_finished": True,
}, {        # Не хватает полей
    "job": "Работка",
    "team_leader": "Scott Ridley",
    "work_size": 30,
    "is_finished": True,
}, {        # Всё верно
    "job": "Работка",
    "team_leader": "Scott Ridley",
    "work_size": 30,
    "collaborators": "Chastain Jessica",
    "category": "Standard",
    "is_finished": True,
}]

for user in users:
    print(post(url, json=user).json())

print()
print(get(url).json())
print()

print(delete(url + '/1000').json())
print(delete(url + '/0').json())
print(delete(url + '/hahaha').json())
print(delete(url + '/5').json())

print()
print(get(url).json())
print()

print(get(url + '/0').json())
print(get(url + '/f').json())
print(get(url + '/').json())
print(get(url + '/4').json())

print()
print(get(url).json())


'''
{'jobs': [{'category': 1, 'collaborators': '2, 3', 'is_finished': True, 'job': 'Deployment of residential modules 1 and 2', 'team_leader': 1, 'work_size': 15}, {'category': 1, 'collaborators': '3, 4', 'is_finished': True, 'job': 'Exploration of mineral resources', 'team_leader': 2, 'work_size': 15}, {'category': 1, 'collaborators': '4', 'is_finished': False, 'job': 'Development of a management system', 'team_leader': 4, 'work_size': 24}, {'category': 1, 'collaborators': '1, 2, 4, 5', 'is_finished': True, 'job': 'Какая-то работа', 'team_leader': 5, 'work_size': 40}]}

{'message': 'Category "not Standard" is not found'}
{'message': 'User "Ноунейм какой-то" is not found'}
{'message': {'collaborators': 'Missing required parameter in the JSON body or the post body or the query string'}}
{'success': 'OK'}

{'jobs': [{'category': 1, 'collaborators': '2, 3', 'is_finished': True, 'job': 'Deployment of residential modules 1 and 2', 'team_leader': 1, 'work_size': 15}, {'category': 1, 'collaborators': '3, 4', 'is_finished': True, 'job': 'Exploration of mineral resources', 'team_leader': 2, 'work_size': 15}, {'category': 1, 'collaborators': '4', 'is_finished': False, 'job': 'Development of a management system', 'team_leader': 4, 'work_size': 24}, {'category': 1, 'collaborators': '1, 2, 4, 5', 'is_finished': True, 'job': 'Какая-то работа', 'team_leader': 5, 'work_size': 40}, {'category': 1, 'collaborators': '3', 'is_finished': True, 'job': 'Работка', 'team_leader': 1, 'work_size': 30}]}

{'message': 'Job #1000 is not found'}
{'message': 'Job #0 is not found'}
{'error': 'Not found'}
{'success': 'OK'}

{'jobs': [{'category': 1, 'collaborators': '2, 3', 'is_finished': True, 'job': 'Deployment of residential modules 1 and 2', 'team_leader': 1, 'work_size': 15}, {'category': 1, 'collaborators': '3, 4', 'is_finished': True, 'job': 'Exploration of mineral resources', 'team_leader': 2, 'work_size': 15}, {'category': 1, 'collaborators': '4', 'is_finished': False, 'job': 'Development of a management system', 'team_leader': 4, 'work_size': 24}, {'category': 1, 'collaborators': '1, 2, 4, 5', 'is_finished': True, 'job': 'Какая-то работа', 'team_leader': 5, 'work_size': 40}]}

{'message': 'Job #0 is not found'}
{'error': 'Not found'}
{'error': 'Not found'}
{'jobs': {'category': 1, 'collaborators': '1, 2, 4, 5', 'is_finished': True, 'job': 'Какая-то работа', 'team_leader': 5, 'work_size': 40}}

{'jobs': [{'category': 1, 'collaborators': '2, 3', 'is_finished': True, 'job': 'Deployment of residential modules 1 and 2', 'team_leader': 1, 'work_size': 15}, {'category': 1, 'collaborators': '3, 4', 'is_finished': True, 'job': 'Exploration of mineral resources', 'team_leader': 2, 'work_size': 15}, {'category': 1, 'collaborators': '4', 'is_finished': False, 'job': 'Development of a management system', 'team_leader': 4, 'work_size': 24}, {'category': 1, 'collaborators': '1, 2, 4, 5', 'is_finished': True, 'job': 'Какая-то работа', 'team_leader': 5, 'work_size': 40}]}

'''