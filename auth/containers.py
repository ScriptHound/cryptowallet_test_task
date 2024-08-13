from dependency_injector import containers, providers

from database.configuration import Database
from user.repositories import UserRepository
from auth.services import UserService


class UserContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["auth.views", "user.views"])

    config = providers.Configuration()

    db = providers.Singleton(Database)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
