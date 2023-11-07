# audio-annonation
Django app that allows you to annotate audio.


# Usage:

- Clone repository: 

```bash
        git clone https://github.com/unna97/audio-annonation.git
        cd audio-annonation
```
- Change the name and prefix in environment.yml file to your desired environment name and folder to save it in.
- Create virtual environment with iven environment.yml file:
    
```bash
    conda env create -f environment.yml
```
- Activate virtual environment:

```bash
    conda activate <environment_name>
```

- Add folder with audio files to static/media/audio
- Run server: 

```bash
    python manage.py runserver
```