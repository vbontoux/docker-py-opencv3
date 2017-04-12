# docker-py-opencv3
## Usage:
```
docker build -t docker-py-opencv3 /path/to/docker-py-opencv3/
docker run -v $(pwd):/app -it docker-py-opencv3 /bin/bash
/app# python feature-matching-sift.py -r ref.png -i photo.png
```
