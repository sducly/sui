FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3-pip \
    curl \
    libgtk-3-dev \
    webkit2gtk-4.0-dev \
    build-essential \
    python3.12-dev \
    pkg-config \
    unzip \
    ffmpeg \
    libsndfile1 \
    g++ \
    libstdc++6 \
    espeak \
    git \
    libsm6 \
    wget \
    festival \
    espeak-ng \
    mbrola \
    mbrola-fr2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN curl -fsSL https://ollama.ai/install.sh | sh

CMD ["ollama", "serve"]