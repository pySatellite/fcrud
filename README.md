# fcrud

### RUN - Dev
```bash
$ uvicorn src.fcrud.main:app --reload
```

### RUN - Docker
```bash
$ docker build -t pysatellite/fcrud:0.2.0 .
$ docker run -dit --rm  --name fcrud020 -p 8020:80 pysatellite/fcrud:0.2.0
```