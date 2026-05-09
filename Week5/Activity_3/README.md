# Clinic System Workflow - Activity Diagram

![Clinic Activity Diagram](Week5/Activity_3/Clinic System.png)

## Purpose
This activity diagram models the comprehensive operational workflow of a clinic system. It captures the end-to-end patient journey, starting from the initial appointment request through to the final medication dispensing. The diagram utilizes vertical swimlanes to clearly separate the responsibilities of administrative staff, medical professionals, and the patient, while also illustrating both the "happy path" (successful consultation) and alternative flows (scheduling conflicts leading to cancellations and refunds).

## Key Actors (Swimlanes)
- **Patients:** The primary users who initiate appointment requests, attend the clinic, handle various billing payments, and order their prescribed medications.
- **Reception:** The administrative hub responsible for reviewing applications, managing the calendar, processing booking fees, registering visiting patients, and handling refunds if a doctor is unavailable.
- **Doctors:** The medical staff tasked with managing their timetables, conducting patient examinations, diagnosing conditions, and prescribing medications.
- **Pharmacy:** The dispensary unit responsible for verifying medical prescriptions and handing over the final medication to the patient.

## Core Process Flows
1. **Appointment & Scheduling:** The process begins with a patient applying for an appointment. Reception coordinates the scheduling and fee processing. A critical decision node occurs when the doctor checks their timetable:
   - *If unavailable:* The appointment is cancelled, and a refund is arranged for the patient.
   - *If available:* The appointment is officially confirmed.
2. **Consultation Phase:** Upon the patient's arrival at the clinic, reception registers them. The doctor then creates a case, examines the patient, makes a diagnosis, and issues a prescription.
3. **Billing & Pharmacy:** Following the consultation, the patient pays the medical bill. They then proceed to order medication, which the pharmacy checks and dispenses. The process concludes once the patient pays the final medication bill.
