FROM golang:1.21 as build

WORKDIR /app

# Copy dependencies list
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go mod download

# Build with optional lambda.norpc tag
COPY main.go .
RUN go build -tags lambda.norpc -ldflags="-s -w" -o main main.go

# Copy artifacts to a clean image
FROM public.ecr.aws/lambda/provided:al2023
COPY --from=build /app/main ./main
ENTRYPOINT [ "./main" ]
