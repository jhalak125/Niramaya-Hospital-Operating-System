from fastapi import FastAPI
import os
from app.database.database import db
from app.routers.auth_router import router as auth_router
from app.routers.patient_router import router as patient_router
from app.routers.appointment_router import router as appointment_router
from app.routers.doctor_router import router as doctor_router
from app.routers.medical_record_router import router as medical_record_router
from app.routers.prescription_router import router as prescription_router
from app.routers.billing_router import router as billing_router
from app.routers.payment_router import router as payment_router
from app.routers.test_router import router as test_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.ai_router import router as ai_router
from app.routers.lab_test_router import router as lab_test_router
from app.routers.lab_report_router import router as lab_report_router
from app.routers.notification_router import router as notification_router
from app.routers.analytics_router import router as analytics_router
from app.routers.audit_log_router import router as audit_log_router
from app.routers.vaidya_ai_router import router as vaidya_ai_router
from app.middleware.response_middleware import response_wrapper
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Niramaya",
    description="AI-powered Hospital Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware(
    "http"
)(response_wrapper)

app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)


app.add_exception_handler(
    Exception,
    global_exception_handler
)

app.include_router(
    vaidya_ai_router
)

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(doctor_router)
app.include_router(medical_record_router)
app.include_router(prescription_router)
app.include_router(billing_router)
app.include_router(payment_router)
app.include_router(test_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(lab_test_router)
app.include_router(lab_report_router)
app.include_router(notification_router)
app.include_router(audit_log_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    collections = await db.list_collection_names()

    return {
        "message": "Welcome to MediFlow",
        "version": "1.0.2-dynamic-category-fix",
        "database": "Connected",
        "collections": collections
    }