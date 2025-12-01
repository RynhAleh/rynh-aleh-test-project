import pytest


@pytest.mark.asyncio
class TestIntegration:
    async def test_full_flow(self, client):
        """Полный тест потока: submit → history"""
        # 1. Отправляем данные
        submit_data = {
            "date": "2024-01-20",
            "first_name": "Integration",
            "last_name": "Test",
        }

        async for client_instance in client:  # ← ИСПРАВЛЕНО
            submit_response = await client_instance.post(
                "/api/submit", json=submit_data
            )
            assert submit_response.status_code == 200
            assert submit_response.json() == {"success": True}

            # 2. Проверяем что данные появились в истории
            history_response = await client_instance.get(
                "/api/history", params={"date": "2024-01-20"}
            )
            assert history_response.status_code == 200

            history_data = history_response.json()
            assert history_data["total"] >= 1

            # Ищем нашу запись
            our_record = next(
                (
                    item
                    for item in history_data["items"]
                    if item["first_name"] == "Integration"
                    and item["last_name"] == "Test"
                ),
                None,
            )

            assert our_record is not None
            assert our_record["date"] == "2024-01-20"
