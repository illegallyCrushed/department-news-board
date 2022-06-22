SERVICES := gateway file news user

build-base:
	docker build -t news-board-base .

build: build-base
	for service in $(SERVICES); do make -C ./services/$$service build-image; done