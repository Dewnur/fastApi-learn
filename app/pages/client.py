from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.api.deps import get_current_user, get_token
from app.api.v1.endpoints.auth import logout_user, login_user
from app.api.v1.endpoints.product import get_product_list

client_router = APIRouter()

templates = Jinja2Templates(directory='app/templates')


@client_router.get('')
async def get_main_page(
        request: Request,
        products=Depends(get_product_list),
        token=Depends(get_token)
):
    return templates.TemplateResponse(
        name='products.html',
        context={
            'request': request,
            'products': products,
            'token': token
        }
    )


@client_router.post('/logout')
async def logout_user(
        request: Request,
        logout=Depends(logout_user),
        products=Depends(get_product_list),

):
    return templates.TemplateResponse(
        name='products.html',
        context={
            'request': request,
            'products': products,
        }
    )


@client_router.get('/authentication')
async def authentication(
        request: Request,
):
    return templates.TemplateResponse(
        name='authentication.html',
        context={
            'request': request,
        }
    )


# @client_router.post('/login')
# async def login(
#         request: Request,
#         response=Depends(login_user),
#         products=Depends(get_product_list),
# ):
#     return templates.TemplateResponse(
#         name='products.html',
#         context={
#             'request': request,
#             'products': products,
#             'token': response['access_token'],
#         }
#     )
