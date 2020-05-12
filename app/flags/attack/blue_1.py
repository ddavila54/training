name = 'ATT&CK Quiz 2'
challenge = 'Refer to \'ATT&CK Quiz 1\' for instructions. Name the uploaded adversary exactly \'blue_quiz_2\'. ' \
            'Ensure that you\'re starting from a fresh layer on the Compass plugin.\n\n' \
            'The adversary procedure is:\nImport-Module .\\invoke-mimi.ps1; Invoke-Mimikatz -DumpCreds'
extra_info = """"""


async def verify(services):
    adversaries = await services.get('data_svc').locate('adversaries', match=dict(name='blue_quiz_2'))
    technique = 'T1003'  # Credential Dumping
    for adv in adversaries:
        match = await does_technique_match(services, adv, technique)
        await services.get('rest_svc').delete_adversary(dict(adversary_id=adv.adversary_id))
        if match:
            return True
    return False


async def does_technique_match(services, adv, technique):
    techniques = set()
    for ab_id in adv.atomic_ordering:
        techniques.add((await services.get('rest_svc').display_objects('abilities',
                                                                       data=dict(ability_id=ab_id)))[0]['technique_id'])
    return technique in techniques and len(techniques) == 1