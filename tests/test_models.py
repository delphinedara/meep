import tempfile
from datetime import date, timedelta

import pytest

from meep.models import db
from meep.models import Address, AreaOfEffect, Coordinate, FuelType, Owner
from meep.models import Line, Project, Radius, Site
from meep import create_app
from config import TestingConfig



# test creation of objects without forming relationships

@pytest.fixture(scope='module')
def new_address():
    address = Address(
        id=87,
        address="1882 133 Pl.",
        city="Overland Park",
        state="KS",
        zip=66209
    )
    return address


def test_new_address(new_address):
    assert new_address.id == 87
    print(new_address.id)
    assert new_address.address == "1882 133 Pl."
    assert new_address.city == "Overland Park"
    assert new_address.state == "KS"
    assert new_address.zip == 66209


@pytest.fixture(scope='module')
def new_area_of_effect():
    aoe = AreaOfEffect(
        id=44442222
    )
    return aoe


def test_new_area_of_effect(new_area_of_effect):
    assert new_area_of_effect.id == 44442222


@pytest.fixture(scope='module')
def new_coordinate():
    return Coordinate(
        id = 44442222,
        lat = 32.1,
        long = -87.42
    )


def test_new_coordinate(new_coordinate):
    assert new_coordinate.id == 44442222
    assert new_coordinate.lat == 32.1
    assert new_coordinate.long == -87.42


@pytest.fixture(scope='module')
def new_fuel_type():
    return FuelType(
        id = 42,
        fuel = "Diesel"
    )


def test_new_fuel_type(new_fuel_type):
    assert new_fuel_type.id == 42
    assert new_fuel_type.fuel == "Diesel"


@pytest.fixture(scope='module')
def new_owner():
    return Owner(
        id=42,
        name="Howie Mandell",
        summary="American actor and talk show host."
    )

def test_new_owner(new_owner):
    assert new_owner.id == 42
    assert new_owner.name == "Howie Mandell"
    assert new_owner.summary == "American actor and talk show host."


@pytest.fixture(scope='module')
def new_line():
    return Line(
        id=23
    )


def test_new_line(new_line):
    assert new_line.id == 23


@pytest.fixture(scope='module')
def new_project():
    return Project(
        id=42,
        name="Clean kitchen",
        start_date=date(1992, 12, 24),
        duration=timedelta(365),
        project_type="Classified",
        summary="Go clean the kitchen. It is a mess."
    )


def test_new_project(new_project):
    assert new_project.id == 42
    assert new_project.name == "Clean kitchen"
    assert new_project.start_date == date(1992, 12, 24)
    assert new_project.duration == timedelta(365)
    assert new_project.summary == "Go clean the kitchen. It is a mess."


@pytest.fixture(scope='module')
def new_radius():
    return Radius(
        id=24,
        radius=55.55
    )


def test_new_radius(new_radius):
    assert new_radius.id == 24
    assert new_radius.radius == 55.55


@pytest.fixture(scope='module')
def new_site():
    return Site(
        id=42,
        GHG_reduced=12.0,
        GGE_reduced=34.3
    )


def test_new_site(new_site):
    assert new_site.id == 42
    assert new_site.GHG_reduced == 12.0
    assert new_site.GGE_reduced == 34.3


# test relationships


def test_owner_addresses():
    owner = Owner(name='Ted Bundy', summary='American serial killer')
    address_1 = Address(
        address='84 Pennings Lane',
        city='Olathe',
        state='KS',
        zip=66211,
        owner=owner
    )
    assert owner.addresses.pop() == address_1
    address_2 = Address(
        address='123 88th Street',
        city='Kansas City',
        state='MO',
        zip=12345
    )
    owner.addresses.append(address_2)
    assert owner.addresses.pop() == address_2

def test_owner_projects():
    owner_1 = Owner(name='Zapp Brannigan', summary='Starship captain. Notorious womanizer.')
    owner_2 = Owner(name='Prof. Farnsworth', summary='Proper genius')
    project_1 = Project(
        name='Go grocery shopping'
    )
    project_2 = Project(
        name='Clean out car'
    )
    owner_1.projects += [project_1, project_2]
    owner_2.projects.append(project_1)
    assert project_1 in owner_1.projects
    assert project_2 in owner_1.projects
    assert owner_1 in project_1.owners
    assert owner_2 in project_1.owners

def test_project_sites():
    project = Project(name="meep")
    site_1 = Site()
    project.sites.append(site_1)
    site_2 = Site(project=project)
    assert site_1 in project.sites
    assert site_2 in project.sites

def test_site_aoes():
    site = Site()
    aoe_1 = AreaOfEffect()
    site.areas_of_effect.append(aoe_1)
    aoe_2 = AreaOfEffect(site=site)
    assert aoe_1 in site.areas_of_effect
    assert aoe_2 in site.areas_of_effect


def test_aoe_radius():
    radius = Radius(radius=3.14)
    aoe = AreaOfEffect(radius=radius)
    assert aoe.radius == radius
    assert aoe.radius.radius == 3.14
    assert radius.area_of_effect == aoe


def test_aoe_line():
    line = Line()
    aoe = AreaOfEffect(line=line)
    assert aoe.line == line
    with pytest.raises(AttributeError)
        assert line.area_of_effect == aoe


def test_line_end_address():
    address = Address()
    line = Line(end_location=address)
    assert line.end_location == address
    with pytest.raises(AttributeError):
        assert address.line == line


def test_aoe_fuel_type():
    fuel = FuelType(fuel="ethanol")
    aoe_1 = AreaOfEffect(fuel_type=fuel)
    aoe_2 = AreaOfEffect(fuel_type=fuel)
    assert aoe_1.fuel_type is fuel
    assert aoe_2.fuel_type is fuel
    assert aoe_1 in fuel.areas_of_effect
    assert aoe_2 in fuel.areas_of_effect


def test_aoe_address():
    address = Address()
    aoe = AreaOfEffect(address=address)
    assert aoe.address is address
    with pytest.raises(AttributeError):
        assert address.area_of_effect is aoe


def test_address_coordinates():
    c = Coordinate(lat=12.2, long=-42.3)
    a = Address(coordinate=c)
    assert c.address is a
    assert a.coordinate is c
