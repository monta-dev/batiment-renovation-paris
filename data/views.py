from django.http import JsonResponse
from data.dtos import *
from data.services.analyse_donnees_pandas import analyse_data_renovationParis

# Instancie une fois (singleton-like)
analyse_service = analyse_data_renovationParis()

def get_energy_classes(request):
    raw_data = analyse_service.get_data_energy_classes()
    adapted_data = [{"className": item["class"], "count": item["count"]} for item in raw_data]
    dtos = [Energy_classesDTO.from_dict(item) for item in adapted_data]
    return JsonResponse([dto.__dict__ for dto in dtos], safe=False)

def get_Renovation_types(request):
    raw_data = analyse_service.get_data_Renovation_types()
    dtos = [RenovationTypeDTO.from_dict(item) for item in raw_data]
    return JsonResponse([dto.__dict__ for dto in dtos], safe=False)

def get_Batiment_renovates(request):
    raw_data = analyse_service.get_data_Batiment_renovates()
    adapted_data = [
        {
            "name": item["name"],
            "total": item["total"],
            "private_renovated": item["private_renovated"],
            "social_renovated": item["social_renovated"],
        }
        for item in raw_data
    ]
    dtos = [Batiment_renovatedDTO.from_dict(item) for item in adapted_data]
    return JsonResponse([dto.__dict__ for dto in dtos], safe=False)