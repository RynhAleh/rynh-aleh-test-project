import pytest
from app.exceptions import validation_exception_handler
from fastapi import Request
from fastapi.exceptions import RequestValidationError


@pytest.mark.asyncio
class TestExceptions:
    async def test_validation_exception_handler_single_error(self):
        """Тест обработки одной ошибки валидации"""
        # Создаем mock ошибку валидации
        mock_exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "first_name"),
                    "msg": "No whitespace in first name is allowed",
                    "type": "value_error",
                }
            ]
        )

        # Создаем mock request
        mock_request = Request(scope={"type": "http"})

        # Обрабатываем ошибку
        response = await validation_exception_handler(mock_request, mock_exc)

        assert response.status_code == 400
        data = response.body.decode()
        assert "first_name" in data
        assert "No whitespace in first name is allowed" in data

    async def test_validation_exception_handler_multiple_errors(self):
        """Тест обработки нескольких ошибок валидации"""
        mock_exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "first_name"),
                    "msg": "No whitespace in first name is allowed",
                    "type": "value_error",
                },
                {
                    "loc": ("body", "last_name"),
                    "msg": "Field required",
                    "type": "value_error.missing",
                },
            ]
        )

        mock_request = Request(scope={"type": "http"})

        response = await validation_exception_handler(mock_request, mock_exc)

        assert response.status_code == 400
        data = response.body.decode()
        assert "first_name" in data
        assert "last_name" in data

    async def test_validation_exception_handler_value_error_parsing(self):
        """Тест парсинга ValueError сообщений"""
        mock_exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "date"),
                    "msg": "value error, Invalid date format",
                    "type": "value_error",
                }
            ]
        )

        mock_request = Request(scope={"type": "http"})

        response = await validation_exception_handler(mock_request, mock_exc)

        assert response.status_code == 400
        data = response.body.decode()
        # Должен убрать "value error," из сообщения
        assert "Invalid date format" in data
