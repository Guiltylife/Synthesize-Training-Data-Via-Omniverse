# .\omni.code.replicator.bat --no-window --/omni/replicator/script=E:/Replicator/ReplicatorScript.py
import random

import omni.replicator.core as rep

with rep.new_layer():
    # Scene
    SCENE_LANDSCAPE = 'omniverse://localhost/Users/admin/USD/scene/MyRanchOutside_Landscape.usd'
    SCENE_BUILDING1 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building1.usd'
    SCENE_BUILDING2 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building2.usd'
    SCENE_BUILDING3 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building3.usd'
    SCENE_BUILDING4 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building4.usd'
    SCENE_BUILDING5 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building5.usd'
    SCENE_BUILDING6 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building6.usd'
    SCENE_BUILDING7 = 'omniverse://localhost/Users/admin/USD/scene/Buildings/MyRanchOutside_Building7.usd'
    SCENE_FENCE = 'omniverse://localhost/Users/admin/USD/scene/MyRanchOutside_Fence.usd'
    SCENE_FEEDER1 = 'omniverse://localhost/Users/admin/USD/scene/Feeder/MyRanchOutside_Feeder1.usd'
    SCENE_FEEDER2 = 'omniverse://localhost/Users/admin/USD/scene/Feeder/MyRanchOutside_Feeder2.usd'
    SCENE_FEEDER3 = 'omniverse://localhost/Users/admin/USD/scene/Feeder/MyRanchOutside_Feeder3.usd'
    SCENE_HAY1 = 'omniverse://localhost/Users/admin/USD/scene/Hay/MyRanchOutside_Hay1.usd'
    SCENE_HAY2 = 'omniverse://localhost/Users/admin/USD/scene/Hay/MyRanchOutside_Hay2.usd'
    # Animals
    CHICKEN = 'omniverse://localhost/Users/admin/USD/animals/Chicken.usd'
    COW = 'omniverse://localhost/Users/admin/USD/animals/Cow.usd'
    GOAT = 'omniverse://localhost/Users/admin/USD/animals/Goat.usd'
    PIG = 'omniverse://localhost/Users/admin/USD/animals/Pig.usd'
    SHEEP = 'omniverse://localhost/Users/admin/USD/animals/Sheep.usd'
    # Vegetations
    TREE1 = 'omniverse://localhost/Users/admin/USD/vegetation/Collected_American_Beech/American_Beech.usd'
    TREE2 = 'omniverse://localhost/Users/admin/USD/vegetation/Collected_Common_Apple/Common_Apple.usd'
    # Animal textures
    CHICKEN_T1 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Chicken/T_ChickenA_BaseColor.png'
    CHICKEN_T2 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Chicken/T_ChickenB_BaseColor.png'
    CHICKEN_T3 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Chicken/T_ChickenC_BaseColor.png'
    COW_T1 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Cow/T_Cow1_BaseColor.png'
    COW_T2 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Cow/T_Cow2_BaseColor.png'
    COW_T3 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Cow/T_Cow3_BaseColor.png'
    GOAT_T1 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Goat/T_Goat_BaseColor.png'
    PIG_T1 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Pig/T_Pig_BaseColor.png'
    PIG_T2 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Pig/T_PigDirty_BaseColor.png'
    SHEEP_T1 = 'omniverse://localhost/Users/admin/USD/animalsTextures/Sheep/T_Sheep_BaseColor.png'
    # Ski light
    SKI = 'omniverse://localhost/Users/admin/HDRI_01.dds'

    def animal():
        rand_num = random.randint(0,4)
        if rand_num == 0:
            animal = rep.create.from_usd(CHICKEN, semantics=[('class', 'chicken')])
        elif rand_num == 1:
            animal = rep.create.from_usd(COW, semantics=[('class', 'cow')])
        elif rand_num == 2:
            animal = rep.create.from_usd(GOAT, semantics=[('class', 'goat')])
        elif rand_num == 3:
            animal = rep.create.from_usd(PIG, semantics=[('class', 'pig')])
        elif rand_num == 4:
            animal = rep.create.from_usd(SHEEP, semantics=[('class', 'sheep')])

        with animal:
            rep.modify.pose(
                position=rep.distribution.uniform((-1400, 0, -1400), (1400, 0, 1400)),
                rotation=rep.distribution.uniform((0,-180, 0), (0, 180, 0)),
            )
            if rand_num == 0:
                rep.randomizer.texture(textures=[CHICKEN_T1, CHICKEN_T2, CHICKEN_T3])
            elif rand_num == 1:
                rep.randomizer.texture(textures=[COW_T1, COW_T2, COW_T3])
            elif rand_num == 2:
                rep.randomizer.texture(textures=[GOAT_T1])
            elif rand_num == 3:
                rep.randomizer.texture(textures=[PIG_T1, PIG_T2])
            elif rand_num == 4:
                rep.randomizer.texture(textures=[SHEEP_T1])
        return animal

    def tree():
        rand_num = random.randint(0,1)
        tree = rep.create.from_usd([TREE1, TREE2][rand_num], semantics=[('class', 'tree')])

        with tree:
            rep.modify.pose(
                position=rep.distribution.uniform((-1400, 0, -1400), (1400, 0, 1400)),
                rotation=rep.distribution.uniform((-90,-180, 0), (-90, 180, 0)),
            )
        return tree

    # Register randomization
    rep.randomizer.register(animal)
    rep.randomizer.register(tree)

    # Setup the static elements
    scene_landscape = rep.create.from_usd(SCENE_LANDSCAPE, semantics=[('class', 'grass')])
    scene_building1 = rep.create.from_usd(SCENE_BUILDING1, semantics=[('class', 'building')])
    scene_building2 = rep.create.from_usd(SCENE_BUILDING2, semantics=[('class', 'building')])
    scene_building3 = rep.create.from_usd(SCENE_BUILDING3, semantics=[('class', 'building')])
    scene_building4 = rep.create.from_usd(SCENE_BUILDING4, semantics=[('class', 'building')])
    scene_building5 = rep.create.from_usd(SCENE_BUILDING5, semantics=[('class', 'building')])
    scene_building6 = rep.create.from_usd(SCENE_BUILDING6, semantics=[('class', 'building')])
    scene_building7 = rep.create.from_usd(SCENE_BUILDING7, semantics=[('class', 'building')])
    scene_fence = rep.create.from_usd(SCENE_FENCE, semantics=[('class', 'fence')])
    scene_feeder1 = rep.create.from_usd(SCENE_FEEDER1, semantics=[('class', 'feeder')])
    scene_feeder2 = rep.create.from_usd(SCENE_FEEDER2, semantics=[('class', 'feeder')])
    scene_feeder3 = rep.create.from_usd(SCENE_FEEDER3, semantics=[('class', 'feeder')])
    scene_hay1 = rep.create.from_usd(SCENE_HAY1, semantics=[('class', 'hay')])
    scene_hay2 = rep.create.from_usd(SCENE_HAY2, semantics=[('class', 'hay')])

    # Setup light
    light = rep.create.light(
        light_type="Dome",
        rotation=(270,0,0),
        texture=SKI
    )

    # Setup camera and attach it to render product
    camera = rep.create.camera(
        focus_distance=1000,
        f_stop=1.8
    )
    render_product = rep.create.render_product(camera, resolution=(1024, 1024))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="E:/Replicator/datasets/ReplicatorData",
        rgb=True,
        bounding_box_2d_tight=True,
        semantic_segmentation=True,
        distance_to_camera=True
    )
    writer.attach([render_product])

    with rep.trigger.on_frame(interval=1, num_frames=10):
        for i in range(2):
            rep.randomizer.tree()
        for i in range(16):
            rep.randomizer.animal()
        with light:
            rep.modify.attribute("exposure", rep.distribution.uniform(-8, 0))
            rep.modify.pose(rotation=rep.distribution.uniform((270, -180, 0), (270, 180, 0)))
        with camera:
            rep.modify.pose(position=rep.distribution.uniform((-1600, 200, -1600), (1600, 300, 1600)), look_at=scene_landscape)
