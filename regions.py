bfm_regions: dict[str, tuple[str]] = {
    "Menu": ("Grillin Village",),
    "Grillin Village": ("Somnolent Forest","Somnolent Forest Deadend","Steamwood Forest","Twinpeak Entrance","Mine Entrance"),
    "Somnolent Forest": ("Somnolent Forest Behind Steam",),
    "Somnolent Forest Deadend": tuple(),
    "Somnolent Forest Behind Steam": tuple(),
    "Steamwood Forest": tuple(),
    "Twinpeak Entrance": ("Twinpeak Around the Bend","Twinpeak Path to Skullpeon"),
    "Twinpeak Around the Bend": ("Twinpeak Waterfall Cave 1",),
    "Twinpeak Waterfall Cave 1": ("Twinpeak Rope Bridge",),
    "Twinpeak Rope Bridge": ("Twinpeak Waterfall Cave 2",),
    "Twinpeak Waterfall Cave 2": ("Twinpeak Second Peak",),
    "Twinpeak Second Peak": tuple(),
    "Twinpeak Path to Skullpeon": tuple(),
    "Mine Entrance": ("Mine Conveyor Belt Room",),
    "Mine Conveyor Belt Room": ("Misteria Underground Lake",),
    "Misteria Underground Lake": tuple()
}