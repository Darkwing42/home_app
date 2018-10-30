# home_app

## data Verzeichnis erstellen

<pre><code> 
  mkdir data 
</code></pre>

## Environment-Variablen für Entwicklungsumgebung setzen

<pre><code>
  touch .env
  
  vim .env
  
  APP_SETTINGS=development
  FLASK_APP=
  FLASK_ENV=
  POSTGRES_USER=
  POSTGRES_PASSWORD=
  POSTGRES_DB=
  
</code></pre>



## Docker installieren

### Windows

folgt

### Linux

#### Arch Linux

<pre><code>
pacman -S docker docker-compose
</code></pre>

### MacOSX

folgt

## Start der Entwicklungsumgebung

<pre><code>
docker-compose up
</code></pre>
## Literatur

https://github.com/timlardner/Docker-FlaskCeleryRabbitRedis
