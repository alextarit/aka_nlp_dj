from abc import ABC, abstractmethod
from typing import Any

from core.domains import SunoOptions, SunoPayload, SunoRequest


class SunoPreparer(ABC):
    @abstractmethod
    def build(
        self, payload: SunoPayload, options: SunoOptions | dict[str, Any] | None = None
    ) -> SunoRequest: ...


class DefaultSunoPreparer(SunoPreparer):
    def __init__(
        self,
        default_model: str = "V5",
        default_callback: str = "https://example.com/callback",
    ):
        self.default_model = default_model
        self.default_callback = default_callback

    def _coerce_options(
        self, options: SunoOptions | dict[str, Any] | None
    ) -> SunoOptions:
        if isinstance(options, SunoOptions):
            return options
        return SunoOptions.model_validate(options or {})

    def build(
        self, payload: SunoPayload, options: SunoOptions | dict[str, Any] | None = None
    ) -> SunoRequest:
        opts = self._coerce_options(options)
        return opts.to_request(payload, self.default_model, self.default_callback)
