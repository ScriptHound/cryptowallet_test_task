from dependency_injector import containers, providers
from database.configuration import Database
from user.repositories import UserRepository
from wallet.repositories import WalletRepository
from wallet.services import UserWalletService


class WalletContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".views"])

    db = providers.Singleton(Database)

    wallet_repository = providers.Factory(
        WalletRepository,
        session_factory=db.provided.session,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    wallet_usecase = providers.Factory(
        UserWalletService,
        wallet_repository=wallet_repository,
        user_repository=user_repository,
    )
