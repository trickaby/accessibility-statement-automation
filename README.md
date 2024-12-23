# accessibility-statements-automation

### Project overview
This project automates the process of verifying content in accessibility statements.

### Steps for installing chromedriver on MacBook
Prerequisites:
- Install latest version of Home brew on MacBook

1. Install ChromeDriver
-Open the Terminal application on your Mac.
-Run the following command to install ChromeDriver via Homebrew:
brew install chromedriver
-Wait for the installation to complete. Homebrew will download and set up the latest version of ChromeDriver.
2. Verify Installation
-To ensure ChromeDriver was installed correctly, run:
chromedriver --version
-This will display the installed version of ChromeDriver.
3. Upgrade ChromeDriver
-To upgrade ChromeDriver to the latest version, use the following command:
brew upgrade chromedriver
-This will download and install the latest version if one is available.
4. Keep ChromeDriver Up to Date
-To update Homebrew itself and all installed packages (including ChromeDriver), run:
brew update
brew upgrade

### Steps for running the app

Prerequisites:
- Python 3.12 installed
- pip (should be installed with python by default. <code>pip --version</code> to check)
- Chromedriver installed

1. Open command line and navigate to accessibility-statement-automation
2. Create virtual environment: <code>python -m venv venv</code>
3. Activate the virtual environment:
    - Windows: <code>venv\Scripts\activate</code>
    - Mac/Linux: <code>source venv/bin/activate</code>
4. Install dependencies: <code>pip install -r requirements.txt</code>
5. ### Run: <code>python app.py</code> 