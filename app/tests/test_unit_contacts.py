import unittest
import asyncio
from datetime import datetime, date
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models.db_models import User, Contact
from app.models.contact_model import PostRequestModel
from app.crud.contact_crud import create_contact_crud, get_contacts_crud


class TestContactRepository(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1)

    def test_create_contact_crud(self):
        data = PostRequestModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="1234567890",
            birthday="2000-01-01"
        )

        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        # Act
        import asyncio
        asyncio.run(create_contact_crud(data, self.user, self.db))

        # Assert
        self.db.add.assert_called()
        self.db.commit.assert_called()

    def test_get_contacts_crud(self):
        mock_contact = Contact(
            id=1,
            user_id=1,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="1234567890",
            birthday=date(2000, 1, 1),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.query().filter().offset().limit().all.return_value = [mock_contact]

        # Act
        result = asyncio.run(get_contacts_crud(0, 10, self.user, self.db))

        # Assert
        self.assertEqual(result.skip, 0)
        self.assertEqual(result.limit, 10)
        self.assertEqual(len(result.contacts), 1)


if __name__ == "__main__":
    unittest.main()
