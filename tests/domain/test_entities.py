from assertpy import assert_that, fail
from msgspec import json
from pytest import fixture

from kdp.domain.entities import (
    KDPMap,
    MapDimensionsOrdinal,
    Villain)
from kdp.domain.value_objects import (
    MapDirectionsOrdinal as Direction,
    MapLocationOrdinal,
    ValidationError)



@fixture
def base_map():
    return KDPMap.factory(rows=20, columns=30, objects=[])

@fixture
def capt_kidd():
    return Villain.factory(
        name="Captain Kidd",
        row=1,
        col=1,
        direction=Direction.NORTH,
        size=1)


@fixture
def big_villain():
    return Villain.factory(
        name="Big Villain",
        row=1,
        col=1,
        direction=Direction.NORTH,
        size=3)

def pytest_smoke_test():
    """basid test if pytest is configured and working properly"""
    pass


def assertpy_smoke_test():
    """basic test if assertpy is configured and working properly"""
    assert_that(1).is_equal_to(1)


def map_dimensions_ordinal_test():
    json_data = b'{"rows": 10, "columns": 30}'
    dims = json.decode(json_data, type=MapDimensionsOrdinal)

    assert_that(dims.rows).is_equal_to(10)
    assert_that(dims.columns).is_equal_to(30)


def map_dimenisions_ordinal_constraints_test():
    json_data = b'{"rows": -10, "columns": 30}'
    try:
        dims = json.decode(json_data, type=MapDimensionsOrdinal)
        fail(f"should have raised an exception, but got {dims}")
    except ValidationError as e:
        assert_that(e).is_not_none()
        assert_that(str(e)).contains("Expected `int` >= 1")


def kdp_map_test():
    kdp_map = KDPMap(dimensions=MapDimensionsOrdinal(10, 30), objects=[])

    assert_that(kdp_map.dimensions.rows).is_equal_to(10)
    assert_that(kdp_map.dimensions.columns).is_equal_to(30)


def kdp_map_w_negative_dimensions_test():
    try:
        kdp_map = KDPMap.factory(rows=-10, columns=-30, objects=[])
        fail(f"should have raised an exception got {kdp_map}")
    except ValidationError as e:
        assert_that(e).is_not_none()
        assert_that(str(e)).contains("rows and columns must be greater than 0")


def villain_test():
    villain = Villain(
        name='Captain Kidd',
        location=MapLocationOrdinal(row=5, column=5),
        direction=Direction.NORTH,
        size=MapDimensionsOrdinal(1, 1))

    assert_that(villain.name).is_equal_to('Captain Kidd')
    assert_that(villain.location.row).is_equal_to(5)
    assert_that(villain.location.column).is_equal_to(5)
    assert_that(villain.direction).is_equal_to(Direction.NORTH)
    assert_that(villain.size.rows).is_equal_to(1)
    assert_that(villain.size.columns).is_equal_to(1)


def place_kidd_on_map_test(base_map, capt_kidd):
    base_map.place(capt_kidd, 5, 5)

    assert_that(base_map.objects).is_length(1)
    assert_that(base_map.objects[0].name).is_equal_to('Captain Kidd')
    assert_that(base_map.objects[0].location.row).is_equal_to(5)
    assert_that(base_map.objects[0].location.column).is_equal_to(5)
    assert_that(base_map.objects[0].direction).is_equal_to(Direction.NORTH)
    assert_that(base_map.objects[0].size.rows).is_equal_to(1)
    assert_that(base_map.objects[0].size.columns).is_equal_to(1)


def re_place_kidd_on_map_test(base_map, capt_kidd):
    base_map.place(capt_kidd, 10, 10)
    base_map.place(capt_kidd, 5, 5)

    assert_that(base_map.objects).is_length(1)
    assert_that(base_map.objects[0].name).is_equal_to('Captain Kidd')
    assert_that(base_map.objects[0].location.row).is_equal_to(5)
    assert_that(base_map.objects[0].location.column).is_equal_to(5)
    assert_that(base_map.objects[0].direction).is_equal_to(Direction.NORTH)
    assert_that(base_map.objects[0].size.rows).is_equal_to(1)
    assert_that(base_map.objects[0].size.columns).is_equal_to(1)


def move_kidd_on_map_test(base_map, capt_kidd):
    base_map.place(capt_kidd, 5, 5)
    base_map.move(capt_kidd, 10, 10)

    assert_that(base_map.objects).is_length(1)
    assert_that(base_map.objects[0].name).is_equal_to('Captain Kidd')
    assert_that(base_map.objects[0].location.row).is_equal_to(10)
    assert_that(base_map.objects[0].location.column).is_equal_to(10)
    assert_that(base_map.objects[0].direction).is_equal_to(Direction.NORTH)
    assert_that(base_map.objects[0].size.rows).is_equal_to(1)
    assert_that(base_map.objects[0].size.columns).is_equal_to(1)


def move_object_not_on_map_failure_test(base_map, capt_kidd):
    try:
        base_map.move(capt_kidd, 5, 5)
        fail("should have raised an exception")
    except ValidationError as e:
        assert_that(e).is_not_none()
        assert_that(str(e)).contains("cannot move Captain Kidd to 5, 5, object not on map")


def place_big_villian_on_map_test(base_map, big_villain):
    base_map.place(big_villain, 5, 5)

    assert_that(base_map.objects).is_length(1)
    assert_that(base_map.objects[0].name).is_equal_to('Big Villain')
    assert_that(base_map.objects[0].location.row).is_equal_to(5)
    assert_that(base_map.objects[0].location.column).is_equal_to(5)
    assert_that(base_map.objects[0].direction).is_equal_to(Direction.NORTH)
    assert_that(base_map.objects[0].size.rows).is_equal_to(3)
    assert_that(base_map.objects[0].size.columns).is_equal_to(3)


def place_big_villian_off_map_test(base_map, big_villain):
    try:
        base_map.place(big_villain, 25, 5)
        fail("should have raised an exception")
    except ValidationError as e:
        assert_that(e).is_not_none()
        assert_that(str(e)).contains("cannot place Big Villain at 25, 5, no such location")


def place_big_villian_too_close_to_edge_test(base_map, big_villain):
    try:
        base_map.place(big_villain, 15, 28)
        fail("should have raised an exception")
    except ValidationError as e:
        assert_that(e).is_not_none()
        assert_that(str(e)).contains("cannot place Big Villain at 15, 28, object does not fit")
