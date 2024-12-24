"""Class to interact with pbs manifest."""

import json
import shutil
from collections.abc import Iterable, Sequence
from datetime import date
from pathlib import Path
from types import TracebackType

from pbs_parse.pbs_2022_01.models import manifest as M
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import StructuredTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.snippets.file.check_file import check_file


class StoreManager:
    """Actions for managing the data store."""

    def __init__(self, manifest_directory: Path) -> None:
        """Init manager and open data store."""
        self.manifest_directory = manifest_directory
        self.manifest_path = self.manifest_directory / self.manifest_file_name()
        with open(self.manifest_path) as file_in:
            manifest = json.load(file_in)
        self.manifest: M.BidPeriodManifest = manifest

    def __enter__(self):
        """Context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Context manager exit."""
        if exc_val is None:
            self.save_manifest()
        return False

    @classmethod
    def manifest_file_name(cls) -> str:
        """The file name for a pbs manifest."""
        return "pbs-manifest.json"

    @classmethod
    def init_manifest(
        cls,
        manifest_directory: Path,
        name: str,
        effective_from: date,
        effective_to: date,
    ):
        """Create a new pbs manifest in a directory."""
        manifest_path = manifest_directory / cls.manifest_file_name()
        check_file(manifest_path)
        bid_period_manifest = M.BidPeriodManifest(
            name=name,
            effective_from=effective_from.isoformat(),
            effective_to=effective_to.isoformat(),
            bases={},
        )
        manifest_path.write_text(json.dumps(bid_period_manifest, indent=1))

    def save_manifest(self):
        """Replace manifest file with current data."""
        self.manifest_path.unlink()
        self.manifest_path.write_text(json.dumps(self.manifest, indent=1))

    def clean(self, file_type: Sequence[M.FileTypes]):
        """Remove files of these types from store."""

    def get_files(self, base: str, file_type: M.FileTypes) -> Sequence[M.FileInfo]:
        """Get all the files of a certain type."""
        files: list[M.FileInfo] = []
        base_data = self.manifest["bases"].get(base, None)
        if base_data is None:
            raise ValueError(f"Base not in store. {base=}")
        for file in base_data["files"].values():
            if file["type"] == file_type:
                files.append(file)
        return files

    def create_base_bid(self, source_pdf: Path, source_txt: Path, name: str):
        """Create a base bid, and copy the pdf and txt files into store."""
        if self.manifest["bases"].get(name, None) is not None:
            raise ValueError(f"Cannot create new base, it already exists. {name=}")
        base = M.Base(base_name=name, files={})
        pdf_info = M.FileInfo(
            key=M.FileTypes.PDF_PACKAGE,
            type=M.FileTypes.PDF_PACKAGE,
            file_path=f"{name}/source/{source_pdf.name}",
        )
        txt_info = M.FileInfo(
            key=M.FileTypes.TXT_PACKAGE,
            type=M.FileTypes.TXT_PACKAGE,
            file_path=f"{name}/source/{source_txt.name}",
        )
        if not source_pdf.is_file():
            raise ValueError(f"Path to pdf file is not valid. {source_pdf=}")
        if not source_txt.is_file():
            raise ValueError(f"Path to txt file is not valid. {source_txt=}")

        pdf_dest_path = self.manifest_directory / pdf_info["file_path"]
        check_file(path_out=pdf_dest_path)
        shutil.copy(source_pdf, pdf_dest_path)
        base["files"][pdf_info["key"]] = pdf_info
        self.manifest["bases"][base["base_name"]] = base

        txt_dest_path = self.manifest_directory / txt_info["file_path"]
        check_file(path_out=txt_dest_path)
        shutil.copy(source_txt, txt_dest_path)
        base["files"][txt_info["key"]] = txt_info
        self.manifest["bases"][base["base_name"]] = base

    def record_file(self, base: str, info: M.FileInfo):
        """Record file info in manifest."""
        self.manifest["bases"][base]["files"][info["key"]] = info

    def save_page_lines(
        self, base: str, pages: Iterable[PageLines], overwrite: bool = False
    ) -> int:
        """Save a PageLines in the store."""
        idx = 0
        for idx, page in enumerate(pages, start=1):
            file_name = f"page_{idx}_{page.uuid}.json"
            page_info = M.FileInfo(
                key=page.uuid,
                type=M.FileTypes.SPLIT_PAGE,
                file_path=f"{base}/pages/{file_name}",
            )
            path_out = self.manifest_directory / page_info["file_path"]
            PAGE_LINES_SERIALIZER.save_as_json(
                path_out=path_out, complex_obj=page, overwrite=overwrite
            )
            self.record_file(base=base, info=page_info)
        return idx

    def save_trip_lines(
        self,
        base: str,
        trips: Iterable[TripLines],
        page: int = 0,
        overwrite: bool = False,
    ):
        """Save TripLines in the store."""
        idx = 0
        for idx, trip in enumerate(trips, start=1):
            file_name = f"page_{page}_trip_{idx}_{trip.uuid}.json"
            trip_info = M.FileInfo(
                key=trip.uuid,
                type=M.FileTypes.SPLIT_TRIP,
                file_path=f"{base}/trips/{file_name}",
            )
            path_out = self.manifest_directory / trip_info["file_path"]
            TRIP_LINES_SERIALIZER.save_as_json(
                path_out=path_out, complex_obj=trip, overwrite=overwrite
            )
            self.record_file(base=base, info=trip_info)
        return idx

    def save_parsed_trip(
        self, base: str, parsed: Iterable[ParsedTrip], overwrite: bool = False
    ):
        """Save a ParsedTrip in the store."""

    def save_structured_trip(
        self, base: str, structured: Iterable[StructuredTrip], overwrite: bool = False
    ):
        """Save a StructuredTrip in the store."""

    def save_expanded_trip(
        self, base: str, expanded: Iterable[ExpandedTrip], overwrite: bool = False
    ):
        """Save an ExpandedTrip in the store."""
