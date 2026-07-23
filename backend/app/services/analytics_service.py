from app.repositories.analytics_repository import AnalyticsRepository


async def get_dashboard_summary():

    return await AnalyticsRepository.dashboard_summary()

async def get_revenue_analytics():

    return await AnalyticsRepository.revenue_analytics()

async def get_top_doctors():

    return await AnalyticsRepository.top_doctors()

async def get_appointment_analytics():

    return await AnalyticsRepository.appointment_analytics()

async def get_lab_test_analytics():

    return await AnalyticsRepository.lab_test_analytics()

async def get_payment_analytics():

    return await AnalyticsRepository.payment_analytics()