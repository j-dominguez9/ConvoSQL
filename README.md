# ConvoSQL

*This program was created as a project for Cloud Computing course in the Southern Methodist University MSDS program.*

*For a demo of this application, see https://sql.ninabobina.me*

### What does this program do?

ConvoSQL takes a request in natural language, which is translated to SQL code via GPT-3.5-turbo API, and finally submits code to the relevant databases to return output. The objective is to have the functionality available to SQL queries without needing to know SQL.

### Requirements
* Upon installation, the program will request your OpenAI Organization and API keys to connect to the GPT-3.5.turbo model.
* Podman

### Installation
All that is needed to run the program is to clone this repository and run the 'install_ConvoSQL.sh' file (make sure it is executable). All the image/container/pod set up is handled by the install script. The default installation will serve a Streamlit interface that can be accessed via localhost:80 (The port can be changed by modifying the install script).

### How it is intended to be used
The default files and code in this repository serves a demo application connected to two mysql containers with toy databases. The objective of this program is to be used locally by people and organizations to query their own databases. In order to do so, one simply needs to switch out the contents of the database containers and folders. *Make sure to modify the relevant Dockerfile code when doing so.*


