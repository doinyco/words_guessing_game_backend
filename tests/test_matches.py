from datetime import datetime, timedelta
from app.models import MatchPlayer


def test_start_match(client):
    response = client.post("/matches/start")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "letter" in data
    assert len(data["letter"]) == 1
    assert data["letter"].isupper()

def test_join_match_creates_player(client):
    match = client.post("/matches/start").json()
    match_id = match["id"]

    r = client.post(f"/matches/{match_id}/join", json={"name": "Alice"})
    assert r.status_code == 200
    data = r.json()
    assert data["match_id"] == match_id
    assert data["player_name"] == "Alice"
    assert isinstance(data["player_id"], int)

def test_max_two_players_per_match(client):
    match_id = client.post("/matches/start").json()["id"]

    r1 = client.post(f"/matches/{match_id}/join", json={"name": "A"})
    assert r1.status_code == 200

    r2 = client.post(f"/matches/{match_id}/join", json={"name": "B"})
    assert r2.status_code == 200

    r3 = client.post(f"/matches/{match_id}/join", json={"name": "C"})
    assert r3.status_code == 400
    assert r3.json()["detail"] == "Match already has 2 players"

def test_submit_requires_join(client, db_session):
    # Start match
    match_id = client.post("/matches/start").json()["id"]

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    real_player_id = join["player_id"]

    r = client.post(f"/matches/{match_id}/submit?player_id=9999", json={"word": "sun"})
    
    assert r.status_code in (400, 404)

def test_submit_wrong_starting_letter(client, db_session):
    match = client.post("/matches/start").json()
    match_id = match["id"]

    from app.models import Match
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    r = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "apple"})
    assert r.status_code == 400
    assert "Word must start with" in r.json()["detail"]

def test_submit_invalid_dictionary_word(client, db_session):
    from app.models import Match
    match_id = client.post("/matches/start").json()["id"]
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    r = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "sdlkfjsdlkfj"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Word not found in dictionary"

def test_submit_duplicate_word(client, db_session):
    from app.models import Match
    match_id = client.post("/matches/start").json()["id"]
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    r1 = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "sun"})
    assert r1.status_code == 200

    r2 = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "sun"})
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Word already submitted"

def test_timer_expired_blocks_submit(client, db_session):
    from app.models import Match
    match_id = client.post("/matches/start").json()["id"]
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    # Manually expire the timer
    link = (
        db_session.query(MatchPlayer)
        .filter(MatchPlayer.match_id == match_id, MatchPlayer.player_id == player_id)
        .first()
    )
    assert link is not None

    # Set expires_at to past
    link.expires_at = datetime.utcnow() - timedelta(seconds=1)
    db_session.commit()

    r = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "sun"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Time is up for this player"

def test_end_match_blocks_submit(client, db_session):
    from app.models import Match
    match_id = client.post("/matches/start").json()["id"]
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    end = client.post(f"/matches/{match_id}/end")
    assert end.status_code == 200

    r = client.post(f"/matches/{match_id}/submit?player_id={player_id}", json={"word": "sun"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Match is not active"

def test_leaderboard_returns_correct_score(client, db_session):
    from app.models import Match
    match_id = client.post("/matches/start").json()["id"]
    m = db_session.get(Match, match_id)
    m.letter = "S"
    db_session.commit()

    p1 = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    p2 = client.post(f"/matches/{match_id}/join", json={"name": "Bob"}).json()

    r1 = client.post(f"/matches/{match_id}/submit?player_id={p1['player_id']}", json={"word": "sun"})
    assert r1.status_code == 200

    r2 = client.post(f"/matches/{match_id}/submit?player_id={p1['player_id']}", json={"word": "sand"})
    assert r2.status_code == 200

    r3 = client.post(f"/matches/{match_id}/submit?player_id={p2['player_id']}", json={"word": "sea"})
    assert r3.status_code == 200

    lb = client.get(f"/matches/{match_id}/leaderboard")
    assert lb.status_code == 200
    data = lb.json()

    assert data["match_id"] == match_id
    leaderboard = data["leaderboard"]
    assert len(leaderboard) == 2

    assert leaderboard[0]["player_name"] == "Alice"
    assert leaderboard[0]["score"] == 2

    assert leaderboard[1]["player_name"] == "Bob"
    assert leaderboard[1]["score"] == 1


def test_ended_match_blocks_join(client, db_session):
    match_id = client.post("/matches/start").json()["id"]

    end = client.post(f"/matches/{match_id}/end")
    assert end.status_code == 200

    r = client.post(f"/matches/{match_id}/join", json={"name": "LatePlayer"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Match is not active"

def test_time_left_endpoint_returns_seconds_left(client, db_session):
    match_id = client.post("/matches/start").json()["id"]

    join = client.post(f"/matches/{match_id}/join", json={"name": "Alice"}).json()
    player_id = join["player_id"]

    r = client.get(f"/matches/{match_id}/players/{player_id}/time")
    assert r.status_code == 200
    data = r.json()

    assert data["match_id"] == match_id
    assert data["player_id"] == player_id
    assert isinstance(data["seconds_left"], int)
    assert 0 <= data["seconds_left"] <= 45