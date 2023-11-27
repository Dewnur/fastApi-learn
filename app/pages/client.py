from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.api.v1.endpoints.product import get_product_list
from app.api.v1.endpoints.profile import get_profile

client_router = APIRouter()

templates = Jinja2Templates(directory='app/templates')


@client_router.get('')
async def main(
        request: Request,
        products=Depends(get_product_list),
):
    return templates.TemplateResponse(
        name='products.html',
        context={
            'request': request,
            'products': products,
        }
    )


@client_router.get('/login')
async def login(
        request: Request,
):
    return templates.TemplateResponse(
        name='login.html',
        context={
            'request': request,
        }
    )


@client_router.get('/profile')
async def authentication(
        request: Request,
        profile=Depends(get_profile)
):
    print(profile.gender)
    return templates.TemplateResponse(
        name='profile.html',
        context={
            'request': request,
            'profile': profile
        }
    )


@client_router.get('/catalog')
async def authentication(
        request: Request,
):
    return templates.TemplateResponse(
        name='catalog.html',
        context={
            'request': request,
        }
    )
