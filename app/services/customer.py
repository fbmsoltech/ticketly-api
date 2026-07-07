from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.base import BaseService


class CustomerService(BaseService[Customer, CustomerCreate, CustomerUpdate]):
    def __init__(self, repository: CustomerRepository) -> None:
        super().__init__(repository, Customer)
        self.customer_repository = repository

    def get_by_user_id(self, user_id: int) -> Customer | None:
        return self.customer_repository.get_by_user_id(user_id)
