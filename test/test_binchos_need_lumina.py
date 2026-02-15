from .bases import BFMTestBase


class TestBinchoNeedLumina(BFMTestBase):
    options = {
        "lumina_randomzied": "true",
        "set_lang": "en",
    }

    def test_binchos_need_lumina(self) -> None:
        """Test locations that require lumina"""
        locations = ["Seer Bincho - Somnolent Forest", "KnightD Bincho - Upper Mines Before Digging"]
        items = [["Lumina"]]
        # This tests that the provided locations aren't accessible without the provided items, but can be accessed once
        # the items are obtained.
        # This will also check that any locations not provided don't have the same dependency requirement.
        # Optionally, passing only_check_listed=True to the method will only check the locations provided.
        self.assertAccessDependency(locations, items, only_check_listed=True)
