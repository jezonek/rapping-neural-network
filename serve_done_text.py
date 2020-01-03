from rhyme_finding import prepare_connection_to_db_texts


def serve_done_text():
    collection = prepare_connection_to_db_texts()
    record = collection.find_one_and_delete({})
    if record:
        text = record["text"]
        return text
    else:
        return None
