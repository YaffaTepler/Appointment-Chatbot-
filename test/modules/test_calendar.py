import unittest
from unittest.mock import patch, MagicMock

from modules.calendar import add_appointment


class TestAddAppointment(unittest.TestCase):

    @patch('modules.calendar.get_calendar_service')
    def test_add_appointment_slot_taken(self, mock_get_service):
        mock_service = MagicMock()
        mock_events = MagicMock()
        mock_events.execute.return_value = {'items': ['existing event']}
        mock_service.events.return_value.list.return_value = mock_events
        mock_get_service.return_value = mock_service

        success, message = add_appointment("2025-05-15T10:00", "Alice")

        self.assertFalse(success)
        self.assertEqual(message, "Slot already booked. Please choose a different time.")

    @patch('modules.calendar.get_calendar_service')
    def test_add_appointment_success(self, mock_get_service):
        mock_service = MagicMock()
        mock_events_list = MagicMock()
        mock_events_list.execute.return_value = {'items': []}
        mock_events_insert = MagicMock()
        mock_events_insert.execute.return_value = {'htmlLink': 'http://fake-link'}

        mock_service.events.return_value.list.return_value = mock_events_list
        mock_service.events.return_value.insert.return_value = mock_events_insert
        mock_get_service.return_value = mock_service

        success, message = add_appointment("2025-05-15T11:00", "Bob")

        self.assertTrue(success)
        self.assertIn("Appointment created:", message)

if __name__ == '__main__':
    unittest.main()
