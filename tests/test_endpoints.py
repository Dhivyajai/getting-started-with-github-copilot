import urllib.parse


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    activity = data["Chess Club"]
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_and_remove_participant(client):
    activity = "Chess Club"
    email = "test-student@example.com"

    # Ensure clean start: remove if already present
    data = client.get("/activities").json()
    if email in data[activity]["participants"]:
        client.delete(f"/activities/{activity}/participants/{urllib.parse.quote(email, safe='')}")

    # Sign up via query param
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")

    # Confirm added
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Cleanup: remove participant (email must be URL-encoded in path)
    encoded = urllib.parse.quote(email, safe='')
    resp2 = client.delete(f"/activities/{activity}/participants/{encoded}")
    assert resp2.status_code == 200

    # Confirm removed
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]
