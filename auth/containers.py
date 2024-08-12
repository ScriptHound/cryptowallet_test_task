from dependency_injector import containers, providers

from database.configuration import Database
from user.repositories import UserRepository
from auth.usecases import UserUseCase


class UserContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".views"])

    db = providers.Singleton(Database)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_usecase = providers.Factory(
        UserUseCase,
        user_repository=user_repository,
    )
