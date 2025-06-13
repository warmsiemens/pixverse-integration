import io

import respx
import httpx

from app.models.video import PixverseGeneration


@respx.mock
def test_create_image2video_success(client, db_fixture):
    respx.post("https://app-api.pixverse.ai/openapi/v2/image/upload").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"img_id": 5, "img_url": 'qwer'}})
    )

    respx.post("https://app-api.pixverse.ai/openapi/v2/video/img/generate").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0,
                                               "ErrMsg": "string", "resp": {"video_id": 10}})
    )

    fake_file = io.BytesIO(b"fake image content")
    fake_file.name = "test_pic.jpg"

    response = client.post("/image2video", data={
            "prompt": "test1",
            "app_bundle_id": "idk1",
            "apphud_user_id": "user1234"
        },
        files={"image": ("test_pic.jpg", fake_file, "image/jpeg")}
    )

    assert response.status_code == 200

    videos = db_fixture.query(PixverseGeneration).all()
    assert len(videos) == 1
    assert videos[0].app_bundle_id == "idk1"
    assert videos[0].video_id == '10'
    assert videos[0].description == 'generate video from image'


@respx.mock
def test_create_image2video_error(client, db_fixture):
    respx.post("https://app-api.pixverse.ai/openapi/v2/image/upload").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"img_id": 5, "img_url": 'qwer'}})
    )

    respx.post("https://app-api.pixverse.ai/openapi/v2/video/img/generate").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "resp": {"video_d": 10}})
    )

    fake_file = io.BytesIO(b"fake image content")
    fake_file.name = "test_pic.jpg"

    response = client.post("/image2video", data={
            "prompt": "test1",
            "app_bundle_id": "idk1",
            "apphud_user_id": "user1234"
        },
        files={"image": ("test_pic.jpg", fake_file, "image/jpeg")}
    )

    assert response.status_code == 500



