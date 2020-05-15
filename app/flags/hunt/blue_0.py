from app.objects.c_adversary import Adversary
from app.objects.c_operation import Operation
from app.utility.base_world import BaseWorld


name = 'Hunt Test'
challenge = ''
extra_info = """"""

operation_name = 'Hunt0'
adversary_id = '6e19d5f9-e4d9-42b2-bc89-ea4298541d80'
agent_group = 'cert-nix'


async def does_agent_exist(services, group):
    return len(await services.get('data_svc').locate('agents', match=dict(group=group)))


async def is_operation_started(services, op_name):
    return len(await services.get('data_svc').locate('operations', match=dict(name=op_name)))


async def start_operation(services, op_name, group, adv_id):
    access = dict(access=[BaseWorld.Access.RED])
    data = dict(name=op_name, group=group, adversary_id=adv_id,
                planner='', atomic_enabled=1, hidden=True)
    await services.get('rest_svc').create_operation(access=access, data=data)


async def is_operation_successful(services, op_name):
    operation = (await services.get('data_svc').locate('operations', match=dict(name=op_name)))[0]
    if len(operation.chain) == 1 and 'host.user.name' in [f.trait for f in operation.all_facts()]:
        return True
    return False


async def cleanup_operation(services, op_name):
    await services.get('rest_svc').delete_operation(data=dict(name=op_name))


async def verify(services):
    if await does_agent_exist(services, agent_group):
        if not (await is_operation_started(services, operation_name)):
            await start_operation(services, operation_name, agent_group, adversary_id)
        if await is_operation_successful(services, operation_name):
            await cleanup_operation(services, operation_name)
            return True
    return False
