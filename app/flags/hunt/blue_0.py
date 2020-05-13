from app.objects.c_adversary import Adversary
from app.objects.c_operation import Operation
from app.utility.base_world import BaseWorld


name = 'Hunt Test'
challenge = ''
extra_info = """"""


async def setup(services):
    access = dict(access=[BaseWorld.Access.RED])
    data = dict(name='Hunt0', group='cert-nix', adversary_id='6e19d5f9-e4d9-42b2-bc89-ea4298541d80', atomic_enabled=1,
                auto_close=1, hidden=True)
    return (await services.get('rest_svc').create_operation(access=access, data=data))[0]['id']


async def verify(services, operation_id):
    operation = (await services.get('data_svc').locate('operations', match=dict(id=operation_id)))[0]
    return operation.finish and len(operation.chain) == 1 and \
        'host.user.name' in [f.trait for f in operation.all_facts()]
