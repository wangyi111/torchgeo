import os
from pathlib import Path
import shutil
from typing import Generator

import pytest
from pytest import MonkeyPatch
import torch
from torch.utils.data import ConcatDataset

from torchgeo.datasets import COWCCounting, COWCDetection
import torchgeo.datasets.cowc
from torchgeo.datasets.cowc import _COWC
from torchgeo.transforms import Identity


def download_url(url: str, root: str, **kwargs: str) -> None:
    shutil.copy(url, root)


class TestCOWC:
    def test_not_implemented(self) -> None:
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            _COWC()  # type: ignore[abstract]


class TestCOWCCounting:
    @pytest.fixture
    def dataset(
        self, monkeypatch: Generator[MonkeyPatch, None, None], tmp_path: Path
    ) -> _COWC:
        monkeypatch.setattr(  # type: ignore[attr-defined]
            torchgeo.datasets.cowc, "download_url", download_url
        )
        base_url = os.path.join("tests", "data", "cowc_counting") + os.sep
        monkeypatch.setattr(  # type: ignore[attr-defined]
            COWCCounting, "base_url", base_url
        )
        md5s = [
            "fd44e49492d63e9050e80d2157813263",
            "c44f6d709076562116b1a445ea91a228",
            "405d33d745a850c3a0c5e84713c5fd26",
            "3bd99854a243218fe40ea11dd552887f",
            "5648852da4212876502c7a454e70ce8e",
            "f91460b2e7dcfbad53f5f5ede05f2da2",
            "9d26d6c4bca7c6e932b0a6340647af8b",
            "ccc18c4ac29a13ad2bcb293ff6be69fe",
        ]
        monkeypatch.setattr(COWCCounting, "md5s", md5s)  # type: ignore[attr-defined]
        (tmp_path / "cowc_counting").mkdir()
        root = str(tmp_path)
        split = "train"
        transforms = Identity()
        return COWCCounting(root, split, transforms, download=True, checksum=True)

    def test_getitem(self, dataset: _COWC) -> None:
        x = dataset[0]
        assert isinstance(x, dict)
        assert isinstance(x["image"], torch.Tensor)
        assert isinstance(x["label"], torch.Tensor)

    def test_len(self, dataset: _COWC) -> None:
        assert len(dataset) == 12

    def test_add(self, dataset: _COWC) -> None:
        ds = dataset + dataset
        assert isinstance(ds, ConcatDataset)
        assert len(ds) == 24

    def test_already_downloaded(self, dataset: _COWC) -> None:
        COWCCounting(root=dataset.root, download=True)

    def test_out_of_bounds(self, dataset: _COWC) -> None:
        with pytest.raises(IndexError):
            dataset[12]

    def test_invalid_split(self) -> None:
        with pytest.raises(AssertionError):
            COWCCounting(split="foo")

    def test_not_downloaded(self, tmp_path: Path) -> None:
        with pytest.raises(RuntimeError, match="Dataset not found or corrupted."):
            COWCCounting(str(tmp_path))


class TestCOWCDetection:
    @pytest.fixture
    def dataset(
        self, monkeypatch: Generator[MonkeyPatch, None, None], tmp_path: Path
    ) -> _COWC:
        monkeypatch.setattr(  # type: ignore[attr-defined]
            torchgeo.datasets.cowc, "download_url", download_url
        )
        base_url = os.path.join("tests", "data", "cowc_detection") + os.sep
        monkeypatch.setattr(  # type: ignore[attr-defined]
            COWCDetection, "base_url", base_url
        )
        md5s = [
            "dd8725ab4dd13cf0cc674213bb09e068",
            "37619fce32dbca46d2fd96716cfb2d5e",
            "405d33d745a850c3a0c5e84713c5fd26",
            "3bd99854a243218fe40ea11dd552887f",
            "5648852da4212876502c7a454e70ce8e",
            "f91460b2e7dcfbad53f5f5ede05f2da2",
            "9d26d6c4bca7c6e932b0a6340647af8b",
            "ccc18c4ac29a13ad2bcb293ff6be69fe",
        ]
        monkeypatch.setattr(COWCDetection, "md5s", md5s)  # type: ignore[attr-defined]
        (tmp_path / "cowc_detection").mkdir()
        root = str(tmp_path)
        split = "train"
        transforms = Identity()
        return COWCDetection(root, split, transforms, download=True, checksum=True)

    def test_getitem(self, dataset: _COWC) -> None:
        x = dataset[0]
        assert isinstance(x, dict)
        assert isinstance(x["image"], torch.Tensor)
        assert isinstance(x["label"], torch.Tensor)

    def test_len(self, dataset: _COWC) -> None:
        assert len(dataset) == 12

    def test_add(self, dataset: _COWC) -> None:
        ds = dataset + dataset
        assert isinstance(ds, ConcatDataset)
        assert len(ds) == 24

    def test_already_downloaded(self, dataset: _COWC) -> None:
        COWCDetection(root=dataset.root, download=True)

    def test_out_of_bounds(self, dataset: _COWC) -> None:
        with pytest.raises(IndexError):
            dataset[12]

    def test_invalid_split(self) -> None:
        with pytest.raises(AssertionError):
            COWCDetection(split="foo")

    def test_not_downloaded(self, tmp_path: Path) -> None:
        with pytest.raises(RuntimeError, match="Dataset not found or corrupted."):
            COWCDetection(str(tmp_path))