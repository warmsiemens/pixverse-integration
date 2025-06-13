import respx
import httpx


@respx.mock
def test_generate_status_success(client, db_fixture):
    respx.get("https://app-api.pixverse.ai/openapi/v2/video/result/5").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"id": 0, "prompt": "string",
                                                        "status": 1, "url": "string1"}})
    )
    response = client.get("/get_status", params={
        "app_bundle_id": "idk",
        "apphud_user_id": "user123",
        "video_id": "5"
    })
    assert response.status_code == 200
    assert response.json()["url"] == "string1"


@respx.mock
def test_generate_status_failed(client, db_fixture):
    respx.get("https://app-api.pixverse.ai/openapi/v2/video/result/5").mock(
        return_value=httpx.Response(200, json={"ErrCode": 0, "ErrMsg": "string",
                                               "Resp": {"id": 0, "prompt": "string",
                                                        "status": 0, "url": "string1"}})
    )
    response = client.get("/get_status", params={
        "app_bundle_id": "idk",
        "apphud_user_id": "user123",
        "video_id": "5"
    })
    assert response.status_code == 500
