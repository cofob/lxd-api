FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
		curl \
		&& rm -rf /var/lib/apt/lists/*


# Copy source code
FROM scratch as source

WORKDIR /
COPY alembic.ini /alembic.ini
COPY migrations /migrations
COPY lxdapi /lxdapi


# Final image
FROM base AS final

WORKDIR /app

ENV PORT=8000 HOST=0.0.0.0 WORKERS=1 MODE=server

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm /requirements.txt
COPY .docker/entrypoint.sh .docker/healthcheck.sh /bin/
COPY --from=source / /app

HEALTHCHECK CMD /bin/healthcheck.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
