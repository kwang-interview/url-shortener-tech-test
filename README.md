# URL Shortener Service

This service handles shortening and lengthening of URL strings

## Prerequisites

- [PyCharm Community Edition 2023.2.5+](https://www.jetbrains.com/pycharm/download/other.html)
- [Docker Desktop 4.26.0+](https://www.docker.com/products/docker-desktop/)
- [GNU make](https://gnuwin32.sourceforge.net/packages/make.htm)

## Getting Started

1. Clone project with `git clone https://github.com/kwang-interview/url-shortener-tech-test.git`
2. Setup data stores using `docker-compose pull` then`docker-compose up -d`
3. Start the server using `make run`

### Useful Links

* [Local SwaggerUI](http://localhost:8080/docs)

### Notes

* Service functionality is implemented with the assumption that:
    * Shortened link never expire
    * Already existing link stored in db is returned instead of creating a new link
    * Shortened link should typically be shorter than the input URL unless the input is already a short string