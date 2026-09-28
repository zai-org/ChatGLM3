import importlib.util
import sys
import types
import unittest
from pathlib import Path


def load_api():
    torch = types.ModuleType("torch")
    torch.cuda = types.SimpleNamespace(is_available=lambda: False, empty_cache=lambda: None, ipc_collect=lambda: None)
    sys.modules["torch"] = torch

    fastapi = types.ModuleType("fastapi")

    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass

        def add_middleware(self, *args, **kwargs):
            pass

        def get(self, *args, **kwargs):
            return lambda fn: fn

        def post(self, *args, **kwargs):
            return lambda fn: fn

    fastapi.FastAPI = FastAPI
    fastapi.HTTPException = Exception
    fastapi.Response = object
    middleware = types.ModuleType("fastapi.middleware")
    cors = types.ModuleType("fastapi.middleware.cors")
    cors.CORSMiddleware = object
    sys.modules["fastapi"] = fastapi
    sys.modules["fastapi.middleware"] = middleware
    sys.modules["fastapi.middleware.cors"] = cors

    loguru = types.ModuleType("loguru")
    loguru.logger = types.SimpleNamespace(debug=lambda *a, **k: None, warning=lambda *a, **k: None)
    sys.modules["loguru"] = loguru

    pydantic = types.ModuleType("pydantic")

    class BaseModel:
        pass

    def Field(*args, **kwargs):
        return None

    pydantic.BaseModel = BaseModel
    pydantic.Field = Field
    sys.modules["pydantic"] = pydantic

    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = object
    transformers.AutoModel = object
    sys.modules["transformers"] = transformers

    utils = types.ModuleType("utils")
    utils.process_response = lambda *a, **k: None
    utils.generate_chatglm3 = lambda *a, **k: None
    utils.generate_stream_chatglm3 = lambda *a, **k: None
    sys.modules["utils"] = utils

    st = types.ModuleType("sentence_transformers")
    st.SentenceTransformer = object
    sys.modules["sentence_transformers"] = st

    sse = types.ModuleType("sse_starlette")
    sse_sse = types.ModuleType("sse_starlette.sse")

    class EventSourceResponse:
        DEFAULT_PING_INTERVAL = 1000

    sse_sse.EventSourceResponse = EventSourceResponse
    sys.modules["sse_starlette"] = sse
    sys.modules["sse_starlette.sse"] = sse_sse

    sys.modules["uvicorn"] = types.ModuleType("uvicorn")

    path = Path(__file__).resolve().parent / "api_server.py"
    spec = importlib.util.spec_from_file_location("chatglm3_api_server", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EmbeddingUsageTest(unittest.TestCase):
    def test_a_string_input_is_one_text(self):
        api = load_api()
        prompt_tokens, total_tokens = api.embedding_token_usage("hello world")
        self.assertEqual(prompt_tokens, 2)
        self.assertEqual(total_tokens, 2)

        prompt_tokens, total_tokens = api.embedding_token_usage(["你好世界"])
        self.assertEqual(prompt_tokens, 5)
        self.assertEqual(total_tokens, 5)


if __name__ == "__main__":
    unittest.main()
