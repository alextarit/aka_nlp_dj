from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field


@dataclass
class UserQuery:
    thread_id: str
    query: str
    feedback: str | None = None


@dataclass
class SunoRequest:
    custom_mode: bool
    instrumental: bool
    model: str
    call_back_url: str
    prompt: str | None = None
    style: str | None = None
    title: str | None = None
    persona_id: str | None = None
    negative_tags: str | None = None
    vocal_gender: str | None = None
    style_weight: float | None = None
    weirdness_constraint: float | None = None
    audio_weight: float | None = None

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "customMode": self.custom_mode,
            "instrumental": self.instrumental,
            "model": self.model,
            "callBackUrl": self.call_back_url,
            "prompt": self.prompt,
            "style": self.style,
            "title": self.title,
            "personaId": self.persona_id,
            "negativeTags": self.negative_tags,
            "vocalGender": self.vocal_gender,
            "styleWeight": self.style_weight,
            "weirdnessConstraint": self.weirdness_constraint,
            "audioWeight": self.audio_weight,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass
class SunoPayload:
    prompt: str
    style: str
    title: str


@dataclass
class SunoTrack:
    title: str
    tags: str
    image: str | None
    play_url: str | None
    download_url: str | None


class SunoOptions(BaseModel):
    custom_mode: bool = True
    instrumental: bool = False
    model: str | None = None
    call_back_url: str | None = None
    callback: str | None = None
    prompt: str | None = None
    style: str | None = None
    title: str | None = None
    persona_id: str | None = None
    negative_tags: str | None = None
    vocal_gender: str | None = None
    style_weight: float | None = None
    weirdness_constraint: float | None = None
    audio_weight: float | None = None

    model_config = {"extra": "ignore"}

    def to_request(
        self, payload: SunoPayload, default_model: str, default_callback: str
    ) -> SunoRequest:
        return SunoRequest(
            custom_mode=self.custom_mode,
            instrumental=self.instrumental,
            model=self.model or default_model,
            call_back_url=self.call_back_url or self.callback or default_callback,
            prompt=self.prompt or payload.prompt,
            style=self.style or payload.style,
            title=self.title or payload.title,
            persona_id=self.persona_id,
            negative_tags=self.negative_tags,
            vocal_gender=self.vocal_gender,
            style_weight=self.style_weight,
            weirdness_constraint=self.weirdness_constraint,
            audio_weight=self.audio_weight,
        )


class SunoExtract(BaseModel):
    title: str = Field(max_length=80)
    style: str
    prompt: str
