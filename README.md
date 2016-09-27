## Base module for integration Schema

Install dependency
```bash
make build_env
```

Start server
```bash
 export FLASK_DEBUG=1
 export FLASK_APP=app/main.py
 flask run
```


Example data

For create item send post POST on 127.0.0.1:5000/items/
```json
{
  "data": {
    "name": "First item",
    "cpv": "MA07-9",
    "properties": {
      "version": "002",
      "props": {
        "model": 12,
        "type": "Хетчбек",
        "motor": {
          "properties": 123,
          "bore": 101
        }
      }
    }
  }
}
```

For edit item send PUT on 127.0.0.1:5000/items/{id_item}/
```json
{
  "data": {
    "properties": {
      "props": {
        "model": 1234
      }
    }
  }
}
```