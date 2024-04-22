import re

import uvicorn
from fastapi import FastAPI, Request

from contacts.routes import router

app = FastAPI()

app.include_router(router)

@app.middleware("http")
async def define_response(request: Request,
                          call_next):
    browser_regexp = (r"Mozilla|Chrome|Chromium|Apple|WebKit|" +
                      r"Edge|IE|MSIE|Firefox|Gecko")
    ua_string = request.headers.get('user-agent')
    if re.search(browser_regexp, ua_string):
        response_type = "html"
    else:
        response_type = "api"
    request.headers.__dict__["_list"].append(
        ("response-type".encode(), response_type.encode())
    )
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app="main:app",
                host="localhost",
                port=8080,
                reload=True)
