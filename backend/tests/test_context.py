from app.services.context import build_context


def test_build_context():
    chunks = [
        type("Chunk", (), {"content": "primeiro chunk"})(),
        type("Chunk", (), {"content": "segundo chunk"})(),
    ]

    result = build_context(chunks)

    assert result == "primeiro chunk\n\nsegundo chunk"
