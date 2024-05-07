# NEMO Aggregation

This is an automation project written by [Nathan Ho](https://github.com/ptrichr) for Terrapin Works. The purpose of this application is to aggregate and display data from the [NIST NEMO API](https://github.com/usnistgov/NEMO) about lab usage for Terrapin Works lab spaces (specifically the IFL, RPC, and RPL).

# Setup

Assuming you have Python (preferably >=3.11, the version this was written in), follow these steps to get setup for aggregation:

## Virtual environment

> [!NOTE]
> I recommend using a virtual environment, but this step is completely optional.

Setup the virtual environment:
> ```console
> # python3.11 -m venv venv
> ```

Activate the virtual environment:
> Windows:
> ```console
> # ./venv/Scripts/activate
> ```
> Linux:
> ```console
> # source ./venv/bin/activate
> ```
> MacOS:
> idk tbh google lol

## Dependencies

>  ```console
>  # pip3 install -r requirements.txt
>   ```

## Authentication

If you already have a token:
> ```console
> # touch .env
> # echo "export NEMO_token = \"<your token here>\"" >> .env
> ```

If you don't have a token, you will have to be granted administrator access to get one.
