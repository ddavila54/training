from app.objects.c_adversary import Adversary
from app.objects.c_operation import Operation
from app.utility.base_world import BaseWorld


name = 'Hunt Test'
challenge = ''
extra_info = """"""


async def setup(services):
    adversary = create_adversary()
    operation = await create_operation(services, adversary)
    services.get('rest_svc').loop.create_task(operation.run(services))
    return operation


def create_adversary():
    adversary_id = '6e19d5f9-e4d9-42b2-bc89-ea4298541d80'
    atomic_ordering = ['c0da588f-79f0-4263-8998-7496b1a40596']
    return Adversary(adversary_id=adversary_id, name='Training Hunt Adversary',
                     description='Training Hunt Adversary', atomic_ordering=atomic_ordering)


async def create_operation(services, adversary):
    group = 'cert'
    planner = await services.get('data_svc').locate('planners', match=dict(name='sequential'))
    agents = await services.get('data_svc').locate('agents', match=dict(group='cert'))
    sources = await services.get('data_svc').locate('sources', match=dict(name='basic'))
    access = BaseWorld.Access.APP
    return Operation(name=name, planner=planner[0], agents=agents, adversary=adversary, group=group, jitter='2/8',
                     source=next(iter(sources), None), state='running', autonomous=1, access=access, atomic=1,
                     obfuscator='plain-text', auto_close=1, visibility='50')


async def verify(services, operation):
    return operation.finish and len(operation.links) == 1 and \
           'host.user.name' in [f.trait for f in operation.all_facts()]
