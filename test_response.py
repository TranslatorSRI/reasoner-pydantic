from reasoner_pydantic.message import Response


def test_scratch():

    response_asdf = Response.parse_file("./asdf.pretty.json")
    response_zxcv = Response.parse_file("./zxcv.pretty.json")

    message_asdf = response_asdf.message
    message_asdf.update(response_zxcv.message)

    assert len(message_asdf.results) > 2
