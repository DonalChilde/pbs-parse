import json
from dataclasses import asdict
from importlib import resources

from pbs_parse.pbs_2022_01.models.split import page_lines_serializer
from tests.resources import RESOURCES_ANCHOR

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.page_1_of_173.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_load_page():
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        serializer = page_lines_serializer()
        page = serializer.load_from_json(path_in=input_path)
        page_json = json.loads(input_path.read_text(encoding="utf-8"))
        page_dict = asdict(page)
        assert page_json == page_dict
