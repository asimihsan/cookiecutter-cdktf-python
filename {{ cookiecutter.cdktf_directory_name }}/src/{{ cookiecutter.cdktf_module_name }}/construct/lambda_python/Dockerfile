FROM public.ecr.aws/lambda/python:3.12

RUN --mount=type=cache,target=/root/.cache/pip \
    dnf update -y && \
    dnf clean all && \
    pip install poetry && \
    poetry config virtualenvs.create false

# Copy project files
COPY --link . ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    poetry install --no-interaction --no-ansi

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
