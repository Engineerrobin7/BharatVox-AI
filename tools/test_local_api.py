import importlib.util
import pathlib
from fastapi.testclient import TestClient

# Load api/index.py as a module regardless of package init
spec = importlib.util.spec_from_file_location(
	"api_index",
	str(pathlib.Path(__file__).parent.parent / "api" / "index.py")
)
api_index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_index)

client = TestClient(api_index.app)

resp = client.post("/api", json={"language":"english","audio_format":"mp3","audio_base64":"dGVzdA=="})
print(resp.status_code)
print(resp.json())
