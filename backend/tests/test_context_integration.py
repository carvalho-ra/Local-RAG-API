from app.services.context import build_context


def test_build_context_with_certificate():
    chunks = [
        type(
            "Chunk",
            (),
            {
                "content": (
                    "Este certificado é concedido a Rodrigo Carvalho "
                    "por ter concluído com sucesso o Fundamentos do Python 1."
                )
            },
        )()
    ]

    context = build_context(chunks)

    # print(f"\nCONTEXTO:\n{context}")

    assert "Rodrigo Carvalho" in context
    assert "Fundamentos do Python 1" in context
