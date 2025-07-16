FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt-get update -yqq && apt-get install -yqq \
    curl python3-pip python3-tqdm \
    wget \
    g++ \
    git \
    make \
    libdpkg-perl \
    sudo \
    vim \
    unzip \
    unrar \
    openssh-server \
    tmux \
    psmisc \
    xvfb \
    xclip

# download chorme
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt-get install -yqq ./google-chrome-stable_current_amd64.deb && rm google-chrome-stable_current_amd64.deb

RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip && unzip chromedriver-linux64.zip && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && chmod +x /usr/local/bin/chromedriver && rm chromedriver-linux64.zip && rm -rf chromedriver-linux64

# model environment    
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install selenium==4.26.1
RUN python -m pip install pyperclip==1.9.0
RUN python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN python -m pip install transformers[torch]==4.41.2
RUN python -m pip install datasets==2.20.0
RUN python -m pip install vllm==0.6.2
RUN python -m pip install openai==1.58.1