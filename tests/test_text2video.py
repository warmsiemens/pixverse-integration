import respx
import httpx

from app.models.video import PixverseGeneration


@respx.mock
def test_create_text2video_success(client, db_fixture):
    respx.post("https://app-api.pixverse.ai/openapi/v2/video/text/generate").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"video_id": 15}})
    )
    response = client.post("/text2video", data={
        "prompt": "test",
        "app_bundle_id": "idk",
        "apphud_user_id": "user123"
    })

    assert response.status_code == 200

    videos = db_fixture.query(PixverseGeneration).all()
    assert len(videos) == 1
    assert videos[0].app_bundle_id == "idk"
    assert videos[0].video_id == '15'


@respx.mock
def test_create_text2video_error(client, db_fixture):
    respx.post("https://app-api.pixverse.ai/openapi/v2/video/text/generate").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"video_i": 15}})
    )
    response = client.post("/text2video", data={
        "prompt": "test",
        "app_bundle_id": "idk",
        "apphud_user_id": "user123"
    })

    assert response.status_code == 500
