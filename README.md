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

### Ref
- https://github.com/awtkns/fastapi-crudrouter
- https://fastapi-crudrouter.awtkns.com/backends/async
- https://fastapi.tiangolo.com/advanced/events
- https://fly.io/docs/postgres/connecting/connecting-internal/
- https://fly.io/docs/postgres/connecting/connecting-with-flyctl/
- [PostgreSQL 사용자 추가 및 DB/ Table 생성](https://browndwarf.tistory.com/3)

```bash
$ fly volumes create mysqldata --size 1

                  ID: vol_545j93k0powmo6jv
                Name: mysqldata
                 App: mmsql-internal
              Region: nrt
                Zone: e883
             Size GB: 1
           Encrypted: true
          Created at: 07 Nov 23 04:58 UTC
  Snapshot retention: 5
```