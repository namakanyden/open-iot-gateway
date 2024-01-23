import httpx
from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from weather.dependencies import get_settings, get_mqtt

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.on_event("startup")
@repeat_every(seconds=60)  # 1 hour
def remove_expired_tokens_task() -> None:
    print('kurnik')

    params = {
        'q': get_settings().city,
        'units': 'metric',
        'appid': get_settings().token,
        'lang': 'en'
    }
    response = httpx.get('https://api.openweathermap.org/data/2.5/weather', params=params)



