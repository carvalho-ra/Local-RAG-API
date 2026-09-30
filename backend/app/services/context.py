
def build_context(chunks):
    seen = set()
    unique_chunks = []

    for chunk in chunks:
        if chunk.content not in seen:
            seen.add(chunk.content)
            unique_chunks.append(chunk)

    return "\n\n".join(chunk.content for chunk in unique_chunks)