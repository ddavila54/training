from app.utility.base_world import BaseWorld


class BaseFlag:
    """
    A collection of static functions to be used by training flags.
    """

    @staticmethod
    async def does_agent_exist(services, group):
        return len(await services.get('data_svc').locate('agents', match=dict(group=group)))

    @staticmethod
    async def is_operation_started(services, op_name):
        return len(await services.get('data_svc').locate('operations', match=dict(name=op_name)))

    @staticmethod
    async def start_operation(services, op_name, group, adv_id):
        access = dict(access=[BaseWorld.Access.HIDDEN])
        data = dict(name=op_name, group=group, adversary_id=adv_id,
                    planner='batch', atomic_enabled=1, hidden=True)
        await services.get('rest_svc').create_operation(access=access, data=data)

    @staticmethod
    async def is_operation_successful(services, op_name, traits=[], num_links=1):
        operation = (await services.get('data_svc').locate('operations', match=dict(name=op_name)))[0]
        if len(operation.chain) == num_links and \
                all(trait in [f.trait for f in operation.all_facts()] for trait in traits):
            return True
        return False

    @staticmethod
    async def cleanup_operation(services, op_name):
        await services.get('rest_svc').delete_operation(data=dict(name=op_name))

    @staticmethod
    async def verify_attack_flag(services, technique, adv_name):
        adversaries = await services.get('data_svc').locate('adversaries', match=dict(name=adv_name))
        for adv in adversaries:
            match = await BaseFlag.does_technique_match(services, technique, adv)
            await services.get('rest_svc').delete_adversary(dict(adversary_id=adv.adversary_id))
            if match:
                return True
        return False

    @staticmethod
    async def does_technique_match(services, technique, adversary):
        techniques = set()
        for ab_id in adversary.atomic_ordering:
            techniques.add((await services.get('rest_svc').display_objects('abilities',
                                                                           data=dict(ability_id=ab_id)))[0][
                               'technique_id'])
        return technique in techniques and len(techniques) == 1
