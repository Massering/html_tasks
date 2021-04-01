import requests

APIKEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def bbox_of_object(object_name) -> (str, str):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={APIKEY}&geocode={object_name}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()

        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # print(json.dumps(toponym, sort_keys=True, indent=4, ensure_ascii=False))

        toponym_bbox_dict: dict = toponym["boundedBy"]["Envelope"]
        # print(toponym_bbox_dict)

    else:
        raise RuntimeError(f"""Ошибка выполнения запроса: {geocoder_request}
    Http статус: {response.status_code} ({response.reason})""")

    toponym_bbox = tuple(','.join(s.split()) for s in tuple(toponym_bbox_dict.values()))
    return toponym_bbox


def save_picture_by_name(object_name: str, filename: str, map_type="sat,skl") -> None:
    map_request = f"https://static-maps.yandex.ru/1.x/"
    map_params = {
        "l": map_type,
        "bbox": "~".join(bbox_of_object(object_name)),
    }

    response = requests.get(map_request, params=map_params)

    if not response:
        raise RuntimeError(f"""Ошибка выполнения запроса: {response.url}
    Http статус: {response.status_code} ({response.reason})""")

    # Запишем полученное изображение в файл.
    with open(filename, "wb") as file:
        file.write(response.content)
