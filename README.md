# Dasboard monitoring datasets in 4TU.ResearchData

Welcome to the workshop **Building a minimal dashboard to monitor datasets using 4TU.ResearchData API**! for data support staff from University of Twente, on March 17th, 2026.  



## 🚀 Workshop Overview

### What we will build

By the end of the workshop, you will be able to:

- Apply the API data flow: request → JSON → DataFrame → Streamlit UI

- Add different filters 
- Deploy the application in a webserver 


We will live-code everything in a single script.



## 🛠 Workshop Setup

Before the workshop, please:

### 1. Check your Python installation

Make sure you have **Python 3.10 or newer** installed.

Open a Unix terminal
(**Git Bash on Windows, Terminal on macOS or Linux**) and run:

```bash
python --version
```

or

```bash
python3 --version
```



### 2. Create a project folder

Create a new folder for the workshop project and move into it:

```bash
mkdir api-dashboard-workshop
cd api-dashboard-workshop
```



### 3. Create and activate a virtual environment

Inside the project folder, create a virtual environment:

```bash
python3 -m venv api-dashboard-env
```

Activate the environment:

#### macOS / Linux

```bash
source api-dashboard-env/bin/activate
```

#### Windows (Git Bash)

```bash
source api-dashboard-env/Scripts/activate
```

After activation, your terminal should display something like:

```
(api-dashboard-env)
```


### 4. Install the required libraries

#### 4.1 Create a requirements file

```bash
touch requirements.txt
```

#### 4.2 Add the following libraries to the file

Open the file with any text editor and paste:

```
requests>=2.31
pandas>=2.0
streamlit>=1.30
python-dotenv>=1.0
pytest>=8.0
ruff>=0.4
python-dateutil>=2.8
```

### 4.3 Install the libraries

Run:

```bash
pip install -r requirements.txt
```



### 5. Verify that Streamlit works

Test that Streamlit was installed correctly:

```bash
streamlit hello
```

This should open a **demo Streamlit application in your browser**.

### 6. Install Git (if needed)

The deployment step of the workshop will require **Git** and a **GitHub account**.

Check whether Git is installed:

```bash
git --version
```

If Git is not installed, download it from:

[https://git-scm.com/](https://git-scm.com/)



## 🛠 Prerequisites

Before attending the workshop, please ensure you have:

### Required Knowledge

This is not a beginner Python workshop. You should be comfortable with:

- Basic Python syntax (functions, dictionaries, loops)

- Running Python from the command line

- Installing packages with pip

- Basic familiarity with pandas

- Basic understanding of HTTP concepts (GET requests, JSON)

If you have never used requests or streamlit before, that is fine, we will cover those from scratch.


### Required Software

Please ensure the following are installed:

✅ Python : Python 3.10 or newer

Verify with: `python --version` 


✅ Git 

Verify with: `git --version`

✅ Code Editor

Recommended:

- VS Code

-Any editor where you can run a terminal

## 📖 Workshop Materials

- Laptop with charger

- Admin rights to install packages (if needed)

- Stable internet connection

## 🔗 Resources

- 4TU.ResearchData API documentation: https://djehuty.4tu.nl/

## 💡 License
This workshop material is licensed under **GNU AFFERO GENERAL PUBLIC LICENSE Version 3**. Feel free to share and modify the lesson according your needs.

## 🙌 Acknowledgments


---


Happy coding! 🎉
