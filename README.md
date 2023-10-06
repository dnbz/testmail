# Testmail project

Before running the app .env file should be created in the root directory.
The example can be seen in `.env.example`

Running via docker-compose:

```bash
docker compose up -d
```

Then the app will be available at http://localhost:8090

Or you can run it locally via pdm (pdm needs to be installed beforehand):

```bash
pdm run serve
```

Alternatively, you can run it via plain docker
```
docker build -t testmail .
docker run -p 8090:80 testmail
```