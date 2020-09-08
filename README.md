# ThemeToggler
Toggle mode (themes) for multiple applications at the same time, quickly switching between light and dark mode.

## Config
Create a new `ApplicationTheme` object for each app you want to register a theme for and add to the `themes` list.
Currently the theme paths are hardcoded so you'll have to at least change the paths for the present apps (VS Code and Windows Terminal).
* Todo: Implement configs with `.env` file.


## Usage
Navigate into the project directory and run the `main.py` file as a module.
* Todo: Create `setup.py` to run without specifying `python`.

### Windows
```
cd theme-toggler
python -m main
```
> Python installed via Microsoft Store doesn't have access to edit the Windows Registry. You need to download Python from [python.org](https://python.org) (and add it to `PATH`) if you want to also toggle system mode.
### Linux/MacOS
```
cd theme-toggler
python3 -m main
```
> Currently you cannot toggle system mode for other platforms than Windows.



# Requirements
* Python 3 (tested on 3.8)
