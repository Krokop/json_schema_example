## Base module for integration Schema

Install dependency
```bash
make build_env
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

For create item with custom version you need send "version" in "properties"
```json
{
  "data": {
    "name": "First item",
    "cpv": "MA07-9",
    "properties": {
      "version": "001",
      "props": {
        "model": "Model as a string",
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