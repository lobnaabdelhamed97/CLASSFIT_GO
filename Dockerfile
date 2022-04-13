ARG GO_VERSION=1.18

FROM golang:${GO_VERSION}-alpine AS builder

RUN apk update && apk add alpine-sdk git python3-dev \
    && rm -rf /var/cache/apk/* \
     apk add libmariadb-dev libmariadbclient-dev r-base r-base-core r-base-dev && \
	 apk add --no-cache python3 py3-pip \
  && echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile \
 
RUN R -e "install.packages(c('reticulate','purrr', 'jsonlite', 'stringi', 'stringr','urltools','Dict','foreach'))" \
    python -m pip install --upgrade pip
RUN mkdir -p /api
WORKDIR /api

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .
RUN go build -o ./app ./main.go

FROM alpine:latest

RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*

RUN mkdir -p /api
WORKDIR /api
COPY --from=builder /api/app .

EXPOSE 8080
RUN pip3 install -r kernel/requirements.txt


ENTRYPOINT ["./app"]
