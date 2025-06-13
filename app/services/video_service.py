import time
import json

from typing import Optional, Dict, Any
import httpx

from fastapi import HTTPException
from app.core.config import settings

STATUS_DICT = {1: 'Generation successful', 5: 'Generating', 6: 'Deleted',
               7: 'Contents moderation failed', 8: 'Generation failed'}


def request_with_retry(method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
    for _ in range(settings.MAX_RETRIES):
        try:
            response = httpx.request(method, url, timeout=15, **kwargs)
            if response.status_code in settings.RETRY_STATUS_CODES:
                time.sleep(settings.RETRY_DELAY)
                continue
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502,
                                detail=f"HTTP error: {e.response.status_code} - {e.response.text}")

    raise HTTPException(status_code=504, detail="Max retries exceeded")


def _check_pixverse_error(response: Dict):
    if response.get("ErrCode", 0) != 0:
        raise HTTPException(
            status_code=502,
            detail=f"Pixverse error {response.get('ErrCode')}:"
                   f" {response.get('ErrMsg', 'Unknown error')}"
        )


def text2video(prompt: str) -> Optional[Dict[str, Any]]:
    url = f"{settings.BASE_URL}/video/text/generate"
    payload = json.dumps({
        "aspect_ratio": "16:9",
        "duration": 5,
        "model": "v3.5",
        "prompt": prompt,
        "quality": "540p",
    })
    headers = {
        'API-KEY': settings.API_KEY,
        'Ai-trace-id': '{{$string.uuid}}',
        'Content-Type': 'application/json'
    }

    response = request_with_retry("POST", url, data=payload, headers=headers)
    _check_pixverse_error(response)

    video_id = response.get("Resp", {}).get("video_id")
    if not video_id:
        raise HTTPException(status_code=500, detail="video_id not found")
    return video_id


def upload_image_to_get_id(image_data: bytes, filename: str):
    url = f"{settings.BASE_URL}/image/upload"
    files = {"image": (filename, image_data, "application/octet-stream")}
    headers = {
        'API-KEY': settings.API_KEY,
        'Ai-trace-id': '{{$string.uuid}}',
    }
    response = request_with_retry("POST", url, headers=headers, files=files)
    _check_pixverse_error(response)

    image_id = response.get("Resp", {}).get("img_id")
    if not image_id:
        raise HTTPException(status_code=500, detail="img_id not found")
    return image_id


def image2video(prompt: str, image_id: int) -> Optional[Dict[str, Any]]:
    url = f"{settings.BASE_URL}/video/img/generate"
    headers = {
        'API-KEY': settings.API_KEY,
        'Ai-trace-id': '{{$string.uuid}}',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "duration": 5,
        "img_id": image_id,
        "model": "v3.5",
        "prompt": prompt,
        "quality": "540p"

    })

    response = request_with_retry("POST", url, headers=headers, data=payload)
    _check_pixverse_error(response)

    video_id = (response.get("Resp", {}).get("video_id") or
                response.get("resp", {}).get("video_id"))
    if not video_id:
        raise HTTPException(status_code=500, detail="video_id not found")
    return video_id


def get_status_generate(generation_id: int) -> Optional[Dict[str, Any]]:
    url = f"{settings.BASE_URL}/video/result/{generation_id}"
    headers = {
        'API-KEY': settings.API_KEY,
        'Ai-trace-id': '{{$string.uuid}}',
    }

    response = request_with_retry("GET", url, headers=headers)
    _check_pixverse_error(response)

    status = STATUS_DICT.get(response.get("Resp", {}).get("status"), '')

    if not status:
        raise HTTPException(status_code=500, detail="status of generation not found")
    if status != 'Generation successful':
        return {'status': status}

    url_video = response.get("Resp", {}).get("url")
    if not url_video:
        raise HTTPException(status_code=500, detail="url of generation not found")
    return {'status': status, 'url': url_video}
