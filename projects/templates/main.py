import fastapi
import uvicorn
from fastapi_chameleon import template, global_init

app = fastapi.FastAPI()

global_init('static')

@app.get("/")
@template(template_file='index.html')
def index():
    return {'username': 'John'}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
