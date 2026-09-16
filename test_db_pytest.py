import db

def test_save_then_load(tmp_path):
    db.DB_PATH = str(tmp_path / "t.db")
    db.init_db()

    db.save_message("A", "user", "我是汉堡王三世")
    db.save_message("A", "user", "我是谁")

    msgs = db.load_messages("A")
    assert len(msgs) == 2, f"期望2条，实际{len(msgs)}条"
    assert msgs[0]["role"] == "user"
    assert "汉堡王三世" in msgs[0]["content"]

def test_two_session(tmp_path):
    db.DB_PATH = str(tmp_path / "t.db")
    db.init_db()

    db.save_message("A", "user", "不羡鸳鸯不羡仙")
    db.save_message("B", "user", "爱你一万年")
    db.save_message("B", "user", "爱一个人需要理由吗")
    msgs1 = db.load_messages("A")
    msgs2 = db.load_messages("B")

    assert len(msgs1) == 1
    assert len(msgs2) == 2

def test_clear(tmp_path):
    db.DB_PATH = str(tmp_path / "t.db")
    db.init_db()

    db.save_message("A", "user", "我是汉堡王三世")
    db.save_message("A", "user", "我是谁")

    db.clear_messages("A")
    assert db.load_messages("A") == []

