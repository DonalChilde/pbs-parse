from importlib import resources
from pathlib import Path

from pbs_parse.pbs_2022_01.models.split import trip_lines_serializer
from pbs_parse.pbs_2022_01.split.extract_trips import parse_trips_from_file, write_trips
from tests.resources import RESOURCES_ANCHOR

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.page_3_of_173.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_page_to_trips(test_output_dir: Path):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        path_out = test_output_dir / Path("trip/test_page_to_trip")
        trips = parse_trips_from_file(input_path)
        count = write_trips(
            file_stem=input_path.stem, trips=trips, path_out=path_out, overwrite=False
        )
        files_output = list(path_out.glob("*.trip_*"))
        assert len(files_output) == count
        assert count == 5
        serializer = trip_lines_serializer()
        trip = serializer.load_from_json(path_in=files_output[2])
        assert len(trip.lines) > 5
