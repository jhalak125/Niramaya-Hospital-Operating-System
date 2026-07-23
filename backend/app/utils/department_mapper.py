def map_department(department: str):

    if not department:
        return None

    department = department.lower()

    if "cardio" in department:
        return "Cardiology"

    if "heart" in department:
        return "Cardiology"

    if "emergency" in department:
        return "Cardiology"

    if "er" in department:
        return "Cardiology"

    if "neurology" in department:
        return "Neurology"

    if "brain" in department:
        return "Neurology"

    if "orthopedic" in department:
        return "Orthopedics"

    if "bone" in department:
        return "Orthopedics"

    if "child" in department or "pediatric" in department:
        return "Pediatrics"

    if "skin" in department or "dermatology" in department:
        return "Dermatology"

    if "eye" in department or "ophthalmology" in department:
        return "Ophthalmology"

    return department.title()