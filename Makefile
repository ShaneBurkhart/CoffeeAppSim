NAME=macd_notifier
IMAGE_NAME=shaneburkhart/$(NAME)

all:
	docker run --rm -t -v $(PWD):/app $(IMAGE_NAME) python ./coffee/coffee.py

build:
	docker build -t $(IMAGE_NAME) .

watch:
	docker run --rm -t -v $(PWD):/app $(IMAGE_NAME) reload ./coffee/coffee.py

c:
	docker run --rm -v $(PWD):/app -it $(IMAGE_NAME) /bin/bash