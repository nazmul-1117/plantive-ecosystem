
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.verification_token_model import VerificationToken

class VerificationTokenRepository:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def create_token(
            self,
            db_token: VerificationToken
    ) -> VerificationToken | None:

        self.session.add(db_token)
        await self.session.flush()

        return db_token
    
    
    async def get_by_hash(
            self,
            token_hash: str
    ) -> VerificationToken | None:
        
        statement = select(VerificationToken).where(
            VerificationToken.token_hash == token_hash
        )
        result = await self.session.exec(statement)
        return result.first()
    
    async def update(
            self,
            db_token: VerificationToken,
    ) -> VerificationToken:
        
        self.session.add(db_token)
        await self.session.flush()

        return db_token


    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)
        