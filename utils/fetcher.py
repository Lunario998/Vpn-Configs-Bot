import logging
import re

import aiohttp

from config import Github_Url

logger = logging.getLogger(__name__)

# все возможные протоколы
Config_Patterns = re.compile(r"(?:vless|vmess|ss|trojan)://[^\s]+", re.IGNORECASE)


async def fetch_configs() -> list[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(Github_Url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    logger.error("Github ответил %d", resp.status)
                    return []
                text = await resp.text()
    except Exception as e:
        logger.error("Ошибка: %s", e)
        return []

    configs = Config_Patterns.findall(text)
    if not configs:
        configs = Config_Patterns.findall(text.replace("\n", " "))

    return configs
