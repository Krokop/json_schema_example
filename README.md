## Base module for integration Schema

Install dependency
```bash
make build_env
```

Set couchdb_url in app/main.py
```python
COUCHDB_URL = 'http://admin:admin@127.0.0.1:9000/'
```

Start server
```bash
 make run
```


Example data

Створемо item з кодом 0412234 та версією 1
POST on 127.0.0.1:5000/items/
```json
{
  "data": {
    "name": "First item",
    "cpv": "0412234",
    "properties": {
      "version": "1",
      "props": {
        "number_of_kitchen": 1,
        "total_area": 30,
        "number_of_rooms": 6,
        "living_space": 2
      }
    }
  }
}
```


Переглянемо створений item
GET on 127.0.0.1:5000/items/{id_item}/
```json
{
  "_rev": "1-7dafbb12197edb81d5aa037fb49c0a2d",
  "doc_type": "Item",
  "_id": "{id_item}",
  "cpv": "0412234",
  "name": "First item",
  "properties": {
    "props": {
      "total_area": 30,
      "number_of_rooms": 6,
      "living_space": 2,
      "number_of_kitchen": 1
    },
    "save_cpv": "04122",
    "doc_type": "BaseSchema",
    "version": "001"
  }
}
```

Але версія 1 нам не підходить і ми хочемо оновитися до 2, для цоього зробимо PATCH з новою версією та даними.
```json
{
  "data": {
    "properties": {
      "version": 2,
      "props": {
        "number_of_doors": 5,
        "number_of_kitchen": 1,
        "total_area": 2,
        "number_of_rooms": 5
      }
    }
  }
}
```