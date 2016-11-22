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

For create item send post POST on 127.0.0.1:5000/items/
```json
{
  "data": {
    "name": "First item",
    "cpv": "0412234",
    "properties": {
      "props": {
        "number_of_kitchen": 1,
        "total_area": 30,
        "number_of_rooms": 6,
        "number_of_doors": 2
      }
    }
  }
}
```

For edit item send PATCH on 127.0.0.1:5000/items/{id_item}/
```json
{
  "data": {
    "properties": {
      "props": {
        "number_of_kitchen": 10
      }
    }
  }
}
```

For create item with custom version you need send "version" in "properties"
```json
{
  "data": {
    "name": "First item",
    "cpv": "0412234",
    "properties": {
      "version": "2",
      "props": {
        "number_of_kitchen": 1,
        "total_area": 30,
        "number_of_rooms": 6,
        "number_of_doors": 2
      }
    }
  }
}
```