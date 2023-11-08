# fcrud

### RUN - Dev
```bash
$ uvicorn src.fcrud.main:app --reload
```

### RUN - Docker
```bash
$ docker build -t pysatellite/fcrud:0.3.0 .
$ docker run -dit --rm  --name fcrud030 -p 8020:80 pysatellite/fcrud:0.3.0
```

### Proxy DB
```bash
$ fly proxy 5432 -a fcrud-db
```

### Ref
- https://github.com/awtkns/fastapi-crudrouter
- https://fastapi-crudrouter.awtkns.com/backends/async
- https://fastapi.tiangolo.com/advanced/events
- https://fly.io/docs/postgres/connecting/connecting-internal/
- https://fly.io/docs/postgres/connecting/connecting-with-flyctl/
- [PostgreSQL 사용자 추가 및 DB/ Table 생성](https://browndwarf.tistory.com/3)
