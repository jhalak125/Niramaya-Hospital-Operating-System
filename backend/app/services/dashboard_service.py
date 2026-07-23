from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    @staticmethod
    async def get_admin_dashboard():

        total_patients = await DashboardRepository.total_patients()

        total_doctors = await DashboardRepository.total_doctors()

        total_appointments = await DashboardRepository.total_appointments()

        pending_payments = await DashboardRepository.pending_payments()

        total_revenue = await DashboardRepository.total_revenue()

        total_medical_records = await DashboardRepository.total_medical_records()

        total_prescriptions = await DashboardRepository.total_prescriptions()

        total_lab_tests = await DashboardRepository.total_lab_tests()

        total_lab_reports = await DashboardRepository.total_lab_reports()

        return {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "pending_payments": pending_payments,
            "total_revenue": total_revenue,
            "total_medical_records": total_medical_records,
            "total_prescriptions": total_prescriptions,
            "total_lab_tests": total_lab_tests,
            "total_lab_reports": total_lab_reports
        }
    
    @staticmethod
    async def get_doctor_dashboard(doctor_id):

        total_appointments = await DashboardRepository.doctor_total_appointments(
            doctor_id
        )

        completed_appointments = await DashboardRepository.doctor_completed_appointments(
            doctor_id
        )

        pending_appointments = await DashboardRepository.doctor_pending_appointments(
            doctor_id
        )

        prescriptions_written = await DashboardRepository.doctor_prescriptions(
            doctor_id
        )

        lab_tests_ordered = await DashboardRepository.doctor_lab_tests(
            doctor_id
        )

        return {
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "pending_appointments": pending_appointments,
            "prescriptions_written": prescriptions_written,
            "lab_tests_ordered": lab_tests_ordered
        }
    
    @staticmethod
    async def get_patient_dashboard(patient_id):

        total_appointments = await DashboardRepository.patient_total_appointments(
            patient_id
        )

        completed_appointments = await DashboardRepository.patient_completed_appointments(
            patient_id
        )

        pending_appointments = await DashboardRepository.patient_pending_appointments(
            patient_id
        )

        prescriptions = await DashboardRepository.patient_prescriptions(
            patient_id
        )

        lab_reports = await DashboardRepository.patient_lab_reports(
            patient_id
        )

        return {
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "pending_appointments": pending_appointments,
            "prescriptions": prescriptions,
            "lab_reports": lab_reports
        }