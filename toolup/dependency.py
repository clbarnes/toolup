import os
import sys
from pathlib import Path
from warnings import warn

import pip
import toml


__all__ = ["Dependency"]

bin_dir = Path(sys.executable).parent


class Dependency:

    def __init__(self, name=None, install_args=None, entry_points=None):
        self.name = name
        self.install_args = self._handle_install_args(install_args)
        self._handle_missing_name()
        self.entry_points = entry_points or [self.name]

    def _handle_missing_name(self):
        if self.name:
            return

        s = self.install_args[-1]
        first_bracket = s.find("[")
        if first_bracket < 0:
            self.name = s
        else:
            self.name = s[:first_bracket]

    def _handle_install_args(self, install_args):
        if install_args is None:
            if self.name:
                return [self.name]
            else:
                raise ValueError("Must supply at least one of name and install_args")

        if isinstance(install_args, str):
            return install_args.split()
        else:
            return install_args

    def _mangle_path(self, path):
        return Path(os.path.expandvars(path)).expanduser().absolute()

    def install(self, target_dir, delete_existing=True):
        pip.main(["install"] + list(self.install_args))
        target_dir = self._mangle_path(target_dir)

        if not target_dir:
            return

        for entry_point in self.entry_points:
            target_path = target_dir / entry_point

            if target_path.exists():
                if delete_existing:
                    os.remove(target_path)
                else:
                    warn(
                        f"{entry_point} ({self.name}) exists in {target_dir}; skipping (-f to delete)"
                    )
                    continue

            src_path = bin_dir / entry_point

            if not src_path.exists():
                warn(
                    f"{entry_point} ({self.name}) does not exist in {bin_dir}; skipping"
                )
                continue

            os.symlink(src_path, target_path)

    @classmethod
    def install_from_dict(cls, d, delete_existing=True):
        target = Path(d["target"])
        for key, val in d.items():
            if key == "target":
                continue

            Dependency(key, val.get("install_args"), val.get("entry_points")).install(
                target, delete_existing
            )

    @classmethod
    def install_from_config(cls, path, delete_existing=True):
        with open(path) as f:
            config = toml.load(f)

        cls.install_from_dict(config, delete_existing)
