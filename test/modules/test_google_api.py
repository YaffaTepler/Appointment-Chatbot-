import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from modules import google_api as google_api_module


class TestCalendarFunctions(unittest.TestCase):

    @patch('modules.google_api.service_account.Credentials')
    @patch('modules.google_api.build')
    def test_get_calendar_service(self, mock_build, mock_credentials):
        mock_creds = MagicMock()
        mock_credentials.from_service_account_file.return_value = mock_creds
        service = google_api_module.get_calendar_service()
        self.assertTrue(mock_build.called)
        self.assertIsNotNone(service)

    @patch('modules.google_api.get_calendar_service')
    def test_get_available_days(self, mock_get_service):
        mock_service = MagicMock()
        mock_events = {
            'items': [
                {'start': {'dateTime': (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%dT10:00:00Z')}},
                {'start': {'dateTime': (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%dT11:00:00Z')}}
            ]
        }
        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_get_service.return_value = mock_service

        result = google_api_module.get_available_days()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch('modules.google_api.get_calendar_service')
    def test_get_available_slots_for_day(self, mock_get_service):
        mock_service = MagicMock()
        date_str = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
        mock_events = {
            'items': [
                {'start': {'dateTime': f"{date_str}T10:00:00"}},
                {'start': {'dateTime': f"{date_str}T11:00:00"}}
            ]
        }
        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_get_service.return_value = mock_service

        slots = google_api_module.get_available_slots_for_day(date_str)
        self.assertIn("09:00", slots)
        self.assertNotIn("10:00", slots)
        self.assertNotIn("11:00", slots)

if __name__ == '__main__':
    unittest.main()
