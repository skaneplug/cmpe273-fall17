# Instruction 

### Build App Command
```
docker build -t flaskapp .
docker run -p 8000:80 flaskapp

```

### Curl Command
```buildoutcfg
curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@tmp_f/foo.py" http://localhost:8000/api/v1/scripts


curl -i http://localhost:8000/api/v1/scripts/1
```
