#!/usr/bin/python3
import hashlib
import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path


PHANTOMJS_VERSION = "2.1.1"
PHANTOMJS_ARCHIVE = f"phantomjs-{PHANTOMJS_VERSION}-linux-x86_64.tar.bz2"
PHANTOMJS_URL = (
    "https://github.com/Medium/phantomjs/releases/download/"
    f"v{PHANTOMJS_VERSION}/{PHANTOMJS_ARCHIVE}"
)
PHANTOMJS_SHA256 = "86dd9a4bf4aee45f1a84c9f61cf1947c1d6dce9b9e8d2a907105da7852460d2f"


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_runtime() -> Path:
    base_dir = Path(__file__).resolve().parent
    runtime_dir = base_dir / ".runtime"
    archive_path = runtime_dir / PHANTOMJS_ARCHIVE
    extract_dir = runtime_dir / PHANTOMJS_ARCHIVE.removesuffix(".tar.bz2")
    binary_path = extract_dir / "bin" / "phantomjs"

    runtime_dir.mkdir(exist_ok=True)

    if binary_path.exists():
        verify_binary(binary_path)
        return binary_path

    with urllib.request.urlopen(PHANTOMJS_URL) as response, archive_path.open("wb") as f:
        shutil.copyfileobj(response, f)

    archive_sha256 = sha256sum(archive_path)
    if archive_sha256 != PHANTOMJS_SHA256:
        raise RuntimeError(
            "phantomjs archive checksum mismatch: "
            f"expected {PHANTOMJS_SHA256}, got {archive_sha256}"
        )

    with tarfile.open(archive_path, "r:bz2") as tar:
        tar.extractall(runtime_dir)

    archive_path.unlink()
    verify_binary(binary_path)
    return binary_path


def verify_binary(binary_path: Path) -> None:
    env = os.environ.copy()
    env.setdefault("OPENSSL_CONF", "/dev/null")
    result = subprocess.run(
        [str(binary_path), "--version"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.stdout.strip() != PHANTOMJS_VERSION:
        raise RuntimeError(
            f"unexpected phantomjs version: expected {PHANTOMJS_VERSION}, got {result.stdout.strip()!r}"
        )


def main() -> None:
    binary_path = ensure_runtime()
    print(binary_path)


if __name__ == "__main__":
    main()
