def detect_emotion(text):

    text = text.lower()

    # Warning (18+ or very long question)
    if any(word in text for word in [
        "cannot answer inappropriate",
        "please ask one short question"
    ]):
        return "warning"

    # Happy
    elif any(word in text for word in [
        "hello",
        "hi",
        "welcome",
        "great",
        "good",
        "happy",
        "thanks"
    ]):
        return "happy"

    # Sad
    elif any(word in text for word in [
        "sorry",
        "cannot",
        "don't know",
        "unable",
        "failed"
    ]):
        return "sad"

    # Thinking
    elif any(word in text for word in [
        "search",
        "checking",
        "current",
        "latest",
        "thinking"
    ]):
        return "thinking"

    # Default
    return "speaking"