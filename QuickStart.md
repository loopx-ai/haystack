# How to test Haystack locally

## If GPU is available
```
sudo apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git

git clone git@github.com:loopx-ai/haystack.git ~/haystack
git checkout aisear
python3 -m venv --system-site-packages ~/haystack/v_haystack
source ~/haystack/v_haystack/bin/activate
pip install --upgrade pip
pip install -e '.[all-gpu]'
cd ~/haystack
pip install --no-cache-dir ./rest_api
uvicorn rest_api.application:app --host 0.0.0.0
```
## If GPU is NOT available
```
sudo apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git

git clone git@github.com:loopx-ai/haystack.git ~/haystack
git checkout aisear
python3 -m venv --system-site-packages ~/haystack/v_haystack
source ~/haystack/v_haystack/bin/activate
pip install --upgrade pip
pip install -e '.[all]'
cd ~/haystack
pip install --no-cache-dir ./rest_api
uvicorn rest_api.application:app --host 0.0.0.0
```

## Test the API
Test Rest API File Upload
```
curl -X POST 'http://localhost:8000/file-upload' \
--form 'files=@"/home/hamlin/sample.pdf"'
```

Test Rest API Query
```
curl -X POST 'http://localhost:8000/query' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What is the climate of Beijing?",
  "params": {},
  "debug": false
}
```

## Build the Docker and Push to Docker Hub
```
docker login -u loopxai
docker buildx bake base-gpu --push
docker buildx bake gpu --push
```