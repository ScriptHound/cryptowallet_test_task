from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.configuration import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    full_name: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)
    wallets: Mapped["WalletModel"] = relationship("WalletModel", back_populates="user")
