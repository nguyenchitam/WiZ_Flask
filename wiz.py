from pywizlight import wizlight, PilotBuilder, discovery

import db


async def update_state(ip):
    try:
        bulb = wizlight(ip)
        bulb_state = await bulb.updateState()
        if bulb_state:
            print(bulb, bulb_state.pilotResult)
            db.update_bulb_state(bulb.ip, bulb_state.get_state(), bulb_state.get_scene_id(), bulb_state.get_scene())
    except Exception as error:
        print(f'Cannot get State {ip}: {error}')
        db.update_bulb_down(ip)


async def update_all_states():
    bulbs = db.get_all_bulbs()
    for bulb in bulbs:
        await update_state(bulb["IP"])


async def scan():
    # bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    bulbs = await discovery.discover_lights()
    for bulb in bulbs:
        print(bulb)
        db.add_bulb(bulb.ip)

    await update_all_states()


async def on(ip):
    try:
        bulb = wizlight(ip)
        await bulb.turn_on(PilotBuilder(brightness=255))
    except Exception as error:
        print(f'Cannot switch on {ip}: {error}')

    await update_state(ip)


async def off(ip):
    try:
        bulb = wizlight(ip)
        await bulb.turn_off()
    except Exception as error:
        print(f'Cannot switch off {ip}: {error}')

    await update_state(ip)


async def scene(ip, scene_id):
    try:
        bulb = wizlight(ip)
        await bulb.turn_on(PilotBuilder(scene=scene_id))
    except Exception as error:
        print(f'Cannot change {ip} to scene {scene_id}: {error}')

    await update_state(ip)
