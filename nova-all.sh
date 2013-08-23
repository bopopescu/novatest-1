python /opt/stack/novatest/setup.py install
supervisorctl restart nova-api
supervisorctl restart nova-compute
supervisorctl restart nova-network
supervisorctl restart nova-conductor
supervisorctl restart nova-cert
supervisorctl restart nova-scheduler

