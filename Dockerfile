# Canonical environment for the DTA (bivariate SROC) validation:
# R 4.6.0 (rocker, built from source at that version) + mada/mvmeta/ellipse from the
# 2026-10-01 Posit Package Manager snapshot + Node 24.15.0 + pinned Python packages.
#   docker build -t dta-sroc-reproducible .
#   docker run --rm -v "$PWD/outputs:/work/outputs" dta-sroc-reproducible           # full run (default)
#   docker run --rm dta-sroc-reproducible --quick
FROM node:24.15.0-bookworm-slim AS node
FROM rocker/r-ver:4.6.0
COPY --from=node /usr/local/bin/node /usr/local/bin/node
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 MPLBACKEND=Agg \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY bench/install_r_packages.R bench/install_r_packages.R
RUN Rscript bench/install_r_packages.R
COPY requirements.txt .
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
ENTRYPOINT ["python", "reproduce.py"]
