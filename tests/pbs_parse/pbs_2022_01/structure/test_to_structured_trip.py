# from datetime import date
# from importlib import resources
# from pathlib import Path

# import pytest

# from pbs_parse.pbs_2022_01.models.parsed_trip import parsed_trip_serializer
# from pbs_parse.pbs_2022_01.models.structured import structured_trip_serializer
# from pbs_parse.pbs_2022_01.structure.parsed_to_structured_2 import translate
# from pbs_parse.pbs_2022_01.validate.validate_structured import validate_files
# from tests.resources.model import FileBasedTest
# from tests.resources.trips import TRIPS_PARSED_ANCHOR, TRIPS_STRUCTURED_ANCHOR

# OUTPUT_PATH = f"trips/structured/{Path(__file__).stem}"

# items = [
#     FileBasedTest(
#         input_anchor=TRIPS_PARSED_ANCHOR,
#         input_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.parsed.json",
#         comparison_anchor=TRIPS_STRUCTURED_ANCHOR,
#         comparison_filename="PBS_DFW_November_2024_20241010125734.page_8_of_1096.trip_3_of_5.structured.json",
#     )
# ]

# PARSE_ONLY = False


# @pytest.mark.parametrize("structure_trips_data", items)
# def test_structure_trips(test_output_dir: Path, structure_trips_data: FileBasedTest):
#     indexed_file = resources.files(structure_trips_data.input_anchor).joinpath(
#         structure_trips_data.input_filename
#     )
#     parsed_serializer = parsed_trip_serializer()
#     with resources.as_file(indexed_file) as input_path:
#         parsed_trip = parsed_serializer.load_from_json(path_in=input_path)
#         path_out = test_output_dir / OUTPUT_PATH / f"{input_path.stem}.structured.json"
#     structured_trip = translate(
#         parsed_trip=parsed_trip,
#         effective_from=date(2024, 11, 1),
#         effective_to=date(2024, 12, 1),
#     )
#     structured_serializer = structured_trip_serializer()
#     structured_serializer.save_as_json(path_out=path_out, complex_obj=structured_trip)
#     ctx = validate_files(parsed_trip_path=input_path, structured_trip_path=path_out)
#     if ctx.errors:
#         errors_out = path_out.parent / f"{path_out.stem}.errors.txt"
#         errors_out.write_text("\n".join(ctx.errors))
#         assert False
