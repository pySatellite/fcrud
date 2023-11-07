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

### Ref
- https://github.com/awtkns/fastapi-crudrouter
- https://fastapi-crudrouter.awtkns.com/backends/async
- https://fastapi.tiangolo.com/advanced/events