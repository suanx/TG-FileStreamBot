import asyncio
import logging
import aiohttp
from WebStreamer import Var

logger = logging.getLogger("keep_alive")

_stop_event = asyncio.Event()


async def ping_server():
    sleep_time = Var.PING_INTERVAL
    logger.info("Started with {}s interval between pings".format(sleep_time))
    while True:
        try:
            await asyncio.wait([asyncio.sleep(sleep_time), _stop_event.wait()], return_when=asyncio.FIRST_COMPLETED)
            if _stop_event.is_set():
                logger.info("Keep-alive task stopped")
                break
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(Var.URL) as resp:
                    logger.info("Pinged server with response: {}".format(resp.status))
        except asyncio.CancelledError:
            logger.info("Keep-alive task cancelled")
            break
        except TimeoutError:
            logger.warning("Couldn't connect to the site URL..")
        except Exception:
            logger.error("Unexpected error: ", exc_info=True)


def stop_ping_server():
    """Stop the keep-alive ping task."""
    _stop_event.set()
