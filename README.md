# FuncCallPatcherApi

Надстройка над [FuncCallPatcher](https://github.com/Rwwwrl/Func-call-patcher) для удобного патча в джанговых проектах через вебинтерфейс без перезагрузки сервера

### Setup

1. В INSTALLED_APPS добавить `"func_call_patcher_api.endpoint.django_api"`
2. В TEMPLATES.DIRS добавить `BASE_DIR / 'templates'`
3. В MIDDLEWARE добавить `"func_call_patcher_api.endpoint.django_api.middleware.FuncCallPatcherMiddleware"`
4. В urls.py добавить `path('func_patcher_api/', include('func_call_patcher_api.endpoint.django_api.urls'))`

Теперь при заходе на _/func_patcher_api/_ появится страница с добавлением патчей
![alt](func_call_patcher_api/static/readme_images/start_page.png)

Добавить новый патч можно нажав на кнопку "add call patcher".
