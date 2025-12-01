from unittest.mock import AsyncMock, Mock, patch

import pytest
from app.middleware import RandomDelayMiddleware
from fastapi import Request


@pytest.mark.asyncio
class TestMiddleware:
    async def test_random_delay_middleware_api_endpoints(self):
        """Test of middleware with random delay for API endpoints"""
        middleware = RandomDelayMiddleware(Mock())

        # Mock requests to API endpoints
        api_endpoints = ["/api/submit", "/api/history"]

        for endpoint in api_endpoints:
            mock_request = Mock(spec=Request)
            mock_request.url.path = endpoint

            mock_call_next = AsyncMock(return_value=Mock())

            # Test with delay
            with patch("asyncio.sleep") as mock_sleep:
                await middleware.dispatch(mock_request, mock_call_next)

                # Check if sleep was called for API endpoints
                mock_sleep.assert_called_once()
                delay_time = mock_sleep.call_args[0][0]
                assert 0.1 <= delay_time <= 3.0

    async def test_random_delay_middleware_other_endpoints(self):
        """Test of middleware WITHOUT delay for other endpoints"""
        middleware = RandomDelayMiddleware(Mock())

        # Mock requests to other endpoints (non-API)
        other_endpoints = ["/", "/docs", "/health"]

        for endpoint in other_endpoints:
            mock_request = Mock(spec=Request)
            mock_request.url.path = endpoint

            mock_call_next = AsyncMock(return_value=Mock())

            # Test without delay
            with patch("asyncio.sleep") as mock_sleep:
                await middleware.dispatch(mock_request, mock_call_next)

                # Check if sleep WASN'T called for other endpoints
                mock_sleep.assert_not_called()

    async def test_random_delay_middleware_response_passthrough(self):
        """Test if middleware conveys response correctly"""
        middleware = RandomDelayMiddleware(Mock())

        mock_request = Mock(spec=Request)
        mock_request.url.path = "/api/submit"

        expected_response = Mock()
        mock_call_next = AsyncMock(return_value=expected_response)

        with patch("asyncio.sleep"):
            actual_response = await middleware.dispatch(mock_request, mock_call_next)

            # Check if response is conveyed correctly
            assert actual_response == expected_response
            mock_call_next.assert_called_once_with(mock_request)
