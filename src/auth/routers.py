from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import logging
from typing import Annotated, Any
import jwt
from .config import SECRET_KEY, ALGORITHM
from .depends import oauth2Scheme
from .auth import Authenticator
from .models import Token, UserWithPWD
from .exceptions import AuthException

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

userAuth = Authenticator()

@router.post("/token", response_model=Token)
async def authUser(
    data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        await userAuth.authUser(UserWithPWD(login=data.username, password=data.password))
        if not await isUserActive(data.username):
            token = userAuth.token_creater.getJWT(data.username, scopes=data.scopes)
            await userAuth.session.create(token=token.access_token, user=data.username)
        else:
            access_token = (await userAuth.session.get(data.username)).session
            token = Token(access_token=access_token, token_type="bearer")
        return token
    except AuthException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

def getCurrentTokenPayload(token: Annotated[str, Depends(oauth2Scheme)]):
    try:
        logger.debug("Decoding token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except:
        raise HTTPException(detail='Invalid token', status_code=403)

def getCurrentUser(payload: Annotated[str, Depends(getCurrentTokenPayload)]):
    username: str = payload
    if not username:
        raise HTTPException(status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
    logger.debug(f"Current user is {username}")
    return username

async def isUserActive(currentUser) -> bool:
    res = await userAuth.session.get(currentUser)
    logger.debug(f"{currentUser} is {'active' if res else 'not active'}")
    return True if res else False

async def getCurrentActiveUser(currentUser: Annotated[str, Depends(getCurrentUser)]):
    if not await isUserActive(currentUser):
        raise HTTPException(detail='Invalid token', status_code=403)
    return currentUser


@router.post("/exit")
async def dropSession(token: Annotated[str, Depends(oauth2Scheme)]) -> int | Any:
    try:
        return await userAuth.session.drop(token=token)
    except Exception:
        raise HTTPException(
            status_code=500,
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/user/me")
def getUser(currentActiveUser: Annotated[str, Depends(getCurrentActiveUser)]):
    try:
       return currentActiveUser
    except AuthException as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
            headers={"WWW-Authenticate": "Bearer"},
        )