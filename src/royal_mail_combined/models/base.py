from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RMBaseModel(BaseModel):
    model_config = ConfigDict(
        # json_encoders={
        #     time: lambda v: v.strftime("%H:%M"),
        #     date: lambda v: v.strftime("%d/%m/%Y"),
        # },
        alias_generator=AliasGenerator(
            alias=to_camel,
        ),
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )
