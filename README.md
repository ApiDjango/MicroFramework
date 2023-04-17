# MicroFramework

Этот пример микрофреймворка предоставляет два метода - GET и POST - для обработки запросов и обслуживает только базовые роуты. 
Вы можете добавить новые роуты с помощью декоратора route, как показано ниже:
```
@MicroFrameworkHandler.route('/')
def index(query_params):
    return {'message': 'Hello, World!'}

@MicroFrameworkHandler.route('/user')
def user(query_params):
    user_id = query_params.get('id')
    return {'user_id': user_id}
    
```

Чтобы запустить сервер с поддержкой SSL, вы можете вызвать функцию run_server следующим образом:
```
run_server(8080, use_ssl=True, ssl_certfile='server.crt', ssl_keyfile='server.key')
```
