"""File-operation utilities (modern API)."""

import logging
import os
import shutil

from .exceptions import FileOperationError

logger = logging.getLogger(__name__)


def move_file(
    current_file_path: str,
    new_name: str,
    processed_dir: str = "ot_procesados",
) -> str:
    """Move *current_file_path* into a *processed_dir* sub-directory.

    The file is placed under its original parent and renamed to *new_name*.

    Args:
        current_file_path: Absolute or relative path to the source file.
        new_name: The desired filename (not full path) at the destination.
        processed_dir: Name of the sub-directory created inside the source
            file's parent directory.

    Returns:
        The full destination path.

    Raises:
        FileOperationError: If the source file does not exist, the destination
            is a directory, or the move fails for any other reason.

    """
    parent = os.path.dirname(current_file_path)
    destination_folder = os.path.join(parent, processed_dir)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        logger.info("Created destination folder: %s", destination_folder)

    new_file_path = os.path.join(destination_folder, new_name)

    if os.path.isdir(new_file_path):
        logger.error(
            "Destination '%s' is a directory; cannot overwrite with a file.",
            new_file_path,
        )
        raise FileOperationError(
            f"Destination '{new_file_path}' is a directory"
        )

    try:
        shutil.move(current_file_path, new_file_path)
        logger.info(
            "Moved '%s' -> '%s'",
            os.path.basename(current_file_path),
            new_file_path,
        )
        return new_file_path
    except FileNotFoundError as exc:
        logger.error("Source file not found: %s", current_file_path)
        raise FileOperationError(
            f"Source file not found: {current_file_path}"
        ) from exc
    except shutil.Error as exc:
        logger.error("Error moving file: %s", exc)
        raise FileOperationError(f"Error moving file: {exc}") from exc
    except OSError as exc:
        logger.error("OS error during move: %s", exc)
        raise FileOperationError(f"OS error during move: {exc}") from exc
