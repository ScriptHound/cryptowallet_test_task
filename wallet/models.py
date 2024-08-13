from sqlalchemy import Integer, Column, Float, ForeignKey, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Numeric

from database.configuration import Base
from database.db_views import view


class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    balance: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="wallets")

    currencies = relationship("CurrencyModel", backref="CurrencyModel", secondary="wallet_currencies")
    transactions = relationship("TransactionModel", back_populates="wallet")
    def __repr__(self):
        return f"<Wallet(balance='{self.balance}')>"


class CurrencyModel(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=False)

    wallets = relationship("WalletModel", backref="WalletModel", secondary="wallet_currencies")

    def __repr__(self):
        return f"<Currency(name='{self.name}', symbol='{self.symbol}')>"


class WalletCurrencyModel(Base):
    __tablename__ = "wallet_currencies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))

    def __repr__(self):
        return f"<WalletCurrency(amount='{self.amount}', type='{self.transaction_type}')>"


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), index=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"), index=True)
    amount = mapped_column(Numeric(15, 2), nullable=False)
    outgoing: Mapped[bool] = mapped_column(nullable=False)
    wallet: Mapped["WalletModel"] = relationship("WalletModel", back_populates="transactions")
    currency: Mapped["CurrencyModel"] = relationship("CurrencyModel")

    def __repr__(self):
        return f"<Transaction(amount='{self.amount}', type='{self.transaction_type}')>"


# balance_query = (select(
#     WalletModel.user_id.label("user_id"),
#     WalletModel.id.label("wallet_id"),
#     CurrencyModel.name.label("currency_name"),
#     func.sum(TransactionModel.amount).label("balance"))
#                  .join(TransactionModel, WalletModel.id == TransactionModel.wallet_id)
#                  .join(CurrencyModel, TransactionModel.currency_id == CurrencyModel.id)
#                  .join(WalletCurrencyModel, WalletModel.id == WalletCurrencyModel.wallet_id)
#                  .group_by(WalletModel.user_id, WalletCurrencyModel.currency_id).alias("balance_view"))
#
# class BalanceView(Base):
#     __table__ = view(
#         "balance_view",
#         Base.metadata,
#         balance_query
#     )
