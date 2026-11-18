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


SHARED = (
    "AuthenticationError", "CannotConnectError", "Certainty", "Change", "ClientError", "Clock", "DataValue",
    "DeviceClient", "Identity", "InvalidValueError", "Key", "Labels", "Limits", "ModelError", "NotConnectedError",
    "PointsCallback", "PollRate", "Quality", "ReadOnlyError", "Selector", "Status", "StatusCallback", "Unit",
    "UnsupportedDeviceError", "ValueCallback", "Write", "WriteKind", "WriteRange",
)
"""What every device library exports, as event_connect's own, so that each is used alike."""

NILANS_OWN = ("DiscoveredDevice", "discover")
"""Names modbus_event_connect has too, for something of its own."""


def test_it_exports_what_every_device_library_shares_as_event_connects_own() -> None:
    import event_connect

    assert [name for name in SHARED if name not in nilan_connect.__all__] == []
    assert [name for name in SHARED if getattr(nilan_connect, name) is not getattr(event_connect, name)] == []


def test_what_it_passes_on_from_the_libraries_it_is_built_on_is_their_own() -> None:
    """What the package passes on is modbus_event_connect's or event_connect's own, not a copy that
    could drift."""
    import event_connect
    import modbus_event_connect
    import modbus_event_connect.micro_nabto
    import modbus_event_connect.testing

    import nilan_connect.testing

    for package, sources in (
        (nilan_connect, (modbus_event_connect, modbus_event_connect.micro_nabto, event_connect)),
        (nilan_connect.testing, (modbus_event_connect.testing,)),
    ):
        for name in (name for name in package.__all__ if name not in NILANS_OWN):
            source = next((s for s in sources if name in getattr(s, "__all__", ())), None)
            if source is not None:
                assert getattr(package, name) is getattr(source, name), name
    assert "Client" in nilan_connect.__all__
    assert "SimulatedMicroNabtoDevice" in nilan_connect.testing.__all__


def test_it_names_the_range_a_setting_can_be_written_with() -> None:
    """A consumer offers a setting the values its `Point.write_range()` gives."""
    import event_connect

    assert nilan_connect.WriteRange is event_connect.WriteRange
    assert "WriteRange" in nilan_connect.__all__
