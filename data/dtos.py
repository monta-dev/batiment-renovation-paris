from dataclasses import dataclass


@dataclass
class RenovationTypeDTO:
    type: str
    count: int
    percentage: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            type=data.get("type", "Inconnu"),
            count=data.get("count", 0),
            percentage=data.get("percentage", 0),
        )


@dataclass
class Batiment_renovatedDTO:
    name: str
    total: int
    private_renovated: int
    social_renovated: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", "Inconnu"),
            total=data.get("total", 0),
            private_renovated=data.get("private_renovated", 0),
            social_renovated=data.get("social_renovated", 0),
        )


@dataclass
class Energy_classesDTO:
    className: str
    count: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            className=data.get("className", "Inconnu"),
            count=data.get("count", 0),
        )
