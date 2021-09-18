# Pinnacle 2021
Team HackDuke (PMOI) project for Pinnacle 2021.

### Team Members
Albert Lua, Sai Coumar, Jason Leong, Daniel Trager

## Initial Setup
First, the Execution Policy for PowerShell needs to be changed. The following command needs to be run in PowerShell (admin).

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

Verification can be done with the following, ensure "RemoteSigned" is returned.

```
Get-ExecutionPolicy
```

Now the virtual environment needs to be setup (we will be using "pinnacle" as the name).

```
python -m venv pinnacle
```

Virtual environment needs to be activated. For PowerShell, remove the .bat extension.

```
pinnacle\Scripts\activate.bat
```

Verify `(pinnacle)` is present in the beginning of the line for terminal. Now in the virtual environment, install the requirements via pip.

```
pip install -r requirements.txt
```

Now we can run the Flask application.

```
python app.py
```

Application should now be running and accessible via localhost. Default is `127.0.0.1:5000`