from pvz_model import (
    LawnState, LawnConfig,
    place_plant, remove_plant, plant_in_cell, get_plant_type,
    get_cell_from_xy, get_cell_center, get_cell_bounds,
    spawn_zombie, move_zombies, move_peas, spawn_peas,
    check_collisions, rects_overlap, collect_sun, spawn_sun,
    reset_level, reset_game, should_spawn_zombie, check_game_over
)


def get_config():
    return LawnConfig(width=1350, height=750, columns=9, rows=5, plant_radius=20)


def get_state():
    return LawnState()



def test_place_peashooter():
    """Test placing a peashooter plant"""
    state = get_state()
    config = get_config()
    initial_suns = state.sun_count
    
    success = place_plant(state, 0, 0, "peashooter", config)
    
    assert success is True
    assert (0, 0) in state.plants
    assert state.plants[(0, 0)]["type"] == "peashooter"
    assert state.plants[(0, 0)]["health"] == config.peashooter_health
    assert state.sun_count == initial_suns - config.plant_costs["peashooter"]


def test_place_wallnut():
    """Test placing a wallnut plant"""
    state = get_state()
    config = get_config()
    initial_suns = state.sun_count
    
    success = place_plant(state, 1, 2, "wallnut", config)
    
    assert success is True
    assert (1, 2) in state.plants
    assert state.plants[(1, 2)]["type"] == "wallnut"
    assert state.plants[(1, 2)]["health"] == config.wallnut_health
    assert state.sun_count == initial_suns - config.plant_costs["wallnut"]


def test_place_slowflower():
    """Test placing a slowflower plant"""
    state = get_state()
    config = get_config()
    initial_suns = state.sun_count
    
    success = place_plant(state, 2, 3, "slowflower", config)
    
    assert success is True
    assert (2, 3) in state.plants
    assert state.plants[(2, 3)]["type"] == "slowflower"
    assert state.plants[(2, 3)]["health"] == config.slowflower_health
    assert state.sun_count == initial_suns - config.plant_costs["slowflower"]


def test_place_plant_insufficient_suns():
    """Test that plant placement fails with insufficient suns"""
    state = get_state()
    config = get_config()
    state.sun_count = 10  # Not enough for any plant
    
    success = place_plant(state, 0, 0, "peashooter", config)
    
    assert success is False
    assert (0, 0) not in state.plants
    assert state.sun_count == 10


def test_place_plant_duplicate_cell():
    """Test that can't place plant on occupied cell"""
    state = get_state()
    config = get_config()
    
    place_plant(state, 0, 0, "peashooter", config)
    success = place_plant(state, 0, 0, "wallnut", config)
    
    assert success is False
    assert state.plants[(0, 0)]["type"] == "peashooter"


def test_remove_plant():
    """Test removing a plant"""
    state = get_state()
    config = get_config()
    
    place_plant(state, 0, 0, "peashooter", config)
    remove_plant(state, 0, 0)
    
    assert (0, 0) not in state.plants


def test_plant_in_cell():
    """Test checking if cell has plant"""
    state = get_state()
    config = get_config()
    
    assert plant_in_cell(state, 0, 0) is False
    place_plant(state, 0, 0, "peashooter", config)
    assert plant_in_cell(state, 0, 0) is True


def test_get_plant_type():
    """Test getting plant type"""
    state = get_state()
    config = get_config()
    
    place_plant(state, 0, 0, "peashooter", config)
    assert get_plant_type(state, 0, 0) == "peashooter"
    assert get_plant_type(state, 1, 1) is None


def test_get_cell_from_xy():
    """Test converting pixel to grid coordinates"""
    config = get_config()
    
    row, col = get_cell_from_xy(0, 0, config)
    assert row == 0
    assert col == 0
    
    row, col = get_cell_from_xy(150, 150, config)
    assert row >= 0
    assert col >= 0


def test_get_cell_center():
    """Test getting cell center coordinates"""
    config = get_config()
    
    cx, cy = get_cell_center(0, 0, config)
    assert cx > 0
    assert cy > 0


def test_get_cell_bounds():
    """Test getting cell bounds"""
    config = get_config()
    
    x1, y1, x2, y2 = get_cell_bounds(0, 0, config)
    assert x1 == 0
    assert y1 == 0
    assert x2 > x1
    assert y2 > y1




def test_spawn_zombie():
    """Test spawning a zombie"""
    state = get_state()
    config = get_config()
    initial_count = len(state.zombies)
    
    spawn_zombie(state, config)
    
    assert len(state.zombies) == initial_count + 1
    zombie = state.zombies[-1]
    assert zombie["x"] == config.width - 50
    assert zombie["health"] > 0
    assert zombie["type"] in ["normal", "large", "boss"]


def test_move_zombies_not_eating():
    """Test zombie movement when not eating"""
    state = get_state()
    config = get_config()
    
    spawn_zombie(state, config)
    initial_x = state.zombies[0]["x"]
    
    move_zombies(state, config)
    
    assert state.zombies[0]["x"] < initial_x


def test_move_zombies_eating():
    """Test zombie doesn't move when eating"""
    state = get_state()
    config = get_config()
    
    spawn_zombie(state, config)
    state.zombies[0]["eating"] = True
    initial_x = state.zombies[0]["x"]
    
    move_zombies(state, config)
    
    assert state.zombies[0]["x"] == initial_x


def test_spawn_peas():
    """Test peashooter spawning projectiles"""
    state = get_state()
    config = get_config()
    
    place_plant(state, 0, 0, "peashooter", config)
    
    spawn_peas(state, config)
    assert len(state.peas) > 0
    assert state.peas[0]["row"] == 0


def test_move_peas():
    """Test pea projectile movement"""
    state = get_state()
    
    state.peas.append({"row": 0, "x": 100.0, "y": 100.0})
    initial_x = state.peas[0]["x"]
    
    move_peas(state)
    
    assert state.peas[0]["x"] > initial_x


def test_sun_spawning():
    """Test sun spawning"""
    state = get_state()
    config = get_config()
    initial_count = len(state.suns)
    
    # Try multiple times to trigger spawn
    for _ in range(100):
        spawn_sun(state, config)
    
    assert len(state.suns) > initial_count


def test_collect_sun():
    """Test collecting a sun"""
    state = get_state()
    config = get_config()
    initial_suns = state.sun_count
    
    state.suns.append({"x": 100.0, "y": 100.0, "collected": False})
    
    success = collect_sun(state, 100, 100, config)
    
    assert success is True
    assert state.sun_count > initial_suns



def test_rects_overlap_true():
    """Test rectangle overlap detection - overlapping"""
    rect_a = (0, 0, 100, 100)
    rect_b = (50, 50, 150, 150)
    
    assert rects_overlap(rect_a, rect_b) is True


def test_rects_overlap_false():
    """Test rectangle overlap detection - non-overlapping"""
    rect_a = (0, 0, 100, 100)
    rect_b = (150, 150, 250, 250)
    
    assert rects_overlap(rect_a, rect_b) is False


def test_rects_overlap_touching():
    """Test rectangle overlap detection - touching edges"""
    rect_a = (0, 0, 100, 100)
    rect_b = (100, 100, 200, 200)
    
    assert rects_overlap(rect_a, rect_b) is False





def test_should_spawn_zombie_level_1():
    """Test zombie spawning should work in level 1"""
    state = get_state()
    config = get_config()
    state.level = 1
    state.zombies_spawned = 0
    
    # Should be able to spawn (probabilistic, but should succeed eventually)
    can_spawn = False
    for _ in range(1000):
        if should_spawn_zombie(state, config):
            can_spawn = True
            break
    
    assert can_spawn is True


def test_check_game_over_false():
    """Test game over condition - not met"""
    state = get_state()
    spawn_zombie(state, get_config())
    
    result = check_game_over(state)
    
    assert result is False
    assert state.game_over is False


def test_check_game_over_true():
    """Test game over condition - met"""
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    state.zombies[0]["x"] = -10  # Zombie reached left side
    
    result = check_game_over(state)
    
    assert result is True
    assert state.game_over is True


def test_reset_level():
    """Test resetting a level"""
    state = get_state()
    config = get_config()
    
    # Set up some game state
    place_plant(state, 0, 0, "peashooter", config)
    spawn_zombie(state, config)
    state.zombies_killed = 5
    
    reset_level(state)
    
    assert len(state.plants) == 0
    assert len(state.zombies) == 0
    assert state.zombies_killed == 0
    assert state.sun_count == 150


def test_reset_game():
    """Test resetting entire game"""
    state = get_state()
    config = get_config()
    
    # Advance state
    state.level = 2
    place_plant(state, 0, 0, "peashooter", config)
    state.zombies_killed = 10
    
    reset_game(state)
    
    assert state.level == 1
    assert state.running is True
    assert state.game_over is False
    assert len(state.plants) == 0
    assert state.zombies_killed == 0
    assert state.sun_count == 150


def test_get_plant_type_wallnut():
    state = get_state()
    place_plant(state, 0, 0, "wallnut")
    assert get_plant_type(state, 0, 0) == "wallnut"


def test_get_plant_type_empty():
    state = get_state()
    assert get_plant_type(state, 0, 0) is None


def test_remove_plant():
    state = get_state()
    place_plant(state, 0, 0, "peashooter")
    assert plant_in_cell(state, 0, 0) is True
    remove_plant(state, 0, 0)
    assert plant_in_cell(state, 0, 0) is False


def test_get_cell_from_xy_origin():
    config = get_config()
    row, col = get_cell_from_xy(0, 0, config)
    assert row == 0
    assert col == 0


def test_get_cell_from_xy_middle():
    config = get_config()
    row, col = get_cell_from_xy(600, 300, config)
    assert row == 2
    assert col == 4


def test_get_cell_from_xy_bottom_right():
    config = get_config()
    row, col = get_cell_from_xy(1000, 500, config)
    assert 0 <= row < config.rows
    assert 0 <= col < config.columns


def test_get_cell_center_top_left():
    config = get_config()
    center_x, center_y = get_cell_center(0, 0, config)
    assert center_x > 0
    assert center_y > 0


def test_get_cell_center_consistency():
    config = get_config()
    row, col = 2, 3
    x1, y1, x2, y2 = get_cell_bounds(row, col, config)
    cx, cy = get_cell_center(row, col, config)
    assert x1 <= cx <= x2
    assert y1 <= cy <= y2


def test_get_cell_bounds():
    config = get_config()
    x1, y1, x2, y2 = get_cell_bounds(0, 0, config)
    assert x1 == 0
    assert y1 == 0
    assert x2 > x1
    assert y2 > y1


def test_get_cell_bounds_consecutive_cells():
    config = get_config()
    x1_a, y1_a, x2_a, y2_a = get_cell_bounds(0, 0, config)
    x1_b, y1_b, x2_b, y2_b = get_cell_bounds(0, 1, config)
    assert x2_a == x1_b


def test_spawn_zombie_initial_position():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    assert len(state.zombies) == 1
    assert state.zombies[0]["x"] == config.width - 50
    assert 0 <= state.zombies[0]["row"] < config.rows


def test_spawn_zombie_types():
    state = get_state()
    config = get_config()
    for _ in range(20):
        spawn_zombie(state, config)
    
    types = {z["type"] for z in state.zombies}
    assert "normal" in types


def test_move_zombies_normal():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    initial_x = state.zombies[0]["x"]
    move_zombies(state)
    assert state.zombies[0]["x"] < initial_x


def test_move_zombies_while_eating():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    state.zombies[0]["eating"] = True
    initial_x = state.zombies[0]["x"]
    move_zombies(state)
    assert state.zombies[0]["x"] == initial_x


def test_move_multiple_zombies():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    spawn_zombie(state, config)
    initial_positions = [z["x"] for z in state.zombies]
    move_zombies(state)
    final_positions = [z["x"] for z in state.zombies]
    for initial, final in zip(initial_positions, final_positions):
        assert final < initial


def test_spawn_peas_with_peashooter():
    state = get_state()
    config = get_config()
    place_plant(state, 0, 0, "peashooter")
    state.pea_cooldown = 0
    spawn_peas(state, config)
    assert len(state.peas) > 0


def test_spawn_peas_cooldown():
    state = get_state()
    config = get_config()
    place_plant(state, 0, 0, "peashooter")
    state.pea_cooldown = 0
    spawn_peas(state, config)
    pea_count_first = len(state.peas)
    spawn_peas(state, config)
    assert len(state.peas) == pea_count_first


def test_spawn_peas_no_plants():
    state = get_state()
    config = get_config()
    state.pea_cooldown = 0
    spawn_peas(state, config)
    assert len(state.peas) == 0


def test_move_peas():
    state = get_state()
    state.peas = [{"row": 0, "x": 100}]
    move_peas(state)
    assert state.peas[0]["x"] == 108


def test_move_peas_removes_off_screen():
    state = get_state()
    state.peas = [{"row": 0, "x": 1400}, {"row": 0, "x": 100}]
    move_peas(state)
    assert len(state.peas) == 1
    assert state.peas[0]["x"] == 108


def test_rects_overlap_overlapping():
    rect_a = (0, 0, 10, 10)
    rect_b = (5, 5, 15, 15)
    assert rects_overlap(rect_a, rect_b) is True


def test_rects_overlap_not_overlapping():
    rect_a = (0, 0, 10, 10)
    rect_b = (20, 20, 30, 30)
    assert rects_overlap(rect_a, rect_b) is False


def test_rects_overlap_touching_edge():
    rect_a = (0, 0, 10, 10)
    rect_b = (10, 0, 20, 10)
    assert rects_overlap(rect_a, rect_b) is False


def test_zombie_plant_collision():
    state = get_state()
    config = get_config()
    place_plant(state, 0, 0, "peashooter")
    spawn_zombie(state, config)
    state.zombies[0]["row"] = 0
    state.zombies[0]["x"] = 100
    
    initial_health = state.plants[(0, 0)]["health"]
    check_collisions(state, config)
    
    assert state.plants[(0, 0)]["health"] < initial_health


def test_zombie_plant_collision_kills_plant():
    state = get_state()
    config = get_config()
    place_plant(state, 0, 0, "wallnut")
    spawn_zombie(state, config)
    state.zombies[0]["row"] = 0
    state.zombies[0]["x"] = 100
    state.plants[(0, 0)]["health"] = 1
    
    check_collisions(state, config)
    assert (0, 0) not in state.plants


def test_pea_zombie_collision():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    state.peas = [{"row": state.zombies[0]["row"], "x": state.zombies[0]["x"]}]
    
    initial_health = state.zombies[0]["health"]
    check_collisions(state, config)
    
    assert state.zombies[0]["health"] < initial_health


def test_pea_zombie_collision_kills_zombie():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    state.zombies[0]["health"] = 2
    state.peas = [{"row": state.zombies[0]["row"], "x": state.zombies[0]["x"]}]
    
    check_collisions(state, config)
    
    assert len(state.zombies) == 0
    assert state.zombies_killed == 1


def test_pea_removed_on_zombie_hit():
    state = get_state()
    config = get_config()
    spawn_zombie(state, config)
    state.peas = [{"row": state.zombies[0]["row"], "x": state.zombies[0]["x"]}]
    
    check_collisions(state, config)
    
    assert len(state.peas) == 0


def test_initial_state():
    state = get_state()
    assert state.level == 1
    assert state.zombies_killed == 0
    assert state.zombies_spawned == 0
    assert state.victory is False


def test_config_initialization():
    config = get_config()
    assert config.width == 1200
    assert config.height == 600
    assert config.columns == 9
    assert config.rows == 5
    assert config.pea_shooter_health == 20
    assert config.wallnut_health == 10
