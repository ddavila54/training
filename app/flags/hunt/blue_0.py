from app.objects.c_adversary import Adversary
from app.objects.c_operation import Operation
from app.utility.base_world import BaseWorld


name = 'Hunt Test'
challenge = ''
extra_info = """"""

operation_name = 'Hunt0'


async def prerequisites_met(services):
    agents = await services.get('data_svc').locate('agents', match=dict(group='cert-nix'))
    return len(agents)


async def setup(services, op_name):
    access = dict(access=[BaseWorld.Access.RED])
    data = dict(name=op_name, group='cert-nix', adversary_id='6e19d5f9-e4d9-42b2-bc89-ea4298541d80',
                planner='sequential', atomic_enabled=1, hidden=True)
    return (await services.get('rest_svc').create_operation(access=access, data=data))[0]['id']


async def is_setup(services, op_name):
    ops = await services.get('data_svc').locate('operations', match=dict(name=op_name))
    return len(ops)


async def is_operation_successful(services, op_name):
    operation = (await services.get('data_svc').locate('operations', match=dict(name=op_name)))[0]
    if len(operation.chain) == 1 and 'host.user.name' in [f.trait for f in operation.all_facts()]:
        await services.get('rest_svc').delete_operation(data=dict(name=name))
        return True
    return False


async def verify(services):
    if await prerequisites_met(services):
        if not (await is_setup(services, operation_name)):
            await setup(services, operation_name)
        return await is_operation_successful(services, operation_name)
    return False
