from orders.repositories.orders import OrdersRepositoryProtocol, OrdersRepositoryImpl
from orders.services.orders import OrdersServiceImpl, OrdersServiceProtocol


# --- repositories ---

def get_orders_repositories() -> OrdersRepositoryProtocol:
    return OrdersRepositoryImpl()

OrdersFactoryRepository =  get_orders_repositories()

# --- services ---

def get_orders_service(orders_factory_repositories: OrdersRepositoryProtocol) -> OrdersServiceProtocol:
    return OrdersServiceImpl(orders_factory_repositories)


OrdersService = get_orders_service(OrdersFactoryRepository)

