import asyncio
import json
import logging
import tempfile
import os

from config import Xray

logger = logging.getLogger(__name__)

Test_Link = "http://www.gstatic.com/generate_204"
Timeout = 10


# конвертирует ссылку в xray-конфиг
def _build_xray_config(link: str) -> dict:
    if link.startswith("vless://"):
        return _parse_vless(link)
    else:
        raise ValueError(f"Неподдерживаемый протокол (позже добавлю): {link[:10]}")


def _parse_vless(link: str) -> dict:
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(link)
    params = parse_qs(parsed.query)

    address = parsed.hostname
    rport = parsed.port
    uuid = parsed.username

    security = params.get("security", ["none"])[0]
    flow = params.get("flow", [""])[0]
    sni = params.get("sni", [""])[0]
    fp = params.get("fp", [""])[0]
    pbk = params.get("pbk", [""])[0]
    sid = params.get("sid", [""])[0]

    stream = {"network": "tcp"}
    if security == "reality":
        stream = {
            "network": "tcp",
            "security": "reality",
            "realitySettings": {
                "serverName": sni,
                "fingerprint": fp or "chrome",
                "publicKey": pbk,
                "shortId": sid,
            },
        }
    elif security == "tls":
        stream = {
            "network": "tcp",
            "security": "tls",
            "tlsSettings": {"serverName": sni} if sni else {},
        }

    return {
        "inbounds": [{"port": 1080, "listen": "127.0.0.1", "protocol": "socks", "settings": {"udp": True}}],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {"vnext": [{"address": address, "port": rport, "users": [{"id": uuid, "flow": flow, "encryption": "none"}]}]},
                "streamSettings": stream,
            }
        ],
    }


# проверяет конфиг запуском xray и запросом
async def _test_config(link: str) -> bool:
    try:
        config = _build_xray_config(link)
    except Exception as e:
        logger.debug("Спарсить не вышло: %s", e)
        return False

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        proc = await asyncio.create_subprocess_exec(
            Xray, "run", "-config", config_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.sleep(2)

        if proc.returncode is not None:
            logger.debug("Xray упал %s", link[:30])
            return False

        try:
            import aiohttp
            from aiohttp_socks import ProxyConnector

            connector = ProxyConnector.from_url("socks5://127.0.0.1:1080", rdns=True)
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=Timeout)) as session:
                async with session.get(Test_Link) as resp:
                    ok = resp.status == 204
        except Exception:
            ok = False
        finally:
            proc.terminate()
            await proc.wait()

        return ok
    except Exception as e:
        logger.debug("Ошибка тестов: %s", e)
        return False
    finally:
        os.unlink(config_path)


# возвращает первый рабочий конфиг
async def find_working_config(configs: list[str]) -> str | None:
    for link in configs:
        if await _test_config(link):
            return link
    return None
