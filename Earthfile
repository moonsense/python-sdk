VERSION 0.6

FROM golang:1.16-alpine

cleanup:
    LOCALLY
    RUN rm -f moonsense/models/*_pb2.py*

generate:
    BUILD +cleanup
    ARG DEFINITIONS_BRANCH=main
    COPY github.com/moonsense/definitions/proto:$DEFINITIONS_BRANCH+generate-python-sdk/python /python
    SAVE ARTIFACT /python/*_pb2.py AS LOCAL moonsense/models/
