import asyncio
from datetime import datetime, timedelta
from croniter import croniter
from utils.consts import program
from config import cron_expression
from main import main
from loguru import logger


def get_next_runtime(cron_expression, base_time=None):
    base_time = base_time or datetime.now()
    cron = croniter(cron_expression, base_time)
    return cron.get_next(datetime)


async def run_scheduled_tasks(cron_expression):
    if isinstance(cron_expression, str):
        cron_expression = [cron_expression]
    logger.info(f"{program}运行中")
    next_run = [get_next_runtime(ce) for ce in cron_expression]
    next_run_time = next((x for x in sorted(set(next_run)) if x > datetime.now()), None)
    logger.info(f"下次更新任务时间为{next_run_time }")
    while True:
        now = datetime.now()
        for i in range(len(next_run)):
            if now >= next_run[i]:
                await main(mode="cron")
                next_run = [
                    get_next_runtime(ce, now + timedelta(seconds=1))
                    for ce in cron_expression
                ]
                next_run_time = next((x for x in sorted(set(next_run)) if x > datetime.now()), None)
                logger.info(f"下次更新任务时间为{next_run_time}")
        # if now >= next_run :
        #     await main(mode="cron")
        #     next_run = get_next_runtime(cron_expression, now + timedelta(seconds=1))
        #     logger.info(f"下次更新任务时间为{next_run}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_scheduled_tasks(cron_expression))
