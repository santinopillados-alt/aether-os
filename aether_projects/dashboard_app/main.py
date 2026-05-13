from fastapi import FastAPI, WebSocket, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import random
import time
import logging
from collections import deque
from dataclasses import dataclass, asdict
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Analytics Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MetricType(str, Enum):
    REVENUE = "revenue"
    USERS = "users"
    CONVERSION = "conversion"
    TRAFFIC = "traffic"
    PERFORMANCE = "performance"

class TimeRange(str, Enum):
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    YEAR = "1y"

class ChartType(str, Enum):
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    AREA = "area"
    SCATTER = "scatter"

@dataclass
class DataPoint:
    timestamp: datetime
    value: float
    metric: str
    
class MetricRequest(BaseModel):
    metric_type: MetricType
    time_range: TimeRange
    chart_type: ChartType = ChartType.LINE
    aggregation: Optional[str] = "avg"
    
class DashboardConfig(BaseModel):
    refresh_interval: int = Field(ge=1, le=60, default=5)
    max_data_points: int = Field(ge=10, le=1000, default=100)
    metrics: List[MetricType]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.data_buffer: Dict[str, deque] = {
            metric.value: deque(maxlen=1000) for metric in MetricType
        }
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                
manager = ConnectionManager()

class DataGenerator:
    @staticmethod
    def generate_revenue_data(points: int = 24) -> List[Dict[str, Any]]:
        base_value = 10000
        data = []
        current_time = datetime.now()
        for i in range(points):
            timestamp = current_time - timedelta(hours=points-i)
            value = base_value + random.uniform(-2000, 3000) + (i * 50)
            data.append({
                "timestamp": timestamp.isoformat(),
                "value": round(value, 2),
                "currency": "USD"
            })
        return data
    
    @staticmethod
    def generate_user_data(points: int = 24) -> List[Dict[str, Any]]:
        base_users = 1000
        data = []
        current_time = datetime.now()
        for i in range(points):
            timestamp = current_time - timedelta(hours=points-i)
            active = int(base_users + random.uniform(-200, 300))
            new_users = int(random.uniform(50, 150))
            data.append({
                "timestamp": timestamp.isoformat(),
                "active_users": active,
                "new_users": new_users,
                "total_sessions": active + random.randint(100, 500)
            })
        return data
    
    @staticmethod
    def generate_conversion_data(points: int = 24) -> List[Dict[str, Any]]:
        data = []
        current_time = datetime.now()
        for i in range(points):
            timestamp = current_time - timedelta(hours=points-i)
            rate = random.uniform(2.5, 5.5)
            data.append({
                "timestamp": timestamp.isoformat(),
                "conversion_rate": round(rate, 2),
                "total_conversions": int(random.uniform(100, 300))
            })
        return data
    
    @staticmethod
    def generate_traffic_data(points: int = 24) -> List[Dict[str, Any]]:
        sources = ["organic", "direct", "social", "email", "referral"]
        data = []
        current_time = datetime.now()
        for i in range(points):
            timestamp = current_time - timedelta(hours=points-i)
            source_data = {}
            total = 0
            for source in sources:
                value = random.randint(100, 1000)
                source_data[source] = value
                total += value
            data.append({
                "timestamp": timestamp.isoformat(),
                "sources": source_data,
                "total": total,
                "bounce_rate": round(random.uniform(30, 60), 2)
            })
        return data
    
    @staticmethod
    def generate_performance_data(points: int = 24) -> List[Dict[str, Any]]:
        data = []
        current_time = datetime.now()
        for i in range(points):
            timestamp = current_time - timedelta(hours=points-i)
            data.append({
                "timestamp": timestamp.isoformat(),
                "cpu_usage": round(random.uniform(20, 80), 2),
                "memory_usage": round(random.uniform(30, 70), 2),
                "response_time": round(random.uniform(50, 200), 2),
                "error_rate": round(random.uniform(0, 2), 3)
            })
        return data

data_generator = DataGenerator()

class MetricsService:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 60
        
    def get_time_range_hours(self, time_range: TimeRange) -> int:
        mapping = {
            TimeRange.HOUR: 1,
            TimeRange.DAY: 24,
            TimeRange.WEEK: 168,
            TimeRange.MONTH: 720,
            TimeRange.YEAR: 8760
        }
        return mapping.get(time_range, 24)
    
    async def get_metric_data(self, metric_type: MetricType, time_range: TimeRange) -> Dict[str, Any]:
        cache_key = f"{metric_type}_{time_range}"
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
                
        hours = self.get_time_range_hours(time_range)
        points = min(hours, 100)
        
        data_generators = {
            MetricType.REVENUE: data_generator.generate_revenue_data,
            MetricType.USERS: data_generator.generate_user_data,
            MetricType.CONVERSION: data_generator.generate_conversion_data,
            MetricType.TRAFFIC: data_generator.generate_traffic_data,
            MetricType.PERFORMANCE: data_generator.generate_performance_data
        }
        
        