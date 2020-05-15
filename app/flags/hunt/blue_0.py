from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Test'
challenge = ''
extra_info = """"""


operation_name = 'Hunt0'
adversary_id = '6e19d5f9-e4d9-42b2-bc89-ea4298541d80'
agent_group = 'cert-nix'


async def verify(services):
    if await BaseFlag.does_agent_exist(services, agent_group):
        if not (await BaseFlag.is_operation_started(services, operation_name)):
            await BaseFlag.start_operation(services, operation_name, agent_group, adversary_id)
        if await BaseFlag.is_operation_successful(services, operation_name):
            await BaseFlag.cleanup_operation(services, operation_name)
            return True
    return False
