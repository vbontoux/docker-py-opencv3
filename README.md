# docker-py-opencv3
## Usage:
```
docker build -t docker-py-opencv3 /path/to/docker-py-opencv3/
docker run -v $(pwd):/app -it docker-py-opencv3 /bin/bash
/app# python feature-matching-sift.py -r ref.png -i photo.png
```
## References:
The Dockerfile has been build with the help of [Adrian Rosebrock](http://www.pyimagesearch.com/author/adrian/)'s blog post on [pyimagesearch](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
