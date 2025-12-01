from datetime import date

import pytest

from app.services.crud import create_submission, get_history


@pytest.mark.asyncio
class TestCRUDEdgeCases:
    async def test_get_history_empty_filters(self, db_session):
        """Тест получения истории без дополнительных фильтров"""
        async for session in db_session:
            # Создаем разнообразные тестовые данные
            test_data = [
                (date(2024, 1, 10), "User1", "Last1"),
                (date(2024, 1, 11), "User2", "Last2"),
                (date(2024, 1, 12), "User3", "Last3"),
            ]

            for test_date, first_name, last_name in test_data:
                await create_submission(session, test_date, first_name, last_name)

            # Тест без фильтров (только дата)
            result = await get_history(session, filter_date=date(2024, 1, 12))

            # Должны вернуться все записи до указанной даты
            assert result["total"] == 3
            assert len(result["items"]) == 3

            # Проверяем сортировку (по убыванию даты)
            dates = [item["date"] for item in result["items"]]
            assert dates == ["2024-01-12", "2024-01-11", "2024-01-10"]

    async def test_get_history_nonexistent_filters(self, db_session):
        """Тест получения истории с несуществующими фильтрами"""
        async for session in db_session:
            # Создаем тестовые данные
            await create_submission(session, date(2024, 1, 15), "Existing", "User")

            # Тест с фильтрами, которые не соответствуют данным
            result = await get_history(
                session,
                filter_date=date(2024, 1, 15),
                first_name="NonExistent",  # Несуществующее имя
                last_name="User",
            )

            # Не должно быть результатов
            assert result["total"] == 0
            assert result["items"] == []

    async def test_get_history_early_date(self, db_session):
        """Тест получения истории с очень ранней датой"""
        async for session in db_session:
            # Создаем тестовые данные
            await create_submission(session, date(2024, 1, 15), "Test", "User")

            # Тест с датой до всех записей
            result = await get_history(
                session, filter_date=date(2023, 1, 1)  # Очень ранняя дата
            )

            # Не должно быть результатов
            assert result["total"] == 0
            assert result["items"] == []

    async def test_get_history_same_date_different_users(self, db_session):
        """Тест получения истории с одинаковой датой но разными пользователями"""
        async for session in db_session:
            # Создаем записи с одинаковой датой но разными именами
            same_date = date(2024, 1, 15)
            test_users = [
                ("UserA", "Last1"),
                ("UserB", "Last2"),
                ("UserC", "Last3"),
            ]

            for first_name, last_name in test_users:
                await create_submission(session, same_date, first_name, last_name)

            result = await get_history(session, filter_date=same_date)

            # Должны вернуться все 3 записи
            assert result["total"] == 3
            assert len(result["items"]) == 3

            # Проверяем что count для всех записей = 0 (нет предыдущих записей с такой же комбинацией имени)
            for item in result["items"]:
                assert item["count"] == 0

    async def test_create_submission_special_characters(self, db_session):
        """Тест создания записи со специальными символами в именах"""
        async for session in db_session:
            # Тестируем различные символы (кроме пробелов)
            test_cases = [
                ("Jean-Luc", "O'Conner"),
                ("María", "José"),
                ("Иван", "Петров"),
                ("User123", "Name456"),
            ]

            for first_name, last_name in test_cases:
                submission = await create_submission(
                    session,
                    date=date(2024, 1, 15),
                    first_name=first_name,
                    last_name=last_name,
                )

                assert submission.first_name == first_name
                assert submission.last_name == last_name
