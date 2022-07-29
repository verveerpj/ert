import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from res.enkf.enkf_fs import EnkfFs
from res.enkf.enums import EnkfInitModeEnum
from res.enkf.run_arg import RunArg


@dataclass
class ErtRunContext:
    sim_fs: Optional[EnkfFs] = None
    target_fs: Optional[EnkfFs] = None
    mask: List[bool] = field(default_factory=list)
    paths: List[str] = field(default_factory=list)
    jobnames: List[str] = field(default_factory=list)
    itr: int = 0
    init_mode: EnkfInitModeEnum.INIT_CONDITIONAL = EnkfInitModeEnum.INIT_CONDITIONAL

    def __post_init__(self):
        self.run_id = f"{uuid.uuid4()}:{datetime.now().strftime('%Y-%m-%dT%H%M')}"
        self.run_args = []
        if self.jobnames and self.paths:
            for iens, (job_name, path) in enumerate(zip(self.jobnames, self.paths)):
                self.run_args.append(
                    RunArg(
                        str(self.run_id),
                        self.sim_fs,
                        iens,
                        self.itr,
                        path,
                        job_name,
                    )
                )

    def is_active(self, index: int) -> bool:
        try:
            return self.mask[index]
        except IndexError:
            return False

    def __len__(self):
        return len(self.mask)

    def __getitem__(self, item) -> RunArg:
        return self.run_args[item]

    def __iter__(self) -> RunArg:
        yield from self.run_args

    def __repr__(self):
        return f"ErtRunContext(size = {len(self)})"

    def get_id(self) -> str:
        return self.run_id

    def get_mask(self) -> List[bool]:
        return self.mask

    def get_iter(self) -> int:
        return self.itr

    def get_target_fs(self) -> EnkfFs:
        return self.target_fs

    def get_sim_fs(self) -> EnkfFs:
        return self.sim_fs

    def get_init_mode(self):
        return self.init_mode

    def deactivate_realization(self, realization_nr):
        self.mask[realization_nr] = False
