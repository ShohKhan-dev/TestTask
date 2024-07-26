## Simple Django REST API implementation with elasticsearch and jwt authentication



How to run:
```
>>> docker-compose up --build -d
```
to check:
```
>>> docker ps
(env) PS C:\Shohjahon\Work\task\DRF\src> docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS          PORTS                              NAMES
74e70e23097a   src_web                "bash -c 'python3 ma…"   4 minutes ago   Up 4 minutes    0.0.0.0:8000->8000/tcp             src_web_1
1e98090d630b   elasticsearch:8.14.0   "/bin/tini -- /usr/l…"   6 hours ago     Up 28 minutes   0.0.0.0:9200->9200/tcp, 9300/tcp   src_es_1
74d202fa5bdd   postgres:16            "docker-entrypoint.s…"   6 hours ago     Up 28 minutes   0.0.0.0:5432->5432/tcp             src_db_1
```



All APIs:


For Registration, Post Request to: http://localhost:8000/api/register/
with params:
```JSON
{
    "username": "username",
    "password": "password",
    "email": "test@gmail.com",
    "first_name": "test",
    "last_name": "tester"
}
```


To Login or To Get new Token: Post request http://localhost:8000/api/token/
with params:
```JSON
{
    "username": "username",
    "password": "password"
}
```

Response:
```JSON
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjA4NDg5MywiaWF0IjoxNzIxOTk4NDkzLCJqdGkiOiIyZjU4YmM5MGI3YmY0MTc0OGE2ODEyYzQ1MGNjZTk3OSIsInVzZXJfaWQiOjN9.oMtiy2UhfT9jvOuECKfGnQuiHlAEshz1dq2jrQQilSw",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxOTk4NzkzLCJpYXQiOjE3MjE5OTg0OTMsImp0aSI6IjQzNGViNzhjMGI1ZjRjOWRhMWFkYjAwYjc3NTk4NjIzIiwidXNlcl9pZCI6M30.7l9tY96E4lmHJYaCEfO8eq3MI_OxHnAjXkrYe9lS7tg"
}
```

## NOTE: for each of following request you will need to send access token as Bearer Token

POST|GET request to http://localhost:8000/api/categories/

params:
```JSON
{
    "title": "title",
    "description": "description",
    "image": null
}
```

DELETE|GET request to http://localhost:8000/api/categories/1

params:
```JSON
{
    "id": 1
}
```

response:

```JSON
{
    "id": 1,
    "title": "aa",
    "description": "sd ad",
    "image": "http://localhost:8000/media/categories/64c06101e21e4d1ea234e2ade028d0a1.jpg"
}
```


POST|GET request to http://localhost:8000/api/products/

params:
```JSON
{
    "title": "title",
    "price": 10,
    "image": null,
    "description": "hello",
    "category": 1
}
```

DELETE|GET request to http://localhost:8000/api/products/1

params:
```JSON
{
    "id":1
}
```

response:
```JSON
{
    "id":1,
    "title": "title",
    "price": 10,
    "image": null,
    "description": "hello",
    "category": 1
}
```


### Searching
searching is done through elasticsearch

```python
class SearchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            products = ProductDocument.search().query("multi_match", query=query, fields=['title', 'description'])
            results = products.to_queryset()
        else:
            results = Product.objects.none()

        serializer = ProductSerializer(results, many=True)
        return Response(serializer.data)
```


Everytime new products adds, it throws signal to create new index in elasticsearch



```python

product/signals.py

@receiver(post_save, sender=Product)
def update_document(sender, instance, **kwargs):
    ProductDocument().update(instance)

@receiver(post_delete, sender=Product)
def delete_document(sender, instance, **kwargs):
    ProductDocument().delete(instance)

```



Get request: http://127.0.0.1:8000/api/search/?q=chikomo
response:

```JSON
[
    {
        "id": 1,
        "title": "chikomo",
        "price": "14.00",
        "image": "/media/products/15455bd605484cfb9ff550a3ef1fc1e5.jpg",
        "description": "1asdq",
        "category": 1
    }
]
```


manual creating index (optional):

```
docker exec -it src_web_1 python3 manage.py search_index --rebuild
```


## Addiotionally added few tests ;)

```
docker exec -it src_web_1 python3 manage.py test
```