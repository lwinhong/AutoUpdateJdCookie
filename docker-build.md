编译
```bash
docker build -t kk/autojd:latest .
```

运行

```bash
docker run --name=kkautojd --restart=always -p 4567:4567 kk/autojd:latest 


```

单次运行

```bash
docker run --name=kkautojd  kk/autojd:latest python main.py

```