def extract_msg_body(message):
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()

            if ctype == 'text/plain':
                body = part.get_payload(decode=True).decode()
                return (f"Body: {body[:200]}...") # Print first 200 chars of body
                break
    else:
        body = message.get_payload(decode=True).decode()
        return (f"Body: {body[:200]}...") 