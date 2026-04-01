import re

from fastapi import FastAPI, HTTPException, Query, Response

app = FastAPI(title="Mock OpenAI Files API")


FILE_SIZES_MB = {
    "test-file-small": 1,
    "test-file-medium": 10,
    "test-file-large": 50,
}
DEFAULT_FILL_BYTE = b"a"


def _build_payload(size_mb: int, fill_byte: bytes = DEFAULT_FILL_BYTE) -> bytes:
    return fill_byte * (size_mb * 1024 * 1024)


def _resolve_size_mb(file_id: str) -> int | None:
    preset_size = FILE_SIZES_MB.get(file_id)
    if preset_size is not None:
        return preset_size

    match = re.fullmatch(r"test-file-(\d+)", file_id)
    if match is None:
        return None

    size_mb = int(match.group(1))
    if 1 <= size_mb <= 1024:
        return size_mb

    return None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/files/{file_id}/content")
async def get_file_content(
    file_id: str,
    content_type: str = Query(default="application/octet-stream"),
    filename: str | None = Query(default=None),
) -> Response:
    size_mb = _resolve_size_mb(file_id)
    if size_mb is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"unknown file_id '{file_id}'",
                "available_file_ids": list(FILE_SIZES_MB.keys()),
                "accepted_pattern": "test-file-{size_mb}",
            },
        )

    payload = _build_payload(size_mb=size_mb)
    resolved_filename = filename or f"{file_id}.bin"

    return Response(
        content=payload,
        media_type=content_type,
        headers={
            "content-length": str(len(payload)),
            "content-disposition": f'attachment; filename="{resolved_filename}"',
            "x-mock-file-id": file_id,
            "x-mock-size-mb": str(size_mb),
        },
    )
