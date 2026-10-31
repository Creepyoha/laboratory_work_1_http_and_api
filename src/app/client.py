"""
Описание запроса создания горячего кофе
---------------------------------------
Заполните этот docstring после исследования API.

Укажите:
- HTTP-метод и URL;
- необходимые заголовки;
- параметры JSON-тела (тип, обязательность, ограничения);
- какие поля задаёт клиент, а какие создаёт сервер;
- ожидаемый успешный статус и форму ответа;
- какие правила подтверждены запросами к API, а какие проверяете только в клиенте.

Формальная OpenAPI / JSON Schema не требуется.
"""

import requests
import exceptions

JsonObject = dict[str, object]


class SampleApisCoffeeClient:
    def __init__(
        self,
        base_url: str = "https://api.sampleapis.com/coffee/iced",
        timeout: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def CheckStatusCode(status: int) -> bool:
        if status < 400:
            return True
        else:
            return False

    def list_drinks(self) -> list[JsonObject]:
        request = requests.get(self._base_url, timeout = self._timeout)
        if self.CheckStatusCode(request.status_code):
            return request.json
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError

    def get_drink(self, drink_id: int) -> JsonObject:
        request = requests.get(self._base_url + f"/{drink_id}", timeout = self._timeout)
        if self.CheckStatusCode(request):
            return request
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError

    def create_drink(self, payload: JsonObject) -> JsonObject:
        existenceRequest = requests.get(self._base_url + f"/{payload["id"]}", timeout = self._timeout)
        if not self.CheckStatusCode(existenceRequest):
            request = requests.post(url = self._base_url, timeout = self._timeout, data = payload)

            if self.CheckStatusCode(request.status_code):
                return request.json
            else:
                raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError
        else:
            return existenceRequest.json

    def replace_drink(
        self,
        drink_id: int,
        payload: JsonObject,
    ) -> JsonObject:
        existenceRequest = requests.get(self._base_url + f"/{drink_id}", timeout = self._timeout)
        if self.CheckStatusCode(existenceRequest):
            request = requests.put(url = self._base_url + f"/{drink_id}", timeout = self._timeout, data = payload)

            if self.CheckStatusCode(request.status_code):
                return request.json
            else:
                raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError

    def update_drink(
        self,
        drink_id: int,
        changes: JsonObject,
    ) -> JsonObject:
        existenceRequest = requests.get(self._base_url + f"/{drink_id}", timeout = self._timeout)
        if self.CheckStatusCode(existenceRequest):
            request = requests.patch(url = self._base_url + f"/{drink_id}", timeout = self._timeout, data = changes)

            if self.CheckStatusCode(request.status_code):
                return request.json
            else:
                raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError

    def delete_drink(self, drink_id: int) -> None:
        existenceRequest = requests.get(self._base_url + f"/{drink_id}", timeout = self._timeout)
        if self.CheckStatusCode(existenceRequest):
            request = requests.delete(url = self._base_url + f"/{drink_id}", timeout = self._timeout)

            if self.CheckStatusCode(request.status_code):
                return request.json
            else:
                raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError

    def _request(
        self,
        method: str,
        path: str = "",
        payload: JsonObject | None = None,
    ) -> requests.Response:
        return requests.request(method = method, url = self._base_url + '/' + path, data = payload)