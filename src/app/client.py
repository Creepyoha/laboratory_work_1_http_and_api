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

    def list_drinks(self) -> list[JsonObject]:
        return self._request(method = "lst").json

    def get_drink(self, drink_id: int) -> JsonObject:
        return self._request(method = "get", path = drink_id).json

    def create_drink(self, payload: JsonObject) -> JsonObject:
        return self._request(method = "crt", payload = payload).json

    def replace_drink(
        self,
        drink_id: int,
        payload: JsonObject,
    ) -> JsonObject:
        return self._request(method = "rpl", path = drink_id, payload = payload)

    def update_drink(
        self,
        drink_id: int,
        changes: JsonObject,
    ) -> JsonObject:
        return self._request(method = "upd", path = drink_id, payload = changes)

    def delete_drink(self, drink_id: int) -> None:
        self._request(method = "del", path = drink_id)

    def _request(
        self,
        method: str,
        path: str = "",
        payload: JsonObject | None = None,
    ) -> requests.Response:
        request
        if method == "lst":
            request = requests.get(self._base_url, timeout = self._timeout)
        elif method == "get":
            request = requests.get(self._base_url + f"/{path}", timeout = self._timeout)
        elif method == "crt":
            try:
                request = self._request(method = "get", path = payload["id"])
            except exceptions.CoffeeNotFoundError:
                request = requests.post(url = self._base_url, timeout = self._timeout, data = payload)
            except exceptions.CoffeeApiError:
                raise exceptions.CoffeeApiError
            else:
                return request
        elif method == "rpl":
            self._request(method = "get", path = path)
            request = requests.put(url = self._base_url + f"/{path}", timeout = self._timeout, data = payload)
        elif method == "upd":
            self._request(method = "get", path = path)
            request = requests.patch(url = self._base_url + f"/{path}", timeout = self._timeout, data = payload)
        elif method == "del":
            self._request(method = "get", path = path)
            request = requests.delete(url = self._base_url + f"/{path}", timeout = self._timeout)

        if request.status_code < 400:
            return request
        else:
            raise exceptions.CoffeeNotFoundError if request.status_code < 500 else exceptions.CoffeeApiError