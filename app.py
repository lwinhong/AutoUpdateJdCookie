from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from main import main as main_just_one
import threading
import uvicorn
import asyncio


def run_flask_main():

    app = FastAPI()
    # 将 "static" 目录中的文件作为静态文件提供
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def read_index():
        return {"message": "访问 /static/index.html 来查看 index.html 文件"}

    @app.get("/auto")
    def auto_jd():

        def run_main():  # 定义一个函数，用于运行main函数
            asyncio.run(main_just_one(mode="cron"))

        threading.Thread(target=run_main).start()
        return "已运行自动脚本"

    return app


if __name__ == "__main__":

    app = run_flask_main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
