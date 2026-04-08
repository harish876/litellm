import asyncio

from litellm.llms.custom_httpx.http_handler import (
    get_async_httpx_client,
    httpxSpecialProvider,
)

URL = "http://localhost:4443/storage/v1/b/investigation/o/oom-file-endpoint.md?alt=media"
CHUNK_SIZE = 1024 * 1024


async def main() -> None:
    async_httpx_client = get_async_httpx_client(
        llm_provider=httpxSpecialProvider.LoggingCallback
    )

    async with async_httpx_client.client.stream("GET", URL) as response:
        response.raise_for_status()
        async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE):
            if chunk:
                print(chunk)


if __name__ == "__main__":
    asyncio.run(main())
