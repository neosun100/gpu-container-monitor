#!/usr/bin/env python3
import subprocess
import json
import re
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def get_gpu_info():
    """获取所有 GPU 的详细信息"""
    try:
        result = subprocess.run([
            'nvidia-smi', 
            '--query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,power.limit',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, check=True)
        
        gpus = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = [x.strip() for x in line.split(',')]
            gpus.append({
                'index': int(parts[0]),
                'name': parts[1],
                'temperature': int(parts[2]) if parts[2] != '[N/A]' else 0,
                'utilization': int(parts[3]) if parts[3] != '[N/A]' else 0,
                'memory_utilization': int(parts[4]) if parts[4] != '[N/A]' else 0,
                'memory_used': int(parts[5]) if parts[5] != '[N/A]' else 0,
                'memory_total': int(parts[6]) if parts[6] != '[N/A]' else 0,
                'power_draw': float(parts[7]) if parts[7] != '[N/A]' else 0,
                'power_limit': float(parts[8]) if parts[8] != '[N/A]' else 0
            })
        return gpus
    except Exception as e:
        return []

def get_gpu_processes():
    """获取 GPU 进程信息，包括 GPU 索引"""
    try:
        result = subprocess.run([
            'nvidia-smi',
            '--query-compute-apps=pid,used_memory,gpu_uuid',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, check=True)
        
        # 获取 GPU UUID 到索引的映射
        uuid_result = subprocess.run([
            'nvidia-smi',
            '--query-gpu=index,gpu_uuid',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, check=True)
        
        uuid_to_index = {}
        for line in uuid_result.stdout.strip().split('\n'):
            if line:
                idx, uuid = [x.strip() for x in line.split(',')]
                uuid_to_index[uuid] = int(idx)
        
        processes = {}
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = [x.strip() for x in line.split(',')]
            pid = parts[0]
            mem = int(parts[1])
            gpu_uuid = parts[2]
            gpu_index = uuid_to_index.get(gpu_uuid, 0)
            
            if pid not in processes:
                processes[pid] = {'memory': 0, 'gpus': []}
            processes[pid]['memory'] += mem
            if gpu_index not in processes[pid]['gpus']:
                processes[pid]['gpus'].append(gpu_index)
        
        return processes
    except Exception as e:
        return {}

def get_container_gpu_devices(container_id):
    """获取容器配置的 GPU 设备"""
    try:
        # 检查容器的 GPU 设备配置
        result = subprocess.run([
            'docker', 'inspect', container_id,
            '--format', '{{json .HostConfig.DeviceRequests}}'
        ], capture_output=True, text=True)
        
        gpu_indices = []
        
        if result.stdout.strip() and result.stdout.strip() != 'null':
            device_requests = json.loads(result.stdout.strip())
            for req in device_requests:
                # 检查是否为 GPU 请求：
                # 1. Driver 为 "nvidia" 或空字符串
                # 2. Capabilities 包含 "gpu"
                capabilities = req.get('Capabilities', [])
                has_gpu_capability = any('gpu' in cap if isinstance(cap, list) else cap == 'gpu' 
                                        for cap in capabilities)
                
                driver = req.get('Driver', '')
                is_nvidia_driver = driver == 'nvidia' or driver == ''
                
                if is_nvidia_driver and has_gpu_capability:
                    # 检查 DeviceIDs
                    device_ids = req.get('DeviceIDs') or []
                    for dev_id in device_ids:
                        try:
                            gpu_indices.append(int(dev_id))
                        except:
                            pass
                if is_nvidia_driver and has_gpu_capability:
                    # 检查 DeviceIDs
                    device_ids = req.get('DeviceIDs') or []
                    for dev_id in device_ids:
                        try:
                            gpu_indices.append(int(dev_id))
                        except:
                            pass
                    
                    # 如果 DeviceIDs 为空但 Count > 0，说明请求了 GPU 但没指定具体设备
                    if not device_ids and req.get('Count', 0) > 0:
                        gpu_info = get_gpu_info()
                        # 添加所有可用 GPU
                        gpu_indices.extend([g['index'] for g in gpu_info])
        
        # 如果还是没找到，尝试检查环境变量
        if not gpu_indices:
            result = subprocess.run([
                'docker', 'inspect', container_id,
                '--format', '{{range .Config.Env}}{{println .}}{{end}}'
            ], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if 'NVIDIA_VISIBLE_DEVICES' in line:
                    match = re.search(r'NVIDIA_VISIBLE_DEVICES=(.+)', line)
                    if match:
                        devices = match.group(1).strip()
                        if devices and devices != 'void':
                            if devices == 'all':
                                gpu_info = get_gpu_info()
                                gpu_indices = [g['index'] for g in gpu_info]
                            else:
                                for dev in devices.split(','):
                                    try:
                                        gpu_indices.append(int(dev.strip()))
                                    except:
                                        pass
        
        # 去重并排序
        return sorted(list(set(gpu_indices)))
    except Exception as e:
        return []

def get_gpu_containers():
    """获取所有配置了 GPU 的容器"""
    try:
        gpu_processes = get_gpu_processes()
        
        # 获取所有容器（包括停止的）
        docker_ps = subprocess.run([
            'docker', 'ps', '-a', 
            '--format', '{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}'
        ], capture_output=True, text=True)
        
        containers = []
        for line in docker_ps.stdout.strip().split('\n'):
            if not line:
                continue
            cid, name, status, image = line.split('|')
            
            # 获取容器配置的 GPU 设备
            configured_gpus = get_container_gpu_devices(cid)
            
            # 如果容器没有配置 GPU，跳过
            if not configured_gpus:
                continue
            
            # 获取实际 GPU 显存使用（仅对运行中的容器）
            gpu_mem = 0
            actual_gpus = set()
            
            if 'Up' in status and 'Paused' not in status:
                top_result = subprocess.run([
                    'docker', 'top', cid, '-eo', 'pid,args'
                ], capture_output=True, text=True)
                
                for pid, proc_info in gpu_processes.items():
                    if pid in top_result.stdout:
                        gpu_mem += proc_info['memory']
                        actual_gpus.update(proc_info['gpus'])
            
            # 使用实际 GPU（如果有），否则使用配置的 GPU
            display_gpus = sorted(list(actual_gpus)) if actual_gpus else configured_gpus
            
            containers.append({
                'name': name,
                'id': cid[:12],
                'full_id': cid,
                'memory': gpu_mem,
                'status': status,
                'image': image.split(':')[0][-30:],
                'gpus': display_gpus,
                'configured_gpus': configured_gpus
            })
        
        containers.sort(key=lambda x: x['name'])
        return containers
    except Exception as e:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """返回完整的系统状态"""
    return jsonify({
        'gpus': get_gpu_info(),
        'containers': get_gpu_containers()
    })

@app.route('/api/container/<action>/<container_id>', methods=['POST'])
def container_action(action, container_id):
    try:
        if action == 'pause':
            subprocess.run(['docker', 'pause', container_id], check=True)
        elif action == 'unpause':
            subprocess.run(['docker', 'unpause', container_id], check=True)
        elif action == 'restart':
            subprocess.run(['docker', 'restart', container_id], check=True)
        elif action == 'stop':
            subprocess.run(['docker', 'stop', container_id], check=True)
        elif action == 'start':
            subprocess.run(['docker', 'start', container_id], check=True)
        else:
            return jsonify({'success': False, 'error': 'Invalid action'})
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
