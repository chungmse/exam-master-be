import jwt

decoded_token = jwt.decode(
    authorization, "DQ;/_mU9<}La6%wJhF48:(Tg~#bK,BSy", algorithms=["HS256"]
)
