#!/bin/bash

echo "容器名称                          容器ID      GPU显存使用"
echo "================================================================"

nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits | while IFS=',' read -r pid mem; do
    pid=$(echo $pid | xargs)
    mem=$(echo $mem | xargs)
    
    container_id=$(docker ps -q | xargs -I {} sh -c "docker top {} -eo pid,args 2>/dev/null | grep -w $pid && echo {}" | tail -1)
    
    if [ -n "$container_id" ]; then
        container_name=$(docker inspect --format='{{.Name}}' $container_id 2>/dev/null | sed 's/\///')
        container_short_id=$(echo $container_id | cut -c1-12)
        printf "%-32s %-12s %6s MiB\n" "$container_name" "$container_short_id" "$mem"
    fi
done | sort -u
