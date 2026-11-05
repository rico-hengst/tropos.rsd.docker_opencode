<!-- PROJECT LOGO -->
<div align="centerv" style="margin-bottom: 1ex;padding-bottom: 1ex">
    <img src="config/docker_opencode.png" alt="Logo" height="90"><br/>
</div>
Docker sandbox for safe use of AI coding agent <em>OpenCode</em> in terminal environment

[![Opencode][Opencode-logo]][Opencode-url] [![Docker][Docker-logo]][Docker-url] [![Anaconda][Anaconda-logo]][Anaconda-url] [![GWDG][Gwdg-logo]][Gwdg-url]

## Description and target audience

This repository provides you an coding agent [OpenCode](https://opencode.ai/v2/docs/) that will run in a sandboxed [Docker](https://docker.com) container. You will be able to connect the sandbox with your software repository at your host computer via a terminal based environment.
The coding agent only has access to the content of the software repository at your host.
The sandbox is already equipped with a customizable python anaconda environment. If your software repository at the host is python based, so the python code can also be executed into the sandbox.

This repository and tutorial are intended for scientists and engineers who want to use AI coding agents to develop and improve their software code.


## 1 Requirements
* SAIA (Scalable Artificial Intelligence (AI) Accelerator) key, see [GWDG ai-services](https://docs.hpc.gwdg.de/services/ai-services/saia/index.html) (request via [API request](https://docs.hpc.gwdg.de/services/ai-services/saia/index.html#api-request))
* Access rights to build and run Docker images at your host computer

## 2 Intro: Agent coding

Agentic coding is a **software development approach** where autonomous **AI agents plan, write, test, and modify code** with minimal human intervention.  Unlike traditional coding assistants that provide passive suggestions, these agents execute complex workflows by navigating file systems, managing dependencies, and running terminal commands.

#### Focus
Key characteristics include:

* *Autonomous Execution:* Agents take high-level goals (e.g., GitHub issues) and decompose them into actionable steps, iterating until the task is complete.
* *Self-Correction:* If an agent encounters an error, it reads the output, reasons through the problem, and automatically applies fixes.
* *Human Oversight:* Developers shift from writing code line-by-line to defining goals and reviewing the final output, focusing on architecture and logic.


#### Coding agents and their operating environment

Popular coding agents as an software layer like Claude Code, OpenHands, Cursor, GitHub Copilot coding agent, OpenCode and Devin, connects LLM's to your software code.
The coding agents operates via
* Terminal
* IDE, or
* Cloud environments.

The coding agent **"Opencode" and the "terminal based operating environment"** will be the focus here.


## 3 What you'll get here: Coding agent Opencode via isolated Docker sandbox

This repository provides you an coding agent [OpenCode](https://opencode.ai/v2/docs/) that will run in a sandboxed [Docker](https://docker.com) container. You will be able to connect the sandbox with your software repository at your host computer via a terminal based environment.
The coding agent only has access to the content of the software repository at your host.
The sandbox is already equipped with a customizable python anaconda environment. If your software repository at the host is python based, so the python code can also be executed into the sandbox.

#### Description short
1. **Prepartion**: After you've successfully cloned the Opencode Sandbox repo somewhere to your host computer (e.g: ```<~/docker_opencode>```), you'll first need some configuration steps and at the end you have to build your own Docker image.
2. **Usage**: You can then run the image you created as container with a mounted directory from your host computer.
    a) You can mount any directory at your host that contains the software repository you want to work on (e.g:  ```</xyz/yourproject>```).
    b) In the simplest case, this can be the Opencode Sandbox repo you just cloned (e.g: ```<~/docker_opencode>```).

-----------

#### Preparation
**Prep 1.** Clone this repository to you host computer: e.g: ```<~/docker_opencode>```

```shell
git clone https://github.com/rico-hengst/tropos.rsd.docker_opencode <~/docker_opencode>
```
**Prep 2.** OPTIONAL: Export your python conda environment,
only necessary if your software code repository (e.g: ```</xyz/yourproject>```) is *python* based and you want *execute python code in your sandbox*.

```shell
# enter your project directory
cd </xyz/yourproject>

# export your host conda environment
conda export --file=environment.yml

# move environment to docker sandbox
mv environment.yml <~/docker_opencode/>
```
**Prep 3.** Set SAIA key as environment variable

```shell
# export key
echo 'export SAIA_API_KEY="YOUR_SAIA_KEY"' >> ~/.bashrc
# test
echo "ENV SAIA_API_KEY ${SAIA_API_KEY} created"
```
**Prep 4.** Update OpenCode config file (GWDG update the LLM models regularly. To use the latest [GWDG chat-at models](https://docs.hpc.gwdg.de/services/ai-services/chat-ai/models/index.html), you must adjust the configuration.)

```shell
# get the current used LLM models @GWDG via curl
curl -X POST \
  --url https://chat-ai.academiccloud.de/v1/models \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer <SAIA_API_KEY>' \
  --header 'Content-Type: application/json' | jq -S


# returns something like that ...
# pick the id & name of a single or multiple models you are interested in

  {
    "data": [
      {
        "created": 1782907438,
        "demand": 0,
        "id": "deepseek-v4-flash-0731",
        "input": [
          "text"
        ],
        "name": "DeepSeek V4 Flash 0731",
        "object": "model",
        "output": [
          "text",
          "thought"
        ],
        "owned_by": "chat-ai",
        "status": "ready"
      },
     ...
      {
        "created": 1785482424,
        "demand": 0,
        "id": "eurollm-22b-instruct-2512",
        "input": [
          "text"
        ],
        "name": "EuroLLM 22B Instruct 2512",
        "object": "model",
        "output": [
          "text"
        ],
        "owned_by": "chat-ai",
        "status": "ready"
      },
     ]
...
}

# update OpenCode config file (delete unused, add id & name of the models you are interested to use)
edit <~/docker_opencode/>.opencode/opencode.jsonc
```
**Prep 5.** Build Docker image (only initial execution required or if python environment will be updated)

```shell
# enter docker repository
cd <~/docker_opencode>

# build image
docker build --build-arg SAIA_API_KEY="${SAIA_API_KEY}" -t image_sbx_opencode_anaconda:latest     -f .mydocker/Dockerfile.conda     --build-arg ENV_FILE=environment.yml .
```

#### Usage


**Usage 1.** Run Docker image as container and connect to the Opencode Sandbox repository ```<~/docker_opencode>``` at your host computer and test OpenCode coding agent

```shell
# run container
docker run -it --rm     --user "$(id -u):$(id -g)"   -v <~/docker_opencode>:/workspace     -w /workspace     image_sbx_opencode_anaconda:latest     bash

# should return something like this ...
(py3.11_docker) user@142c945869d7:/workspace$

# test1
opencode run hello --print-logs
opencode debug config

# test2 Verification: You can test if it's working by running:
opencode auth list

# test3 config
OPENCODE_CONFIG=$PWD/.opencode/opencode.jsonc opencode debug config
```

**Usage 2.** Run Docker iamge as container and connect to your host software repository ```</xyz/yourproject>``` and use OpenCode via terminal

```shell
# run container
docker run -it --rm     --user "$(id -u):$(id -g)"   -v </xyz/yourproject>:/workspace     -w /workspace     image_sbx_opencode_anaconda:latest     bash

# first request - maybe the current default LLM model is not available
OPENCODE_CONFIG=$PWD/.opencode/opencode.jsonc opencode run "Tell me the current temperature!"

# focussed model, make sure that model is at your opencode config list: --model <providername>/<model_key>
OPENCODE_CONFIG=$PWD/.opencode/opencode.jsonc opencode run --model saia/deepseek-v4-flash-0731 "Please suggest code improvements, with focus on files below the directory: 'src/*.py'"
```



## Authors

* RH [![ORCID iD](https://img.shields.io/badge/-ORCID-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0000-0001-8994-5868)




## Copyright and license [![GNU V3][license-logo]][license-url]
This application is free software, licensed under GNU v3.0.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Opencode-logo]: https://img.shields.io/badge/OpenCode-000000?style=flat-square&logo=github&logoColor=white
[Opencode-url]: https://opencode.ai/v2/docs/
[Docker-logo]: https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=Docker&logoColor=white
[Docker-url]: https://docker.com
[Anaconda-logo]: https://img.shields.io/badge/-Anaconda-44A833?style=flat-square&logo=anaconda&logoColor=white
[Anaconda-url]: https://anaconda.org/
[Gwdg-logo]: https://img.shields.io/badge/GWDG%20Chat%20AI-gold
[Gwdg-url]: https://docs.hpc.gwdg.de/services/ai-services/chat-ai/index.html
[license-logo]: https://img.shields.io/badge/license-GNU/GPLv3-pink
[license-url]: https://www.gnu.org/licenses/gpl-3.0.de.html
