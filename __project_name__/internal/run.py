import uvicorn

from settings.api import API_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "api.main:api",
        host=API_CONFIG.HOST,
        port=API_CONFIG.PORT,
        workers=API_CONFIG.WORKERS,
        reload=API_CONFIG.RELOAD,
    )
