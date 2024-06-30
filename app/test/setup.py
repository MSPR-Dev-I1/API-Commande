def setup_mock_auth(mocker):
    """
        Setup the mock of the validation of the token by the Auth API
    """
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"validation": True}
    return mock_post
