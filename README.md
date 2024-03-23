# Deploy Telegram Bot on Google Cloud Platform
- Consider to follow me on [Github](https://github.com/BrianMohamadSafiudin) and [LinkedIn](https://www.linkedin.com/in/brianmohamadsafiudin), Terima Kasih 😊.
- The code is uploaded https://github.com/BrianMohamadSafiudin/piton/.

## Pre-requisite
- You have committed the code to Github (optional but makes life much easier later on).
- You have your Telegram Bot running successfully on your personal device.

## Steps :
1. Go to https://console.cloud.google.com/projectcreate and create a new project.
2. Enable billing to avail the free tier — https://console.cloud.google.com/billing/.
3. Go to https://console.cloud.google.com/compute and create an instance with ubuntu lts image.
4. Go to instance and click on SSH.
5. Post SSH , install the required python dependencies.

- `sudo apt update`
- `sudo apt-get -y install python-dev build-essential`
- `sudo apt -y install python3-pip`
- `python3 -m pip install -U pip`
- `export PATH="$HOME/.local/bin:$PATH"`
- `pip3 install --upgrade setuptools`

6. Clone the repository and install the requirements.txt dependencies.

- `git clone https://github.com/BrianMohamadSafiudin/piton/ (your repository)`
- `cd piton (your path)`
- `sudo apt install python3-pip`
- `pip3 install -r requirements.txt`

6. Update the config.py (optional if any).
7. Run the Telegram Bot.

- `python3 main.py`
- `nohup python3 main.py &` (optional)