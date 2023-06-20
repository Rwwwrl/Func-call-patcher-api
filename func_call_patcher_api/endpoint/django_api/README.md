### Setup

1. В **INSTALLED_APPS** добавить `"func_call_patcher_api.endpoint.django_api"`
2. В **TEMPLATES.DIRS** добавить `BASE_DIR / 'templates'`
3. В **MIDDLEWARE** добавить `"func_call_patcher_api.endpoint.django_api.middleware.FuncCallPatcherMiddleware"`
4. В **urlpatterns** добавить `path('func_patcher_api/', include('func_call_patcher_api.endpoint.django_api.urls'))`

Теперь при заходе на _/func_patcher_api/_ появится страница с добавлением патчей
![alt](/readme_assets/django_api/start_page.png)

Добавить новый патч можно нажав на кнопку "add call patcher"
![alt](/readme_assets/django_api/func_call_patcher_api.gif)

Патч функций происходит в отдельной _middleware_ ("func_call_patcher_api.endpoint.django_api.middleware.FuncCallPatcherMiddleware"), поэтому добавление/обновление патчей на странице будет иметь эффект сразу без перезагрузки сервера.
