from datetime import datetime, timedelta
from typing import Optional

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)
from typing_extensions import Self

FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(
        ...,
        alias='from_time',
        examples=[FROM_TIME],
        description='Время начала бронирования'
    )
    to_reserve: datetime = Field(
        ...,
        alias='to_time',
        examples=[TO_TIME],
        description='Время окончания бронирования'
    )

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'from_time': FROM_TIME,
                'to_time': TO_TIME
            }
        }
    )


class ReservationUpdate(ReservationBase):

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            error = (
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
            raise ValueError(error)
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self) -> Self:
        if self.from_reserve >= self.to_reserve:
            error = (
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
            raise ValueError(error)
        return self


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int = Field(
        description='ID переговорной комнаты для бронирования'
    )

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'from_time': FROM_TIME,
                'to_time': TO_TIME,
                'meetingroom_id': 1
            }
        }
    )


class ReservationDB(ReservationBase):
    id: int = Field(
        description='ID бронирования'
    )
    meetingroom_id: int = Field(
        description='ID переговорной комнаты'
    )
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
