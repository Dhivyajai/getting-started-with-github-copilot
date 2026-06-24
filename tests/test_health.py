def test_index_page(client):
    resp = client.get("/static/index.html")
    assert resp.status_code == 200
    assert "Mergington High School" in resp.text


def test_root_redirects(client):
    resp = client.get("/", follow_redirects=False)
    # app redirects to the static index page
    assert resp.status_code in (301, 302, 303, 307)
    assert resp.headers.get("location") == "/static/index.html"
