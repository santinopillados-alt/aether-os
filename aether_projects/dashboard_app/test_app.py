import pytest
import asyncio
import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import pandas as pd
import numpy as np
from faker import Faker
from freezegun import freeze_time
import websocket
from redis import Redis
from sqlalchemy.orm import Session
from prometheus_client import CollectorRegistry, Counter, Histogram, Gauge

fake = Faker()


class DashboardDataGenerator:
    @staticmethod
    def generate_time_series(points: int = 100) -> List[Dict[str, Any]]:
        base_time = datetime.now() - timedelta(hours=points)
        return [
            {
                "timestamp": (base_time + timedelta(hours=i)).isoformat(),
                "value": float(np.random.normal(100, 15)),
                "volume": int(np.random.poisson(1000))
            }
            for i in range(points)
        ]

    @staticmethod
    def generate_chart_data(chart_type: str) -> Dict[str, Any]:
        if chart_type == "line":
            return {
                "labels": [f"Point {i}" for i in range(10)],
                "datasets": [{
                    "label": "Series 1",
                    "data": [float(np.random.uniform(0, 100)) for _ in range(10)]
                }]
            }
        elif chart_type == "bar":
            return {
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "datasets": [{
                    "label": "Revenue",
                    "data": [float(np.random.uniform(10000, 50000)) for _ in range(4)]
                }]
            }
        elif chart_type == "pie":
            return {
                "labels": ["Category A", "Category B", "Category C"],
                "data": [float(np.random.uniform(10, 40)) for _ in range(3)]
            }
        elif chart_type == "scatter":
            return {
                "datasets": [{
                    "label": "Cluster 1",
                    "data": [{"x": float(np.random.uniform(-10, 10)), 
                             "y": float(np.random.uniform(-10, 10))} for _ in range(20)]
                }]
            }
        return {}


class MockAnalyticsDashboard:
    def __init__(self, db_session: Session, redis_client: Redis, ws_client: websocket.WebSocket):
        self.db_session = db_session
        self.redis_client = redis_client
        self.ws_client = ws_client
        self.data_generator = DashboardDataGenerator()
        self.metrics_registry = CollectorRegistry()
        self.request_counter = Counter('dashboard_requests_total', 'Total requests', registry=self.metrics_registry)
        self.response_time = Histogram('dashboard_response_seconds', 'Response time', registry=self.metrics_registry)
        self.active_users = Gauge('dashboard_active_users', 'Active users', registry=self.metrics_registry)

    async def get_chart_data(self, chart_id: str, chart_type: str) -> Dict[str, Any]:
        self.request_counter.inc()
        with self.response_time.time():
            cache_key = f"chart:{chart_id}:{chart_type}"
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            data = self.data_generator.generate_chart_data(chart_type)
            self.redis_client.setex(cache_key, 300, json.dumps(data))
            return data

    async def get_real_time_data(self, stream_id: str) -> AsyncMock:
        async def stream_generator():
            for _ in range(10):
                yield {
                    "timestamp": datetime.now().isoformat(),
                    "value": float(np.random.normal(50, 10)),
                    "stream_id": stream_id
                }
                await asyncio.sleep(0.1)
        return stream_generator()

    async def aggregate_metrics(self, metric_type: str, period: str) -> Dict[str, Any]:
        periods = {"1h": 1, "24h": 24, "7d": 168, "30d": 720}
        hours = periods.get(period, 24)
        
        data = self.data_generator.generate_time_series(hours)
        df = pd.DataFrame(data)
        
        return {
            "metric_type": metric_type,
            "period": period,
            "mean": float(df["value"].mean()),
            "median": float(df["value"].median()),
            "std": float(df["value"].std()),
            "min": float(df["value"].min()),
            "max": float(df["value"].max()),
            "total_volume": int(df["volume"].sum())
        }

    def send_websocket_update(self, channel: str, data: Dict[str, Any]) -> bool:
        try:
            message = json.dumps({"channel": channel, "data": data})
            self.ws_client.send(message)
            return True
        except Exception:
            return False

    async def get_dashboard_config(self, dashboard_id: str) -> Dict[str, Any]:
        return {
            "id": dashboard_id,
            "name": f"Dashboard {dashboard_id}",
            "charts": [
                {"id": f"chart_{i}", "type": t, "position": {"x": i % 3, "y": i // 3}}
                for i, t in enumerate(["line", "bar", "pie", "scatter"])
            ],
            "refresh_interval": 5000,
            "theme": "dark"
        }


@pytest.fixture
def mock_db_session():
    session = Mock(spec=Session)
    session.query = Mock(return_value=Mock(filter=Mock(return_value=Mock(all=Mock(return_value=[])))))
    return session


@pytest.fixture
def mock_redis_client():
    client = Mock(spec=Redis)
    client.get = Mock(return_value=None)
    client.setex = Mock(return_value=True)
    client.publish = Mock(return_value=1)
    return client


@pytest.fixture
def mock_ws_client():
    client = Mock(spec=websocket.WebSocket)
    client.send = Mock(return_value=None)
    client.recv = Mock(return_value='{"type": "ping"}')
    return client


@pytest.fixture
def dashboard(mock_db_session, mock_redis_client, mock_ws_client):
    return MockAnalyticsDashboard(mock_db_session, mock_redis_client, mock_ws_client)


@pytest.mark.asyncio
class TestChartData:
    async def test_get_line_chart_data(self, dashboard):
        result = await dashboard.get_chart_data("chart1", "line")
        assert "labels" in result
        assert "datasets" in result
        assert len(result["datasets"]) > 0
        assert "data" in result["datasets"][0]
        assert len(result["datasets"][0]["data"]) == len(result["labels"])

    async def test_get_bar_chart_data(self, dashboard):
        result = await dashboard.get_chart_data("chart2", "bar")
        assert "labels" in result
        assert "datasets" in result
        assert result["labels"] == ["Q1", "Q2", "Q3", "Q4"]
        assert all(isinstance(v, float) for v in result["datasets"][0]["data"])

    async def test_get_pie_chart_data(self, dashboard):
        result = await dashboard.get_chart_data("chart3", "pie")
        assert "labels" in result
        assert "