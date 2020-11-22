# kiyobot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![CodeFactor](https://www.codefactor.io/repository/github/medjedqt/kiyobot/badge?s=8e2c7f35c70e48525e1872c07dda7b97b200b9da)](https://www.codefactor.io/repository/github/medjedqt/kiyobot)

## Getting Started

To get a local copy up and running follow these simple example steps.

---

### NOTE

It is highly recommended to instead use the template bot in the [template branch](https://github.com/medjedqt/kiyobot/tree/template)

---

### Prerequisites

* [Python 3](python.org)
* [Discord bot token](https://discordapp.com/developers/applications)
* [Danbooru account and API key](https://danbooru.donmai.us/profile)
* [Youtube API key](https://cloud.google.com/)

### Installation

1. Clone the repo

    ```sh
    git clone https://github.com/medjedqt/kiyobot.git
    ```

2. Install pip modules

    ```sh
    pip install -r requirements.txt
    ```

3. Enter your bot token and danbooru key in `obot.py`

    ```py
    token = 'ENTER YOUR TOKEN'
    dbkey = 'YOUR DANBOORU KEY'
    dbname = 'YOUR DANBOORU USERNAME'
    ytclient = ytapi(api_key='YOUR YOUTUBE API KEY')
    ```
