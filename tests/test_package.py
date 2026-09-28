"""The package as it is installed: what a type checker and a user of it see."""
import importlib.metadata
import importlib.resources
import re

import nilan_connect


def test_it_ships_its_types() -> None:
    """PEP 561: without py.typed, a type checker treats every import of the package as untyped."""
    assert importlib.resources.files(nilan_connect).joinpath("py.typed").is_file()


def test_its_version_is_the_one_it_was_installed_as() -> None:
    assert nilan_connect.__version__ == importlib.metadata.version("nilan_connect")


def test_every_link_in_its_description_works_where_the_description_is_shown() -> None:
    """PyPI shows the README without the repository's files, so a relative link there is dead."""
    description = importlib.metadata.metadata("nilan_connect").json["description"]
    assert isinstance(description, str) and description
    links = re.findall(r"\]\(([^)]+)\)", description)
    assert links and all(link.startswith(("https://", "#")) for link in links), links


def test_what_it_passes_on_from_modbus_event_connect_is_that_packages_own() -> None:
    """What the package passes on is modbus_event_connect's own, not a copy that could drift."""
    import modbus_event_connect
    import modbus_event_connect.micro_nabto
    import modbus_event_connect.testing

    import nilan_connect.testing

    for package, sources in (
        (nilan_connect, (modbus_event_connect, modbus_event_connect.micro_nabto)),
        (nilan_connect.testing, (modbus_event_connect.testing,)),
    ):
        for name in package.__all__:
            source = next((s for s in sources if name in getattr(s, "__all__", ())), None)
            if source is not None:
                assert getattr(package, name) is getattr(source, name), name
    assert "Client" in nilan_connect.__all__
    assert "SimulatedMicroNabtoDevice" in nilan_connect.testing.__all__
