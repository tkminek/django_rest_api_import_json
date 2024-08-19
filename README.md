# django_rest_api_import_json
Resp api local server for loading json data into sqlite database and serving responses on several end points.



## Preparation
- SQL database is not on github. Please create your own local sqlite database.
- Navige to folder django_test and run commands: ```python manage.py makemigrations``` and ```python manage.py migrate``` or use migrations from folder migrations

## Runing server
- navige to django_test folder and run ```main.py``` or navige to djanto_test and run comand: ```python manage.py runserver```
  

## Calling resp api calls using postman
- go to directory django_test/postman
- import Resp_api_calls.postman_collection.json to your postman
- 4 variants of rest api call are prepared:
   - POST-full_data_OK (http://127.0.0.1:8000/import/) - will import json data, which are specified in Body
   - DELETE-all_tables_data (http://127.0.0.1:8000/delete/) - will clear whole database
   - GET-info_model(http://127.0.0.1:8000/detail/model_name/) - will return data for wanted model
   - GET-info_item (http://127.0.0.1:8000/detail/model_name/id/) - will return data for wanted model and id
