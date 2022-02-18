docker run --rm -d --ulimit='stack=-1:-1' \
    --name klee \
    klee/klee sleep infinity
docker cp . klee:/home/klee
docker exec -ti klee bash