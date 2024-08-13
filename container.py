from dependency_injector import containers, providers

from auth.services import UserService
from database.configuration import Database
from user.repositories import UserRepository
from wallet.repositories import IWalletRepository, CurrencyRepository
from wallet.services import UserWalletService, CurrencyService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["auth.views", "user.views", "wallet.views"])

    db = providers.Singleton(Database)

    wallet_repository = providers.Factory(
        IWalletRepository,
        session_factory=db.provided.session,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    wallet_usecase = providers.Factory(
        UserWalletService,
        wallet_repository=wallet_repository,
        user_repository=user_repository,
    )

    currency_repository = providers.Factory(
        CurrencyRepository,
        session_factory=db.provided.session,
    )

    currency_service = providers.Factory(
        CurrencyService,
        currenct_repository=currency_repository,
    )
