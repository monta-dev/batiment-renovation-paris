from django.shortcuts import render
from data.dtos import *
from django.http import JsonResponse


# Create your views here.
def get_energy_classes(request):
    raw_data = [{"className": "A", "count": 1500}, {"className": "B", "count": 3200}]
    dtos = []

    for item in raw_data:
        dtos.append(Energy_classesDTO.from_dict(item))

    data_json = [dto.__dict__ for dto in dtos]
    # print("data_json: ", data_json)

    return JsonResponse(data_json, safe=False)


def get_Renovation_types(request):
    RAW_DATA_TYPES = [
        {"type": "Isolation Thermique", "count": 12500, "percentage": 35},
        {"type": "Chauffage / EnR", "count": 8900, "percentage": 25},
        # ...
    ]
    dtos = [RenovationTypeDTO.from_dict(item) for item in RAW_DATA_TYPES]

    data_json = [dto.__dict__ for dto in dtos]
    # print("data_json: ", data_json)

    return JsonResponse(data_json, safe=False)


def get_Batiment_renovates(request):
    RAW_DATA_DISTRICTS = [
        {
            "name": "1er",
            "total": 41000,
            "renovated": 15400,
            "private": 10000,
            "social": 5400,
        },
        {
            "name": "2e",
            "total": 49000,
            "renovated": 19500,
            "private": 12000,
            "social": 7500,
        },
    ]

    data_json = [
        Batiment_renovatedDTO.from_dict(item).__dict__ for item in RAW_DATA_DISTRICTS
    ]

    return JsonResponse(data_json, safe=False)
