"""Class to interact with pbs manifest."""

import json
import logging
import shutil
from collections.abc import Iterator, Sequence
from datetime import date
from pathlib import Path
from types import TracebackType
from typing import Any

from pbs_parse.pbs_2022_01.models import manifest as M
from pbs_parse.pbs_2022_01.models.expanded import EXPANDED_TRIP_SERIALIZER, ExpandedTrip
from pbs_parse.pbs_2022_01.models.expanded_validation import (
    EXPANDED_VALIDATION_SERIALIZER,
    ExpandedValidation,
)
from pbs_parse.pbs_2022_01.models.page_lines import PAGE_LINES_SERIALIZER, PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import (
    STRUCTURED_TRIP_SERIALIZER,
    StructuredTrip,
)
from pbs_parse.pbs_2022_01.models.structured_validation import (
    STRUCTURED_VALIDATION_SERIALIZER,
    StructuredValidation,
)
from pbs_parse.pbs_2022_01.models.trip_lines import TRIP_LINES_SERIALIZER, TripLines
from pbs_parse.snippets.file.check_file import check_file

from .exceptions import NotInManifestError, StoreOperationError, UnableToLoadError

logger = logging.getLogger(__name__)


class StoreManager:
    """Actions for managing the data store."""

    def __init__(self, manifest_directory: Path) -> None:
        """Init manager and open data store."""
        self.manifest_directory = manifest_directory
        self.manifest_path = self.manifest_directory / self.manifest_file_name()
        try:
            with open(self.manifest_path) as file_in:
                manifest = json.load(file_in)
        except Exception as e:
            raise UnableToLoadError(
                f"Unable to find Pbs Store `{self.manifest_file_name()}` at `{manifest_directory}`"
            ) from e
        self.manifest: M.BidPeriodManifest = manifest
        for key in ("name", "effective_from", "effective_to", "bases"):
            if not key in self.manifest.keys():
                raise NotInManifestError(
                    "Loaded manifest does not have basic keys. Is the the right location?"
                )
        self.read_only = True

    def __enter__(self):
        """Context manager."""
        self.read_only = False
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
        self.read_only = True
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

    def clean(self, base: str, file_types: Sequence[M.FileTypes]):
        """Remove files of these types from store."""

    def get_file_info_by_type(
        self, base: str, file_type: M.FileTypes
    ) -> Sequence[M.FileInfo]:
        """Get all the files of a certain type."""
        files: list[M.FileInfo] = []
        base_data = self.manifest["bases"].get(base, None)
        if base_data is None:
            raise NotInManifestError(f"Base not in manifest. {base=}")
        for file in base_data["files"].values():
            if file["type"] == file_type:
                files.append(file)
        return files

    def get_file_info_by_id(self, base: str, file_id: str) -> M.FileInfo:
        """get_file_by_id.

        Args:
            base (str): _description_
            file_id (str): _description_

        Returns:
            M.FileInfo|None: _description_
        """
        base_data = self.manifest["bases"].get(base, None)
        if base_data is None:
            raise NotInManifestError(f"Base not in manifest. {base=}")
        info = base_data["files"].get(file_id, None)
        if info is None:
            raise NotInManifestError(f"Resource not in manifest. {base=}, {file_id=}")
        return info

    # def get_effective_dates(self) -> tuple[date, date]:
    #     """get_effective_dates _summary_.

    #     Returns:
    #         tuple[date, date]: (from,to)
    #     """
    #     return (
    #         date.fromisoformat(self.manifest["effective_from"]),
    #         date.fromisoformat(self.manifest["effective_to"]),
    #     )

    # def get_bases(self) -> list[str]:
    #     """Get a list of base keys."""
    #     return list(self.manifest["bases"].keys())

    # def get_name(self) -> str:
    #     """Get store name."""
    #     return self.manifest["name"]

    def create_base_bid(self, source_pdf: Path, source_txt: Path, name: str):
        """Create a base bid, and copy the pdf and txt files into store."""
        if self.manifest["bases"].get(name, None) is not None:
            raise StoreOperationError(
                f"Cannot create new base, it already exists. {name=}"
            )
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
            raise UnableToLoadError(f"Path to pdf file is not valid. {source_pdf=}")
        if not source_txt.is_file():
            raise UnableToLoadError(f"Path to txt file is not valid. {source_txt=}")

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
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        exists = self.manifest["bases"][base]["files"].get(info["key"], None)
        if exists:
            msg = f"Overwriting existing record for base {base} existing={exists!r} new={info!r}"
            err = ValueError(msg)
            logger.error(err)
            raise err
        self.manifest["bases"][base]["files"][info["key"]] = info

    def save_page_lines(
        self, base: str, page: PageLines, overwrite: bool = False
    ) -> Path:
        """Save a PageLines in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        page_info = M.FileInfo(
            key=page.uuid,
            type=M.FileTypes.SPLIT_PAGE,
            file_path=f"{base}/pages/{page.default_file_name()}",
        )
        path_out = self.manifest_directory / page_info["file_path"]
        PAGE_LINES_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=page, overwrite=overwrite
        )
        self.record_file(base=base, info=page_info)
        return path_out

    def load_page_lines(self, base: str, uuid: str) -> PageLines:
        """Load a PageLines from the store.

        Args:
            base (str): _description_
            uuid (str): _description_

        Returns:
            PageLines: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = PAGE_LINES_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make PageLines from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def load_all_page_lines(self, base: str) -> Iterator[PageLines]:
        """load_all_page_lines.

        Args:
            base (str): _description_

        Yields:
            Iterator[PageLines]: _description_
        """
        page_infos = self.get_file_info_by_type(
            base=base, file_type=M.FileTypes.SPLIT_PAGE
        )
        for page_info in page_infos:
            yield self.load_page_lines(base=base, uuid=page_info["key"])

    def save_trip_lines(
        self,
        base: str,
        trip: TripLines,
        overwrite: bool = False,
    ):
        """Save TripLines in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=trip.uuid,
            type=M.FileTypes.SPLIT_TRIP,
            file_path=f"{base}/trip_lines/{trip.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        TRIP_LINES_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=trip, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def load_trip_lines(self, base: str, uuid: str) -> TripLines:
        """Load a TripLines from the store.

        Args:
            base (str): _description_
            uuid (str): _description_

        Returns:
            TripLines: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = TRIP_LINES_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make TripLines from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def load_all_trip_lines(self, base: str) -> Iterator[TripLines]:
        """load_all_trip_lines.

        Args:
            base (str): _description_

        Yields:
            Iterator[TripLines]: _description_
        """
        trip_infos = self.get_file_info_by_type(
            base=base, file_type=M.FileTypes.SPLIT_TRIP
        )
        for page_info in trip_infos:
            yield self.load_trip_lines(base=base, uuid=page_info["key"])

    def save_parsed_trip(
        self, base: str, parsed: ParsedTrip, overwrite: bool = False
    ) -> Path:
        """Save a ParsedTrip in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=parsed.uuid,
            type=M.FileTypes.PARSED_TRIP,
            file_path=f"{base}/parsed/{parsed.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        PARSED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=parsed, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def load_parsed_trip(self, base: str, uuid: str) -> ParsedTrip:
        """Load a ParsedTrip from the store.

        Args:
            base (str): _description_
            uuid (str): _description_

        Returns:
            ParsedTrip: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            logger.info(data)
            value = PARSED_TRIP_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make ParsedTrip from json, but there was an error. {base=}, {uuid=} error={e}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def load_all_parsed_trips(self, base: str) -> Iterator[ParsedTrip]:
        """load_all_parsed_trips.

        Args:
            base (str): _description_

        Yields:
            Iterator[ParsedTrip]: _description_
        """
        trip_infos = self.get_file_info_by_type(
            base=base, file_type=M.FileTypes.PARSED_TRIP
        )
        for page_info in trip_infos:
            yield self.load_parsed_trip(base=base, uuid=page_info["key"])

    def load_resource(self, base: str, uuid: str) -> dict[str, Any]:
        """Load a json object from the store."""
        file_info = self.get_file_info_by_id(base=base, file_id=uuid)
        path_in = self.manifest_directory / file_info["file_path"]
        try:
            with open(path_in) as file_in:
                value = json.load(file_in)
            return value
        except Exception as e:
            msg = f"Unable to load json resource. {base=}, {uuid=}, {file_info=!r}, {path_in=!r}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def save_parsed_prior_month_trip(
        self, base: str, parsed: ParsedTrip, overwrite: bool = False
    ) -> Path:
        """Save a ParsedTrip in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=parsed.uuid,
            type=M.FileTypes.PARSED_PRIOR_MONTH_TRIP,
            file_path=f"{base}/parsed_prior/{parsed.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        PARSED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=parsed, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def save_structured_trip(
        self, base: str, structured: StructuredTrip, overwrite: bool = False
    ) -> Path:
        """Save a StructuredTrip in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=structured.uuid,
            type=M.FileTypes.STRUCTURED_TRIP,
            file_path=f"{base}/structured/{structured.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        STRUCTURED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=structured, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def load_structured_trip(self, base: str, uuid: str) -> StructuredTrip:
        """Load a StructuredTrip from the store.

        Args:
            base (str): _description_
            uuid (str): _description_

        Returns:
            StructuredTrip: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = STRUCTURED_TRIP_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make StructuredTrip from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def load_all_structured_trips(self, base: str) -> Iterator[StructuredTrip]:
        """load_all_structured_trips.

        Args:
            base (str): _description_

        Yields:
            Iterator[StructuredTrip]: _description_
        """
        trip_infos = self.get_file_info_by_type(
            base=base, file_type=M.FileTypes.STRUCTURED_TRIP
        )
        for page_info in trip_infos:
            yield self.load_structured_trip(base=base, uuid=page_info["key"])

    def load_structured_trip_validation(
        self, base: str, uuid: str
    ) -> StructuredValidation:
        """load_structured_trip_validation.

        Args:
            base (str): _description_
            uuid (str): _description_

        Raises:
            UnableToLoadError: _description_

        Returns:
            StructuredValidation: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = STRUCTURED_VALIDATION_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make StructuredValidation from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def save_structured_trip_validation_error(
        self, base: str, validation_model: StructuredValidation, overwrite: bool = False
    ) -> Path:
        """Fix type of error."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=validation_model.uuid,
            type=M.FileTypes.STRUCTURED_TRIP_VALIDATION,
            file_path=f"{base}/structured/errors/{validation_model.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        STRUCTURED_VALIDATION_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=validation_model, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def save_expanded_trip(
        self, base: str, expanded: ExpandedTrip, overwrite: bool = False
    ) -> Path:
        """Save an ExpandedTrip in the store."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=expanded.uuid,
            type=M.FileTypes.EXPANDED_TRIP,
            file_path=f"{base}/expanded/{expanded.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        EXPANDED_TRIP_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=expanded, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def load_expanded_trip(self, base: str, uuid: str) -> ExpandedTrip:
        """Load a ExpandedTrip from the store.

        Args:
            base (str): _description_
            uuid (str): _description_

        Returns:
            ExpandedTrip: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = EXPANDED_TRIP_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make ExpandedTrip from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    def load_all_expanded_trips(self, base: str) -> Iterator[ExpandedTrip]:
        """load_all_expanded_trips.

        Args:
            base (str): _description_

        Yields:
            Iterator[ExpandedTrip]: _description_
        """
        trip_infos = self.get_file_info_by_type(
            base=base, file_type=M.FileTypes.EXPANDED_TRIP
        )
        for page_info in trip_infos:
            yield self.load_expanded_trip(base=base, uuid=page_info["key"])

    def save_expanded_trip_validation_error(
        self, base: str, validation_model: ExpandedValidation, overwrite: bool = False
    ) -> Path:
        """Fix type of error."""
        if self.read_only:
            raise StoreOperationError(
                "Store is opened in read-only mode. No changes allowed."
            )
        trip_info = M.FileInfo(
            key=validation_model.uuid,
            type=M.FileTypes.EXPANDED_TRIP_VALIDATION,
            file_path=f"{base}/expanded/errors/{validation_model.default_file_name()}",
        )
        path_out = self.manifest_directory / trip_info["file_path"]
        EXPANDED_VALIDATION_SERIALIZER.save_as_json(
            path_out=path_out, complex_obj=validation_model, overwrite=overwrite
        )
        self.record_file(base=base, info=trip_info)
        return path_out

    def load_expanded_trip_validation(self, base: str, uuid: str) -> ExpandedValidation:
        """load_expanded_trip_validation.

        Args:
            base (str): _description_
            uuid (str): _description_

        Raises:
            UnableToLoadError: _description_

        Returns:
            ExpandedValidation: _description_
        """
        data = self.load_resource(base=base, uuid=uuid)
        try:
            value = EXPANDED_VALIDATION_SERIALIZER.from_simple(data)  # type: ignore
            return value
        except Exception as e:
            msg = f"Tried to make ExpandedValidation from json, but there was an error. {base=}, {uuid=}"
            logger.exception(msg)
            raise UnableToLoadError(msg) from e

    # def report_errors(self):
    #     """Report errors."""
    #     pass
