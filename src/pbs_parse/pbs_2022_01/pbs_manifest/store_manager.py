"""Class to interact with pbs manifest."""

import json
import logging
import shutil
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from types import TracebackType
from typing import Any

from pbs_parse.pbs_2022_01.models import manifest as M
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

    # def report_errors(self):
    #     """Report errors."""
    #     pass
