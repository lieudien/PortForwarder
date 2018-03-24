

SSH = 22
HTTP = 80
SCALABLE = 7000
LOCAL_SERVICE_PORTS = {SSH: 2200,
                       HTTP: 8000,
                       SCALABLE: 7000,
                      }
PORT_HOSTS = {SSH: '192.168.0.02',
              HTTP: '192.168.0.03',
              SCALABLE: '192.168.0.4',
              }

WORKER_THREADS = 4
