build:
	docker build -t pw/url-shortener:latest .

run: build
	docker run -it --rm -p 8000:8000/tcp --link dynamodb-local:localhost --net url-shortener-tech-test_default --name url-shortener pw/url-shortener:latest
