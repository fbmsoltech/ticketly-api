import pytest
from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.services.customer import CustomerService
from tests.factories import create_customer, create_role, create_user

pytestmark = pytest.mark.integration


def test_customer_service_gets_customer_by_user_id(db_session: Session) -> None:
    role = create_role(db_session)
    customer_user = create_user(db_session, role=role, email="customer@example.com")
    customer = create_customer(db_session, user=customer_user)
    service = CustomerService(CustomerRepository(db_session))

    assert service.get_by_user_id(customer_user.id) == customer
