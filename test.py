from requests import get, post, delete

url = "http://127.0.0.1:5000/api/v2/users"

print(get(url).json())

print()

users = [{     # email уже существует
    "email": "massering@yandex.ru",
    "password": "123123",
    "password_again": "123123",
    "surname": "Imagine",
    "name": "Person",
    "age": 16,
    "position": "Super cleaner",
    "speciality": "DIRT",
    "address": "USSR"
}, {      # Пароли не совпадают
    "email": "lalalalalala@mars.org",
    "password": "123123",
    "password_again": "123123123",
    "surname": "Imagine",
    "name": "Person",
    "age": 16,
    "position": "Super cleaner",
    "speciality": "DIRT",
    "address": "USSR"
}, {      # Не хватает полей
    "email": "lalalalalala@mars.org",
    "password": "123123",
    "surname": "Imagine",
}, {      # Всё верно
    "email": "lalalalalala@mars.org",
    "password": "123123",
    "password_again": "123123",
    "surname": "Imagine",
    "name": "Person",
    "age": 16,
    "position": "Super cleaner",
    "speciality": "DIRT",
    "address": "USSR"
}]

for user in users:
    print(post(url, json=user).json())

print()
print(get(url).json())
print()

print(delete(url + '/1000').json())
print(delete(url + '/0').json())
print(delete(url + '/hahaha').json())
print(delete(url + '/6').json())

print()
print(get(url).json())
print()

print(get(url + '/0').json())
print(get(url + '/f').json())
print(get(url + '/').json())
print(get(url + '/5').json())

print()
print(get(url).json())


'''
{'users': [{'address': 'module_1', 'age': 21, 'email': 'scott_chief@mars.org', 'name': 'Ridley', 'position': 'captain', 'speciality': 'research engineer', 'surname': 'Scott'}, {'address': 'module_1', 'age': 33, 'email': 'marsianin@mars.org', 'name': 'Matt', 'position': 'astronaut', 'speciality': 'pilot', 'surname': 'Damon'}, {'address': 'module_1', 'age': 43, 'email': 'jessica@mars.org', 'name': 'Jessica', 'position': 'astronaut', 'speciality': 'captain', 'surname': 'Chastain'}, {'address': 'module_1', 'age': 45, 'email': 'pena_from_rot@mars.org', 'name': 'Michael', 'position': 'astronaut', 'speciality': 'astronaut', 'surname': 'Peña'}, {'address': 'Не дом, и не улица, мой адрес - Советский Союз!', 'age': 15, 'email': 'massering@yandex.ru', 'name': 'Максим', 'position': 'Ученик', 'speciality': 'Точные науки', 'surname': 'Рудаков'}]}

{'message': 'User with that email already exist'}
{'message': 'Passwords are not the same'}
{'message': {'password_again': 'Missing required parameter in the JSON body or the post body or the query string'}}
{'success': 'OK'}

{'users': [{'address': 'module_1', 'age': 21, 'email': 'scott_chief@mars.org', 'name': 'Ridley', 'position': 'captain', 'speciality': 'research engineer', 'surname': 'Scott'}, {'address': 'module_1', 'age': 33, 'email': 'marsianin@mars.org', 'name': 'Matt', 'position': 'astronaut', 'speciality': 'pilot', 'surname': 'Damon'}, {'address': 'module_1', 'age': 43, 'email': 'jessica@mars.org', 'name': 'Jessica', 'position': 'astronaut', 'speciality': 'captain', 'surname': 'Chastain'}, {'address': 'module_1', 'age': 45, 'email': 'pena_from_rot@mars.org', 'name': 'Michael', 'position': 'astronaut', 'speciality': 'astronaut', 'surname': 'Peña'}, {'address': 'Не дом, и не улица, мой адрес - Советский Союз!', 'age': 15, 'email': 'massering@yandex.ru', 'name': 'Максим', 'position': 'Ученик', 'speciality': 'Точные науки', 'surname': 'Рудаков'}, {'address': 'USSR', 'age': 16, 'email': 'lalalalalala@mars.org', 'name': 'Person', 'position': 'Super cleaner', 'speciality': 'DIRT', 'surname': 'Imagine'}]}

{'message': 'User #1000 not found'}
{'message': 'User #0 not found'}
{'error': 'Not found'}
{'success': 'OK'}

{'users': [{'address': 'module_1', 'age': 21, 'email': 'scott_chief@mars.org', 'name': 'Ridley', 'position': 'captain', 'speciality': 'research engineer', 'surname': 'Scott'}, {'address': 'module_1', 'age': 33, 'email': 'marsianin@mars.org', 'name': 'Matt', 'position': 'astronaut', 'speciality': 'pilot', 'surname': 'Damon'}, {'address': 'module_1', 'age': 43, 'email': 'jessica@mars.org', 'name': 'Jessica', 'position': 'astronaut', 'speciality': 'captain', 'surname': 'Chastain'}, {'address': 'module_1', 'age': 45, 'email': 'pena_from_rot@mars.org', 'name': 'Michael', 'position': 'astronaut', 'speciality': 'astronaut', 'surname': 'Peña'}, {'address': 'Не дом, и не улица, мой адрес - Советский Союз!', 'age': 15, 'email': 'massering@yandex.ru', 'name': 'Максим', 'position': 'Ученик', 'speciality': 'Точные науки', 'surname': 'Рудаков'}]}

{'message': 'User #0 not found'}
{'error': 'Not found'}
{'error': 'Not found'}
{'users': {'address': 'Не дом, и не улица, мой адрес - Советский Союз!', 'age': 15, 'email': 'massering@yandex.ru', 'name': 'Максим', 'position': 'Ученик', 'speciality': 'Точные науки', 'surname': 'Рудаков'}}

{'users': [{'address': 'module_1', 'age': 21, 'email': 'scott_chief@mars.org', 'name': 'Ridley', 'position': 'captain', 'speciality': 'research engineer', 'surname': 'Scott'}, {'address': 'module_1', 'age': 33, 'email': 'marsianin@mars.org', 'name': 'Matt', 'position': 'astronaut', 'speciality': 'pilot', 'surname': 'Damon'}, {'address': 'module_1', 'age': 43, 'email': 'jessica@mars.org', 'name': 'Jessica', 'position': 'astronaut', 'speciality': 'captain', 'surname': 'Chastain'}, {'address': 'module_1', 'age': 45, 'email': 'pena_from_rot@mars.org', 'name': 'Michael', 'position': 'astronaut', 'speciality': 'astronaut', 'surname': 'Peña'}, {'address': 'Не дом, и не улица, мой адрес - Советский Союз!', 'age': 15, 'email': 'massering@yandex.ru', 'name': 'Максим', 'position': 'Ученик', 'speciality': 'Точные науки', 'surname': 'Рудаков'}]}
'''