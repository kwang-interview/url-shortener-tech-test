build:
	docker build -t pw/url-shortener:latest .

run: build
	docker run -it --rm -p 8080:8080/tcp --link dynamodb-local:localhost --net url-shortener-tech-test_default --name url-shortener pw/url-shortener:latest
