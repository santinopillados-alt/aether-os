import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { format, subDays, startOfDay, endOfDay } from 'date-fns';
import axios from 'axios';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];
const REFRESH_INTERVAL = 5000;
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const MetricCard = ({ title, value, change, icon, loading, error }) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        {error ? (
          <p className="text-sm text-red-500 mt-1">Failed to load</p>
        ) : loading ? (
          <div className="h-8 bg-gray-200 rounded animate-pulse mt-1 w-24"></div>
        ) : (
          <>
            <p className="text-2xl font-semibold text-gray-900 mt-1">{value}</p>
            {change !== undefined && (
              <p className={text-sm mt-2 ${change >= 0 ? 'text-green-600' : 'text-red-600'}}>
                {change >= 0 ? '↑' : '↓'} {Math.abs(change)}%
              </p>
            )}
          </>
        )}
      </div>
      {icon && <div className="text-3xl">{icon}</div>}
    </div>
  </div>
);

const useAnalyticsData = (endpoint, refreshInterval = null) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(${API_BASE_URL}${endpoint});
      setData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
      console.error(Error fetching ${endpoint}:, err);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
    
    if (refreshInterval) {
      const interval = setInterval(fetchData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchData, refreshInterval]);

  return { data, loading, error, refetch: fetchData };
};

const AnalyticsDashboard = () => {
  const [dateRange, setDateRange] = useState({
    start: startOfDay(subDays(new Date(), 30)),
    end: endOfDay(new Date())
  });
  const [selectedMetric, setSelectedMetric] = useState('revenue');

  const { data: metrics, loading: metricsLoading, error: metricsError } = useAnalyticsData(
    /analytics/metrics?start=${dateRange.start.toISOString()}&end=${dateRange.end.toISOString()},
    REFRESH_INTERVAL
  );

  const { data: timeSeriesData, loading: timeSeriesLoading, error: timeSeriesError } = useAnalyticsData(
    /analytics/timeseries?metric=${selectedMetric}&start=${dateRange.start.toISOString()}&end=${dateRange.end.toISOString()},
    REFRESH_INTERVAL
  );

  const { data: categoryData, loading: categoryLoading, error: categoryError } = useAnalyticsData(
    /analytics/categories?start=${dateRange.start.toISOString()}&end=${dateRange.end.toISOString()}
  );

  const { data: realtimeData, loading: realtimeLoading, error: realtimeError } = useAnalyticsData(
    '/analytics/realtime',
    3000
  );

  const formattedTimeSeriesData = useMemo(() => {
    if (!timeSeriesData) return [];
    return timeSeriesData.map(item => ({
      ...item,
      date: format(new Date(item.date), 'MMM dd'),
      value: Number(item.value)
    }));
  }, [timeSeriesData]);

  const formattedCategoryData = useMemo(() => {
    if (!categoryData) return [];
    return categoryData.slice(0, 5).map(item => ({
      name: item.name,
      value: Number(item.value)
    }));
  }, [categoryData]);

  const handleDateRangeChange = useCallback((preset) => {
    const end = endOfDay(new Date());
    let start;
    
    switch (preset) {
      case '7d':
        start = startOfDay(subDays(end, 7));
        break;
      case '30d':
        start = startOfDay(subDays(end, 30));
        break;
      case '90d':
        start = startOfDay(subDays(end, 90));
        break;
      default:
        start = startOfDay(subDays(end, 30));
    }
    
    setDateRange({ start, end });
  }, []);

  const metricOptions = [
    { value: 'revenue', label: 'Revenue' },
    { value: 'users', label: 'Users' },
    { value: 'sessions', label: 'Sessions' },
    { value: 'conversions', label: 'Conversions' }
  ];

  const dateRangeOptions = [
    { value: '7d', label: 'Last 7 days' },
    { value: '30d', label: 'Last 30 days' },
    { value: '90d', label: 'Last 90 days' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <div className="flex items-center gap-4 mt-4">
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {metricOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="flex gap-2">
              {dateRangeOptions.map(option => (
                <button
                  key={option.value}
                  onClick={() => handleDateRangeChange(option.value)}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-blue-500"
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg