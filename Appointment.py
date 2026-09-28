"""
We are building the back-end for a clinic appointment management system.
The system tracks doctors and appointments.

Definitions:
* A "doctor" has: doctor_id, name.
* An "appointment" has: appointment_id, doctor_id, patient_id,
  duration_minutes, status, appointment_type.
* AppointmentStatus is one of: SCHEDULED, COMPLETED, CANCELLED, NO_SHOW.
* AppointmentType is one of: CONSULTATION, FOLLOWUP, EMERGENCY.
* "ClinicManager" manages doctors, appointments, and provides statistics.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for ClinicManager is not passing due to a bug in the code.
     Make the necessary changes to ClinicManager to fix the bug.
"""
"""
We are extending the platform to report on appointment durations by type.

Recall that each Appointment carries an appointment_type, one of
CONSULTATION, FOLLOWUP, EMERGENCY.

Add a new function to the ClinicManager class:

2) The get_average_appointment_duration_by_type function should return a
   dictionary mapping each appointment type (CONSULTATION, FOLLOWUP,
   EMERGENCY) to the doctor's average appointment duration in minutes for
   that type. Only appointments with a COMPLETED status should be counted;
   ignore appointments with any other status. Only appointment types the
   doctor has at least one completed appointment for should appear in the
   dictionary. If the doctor has no completed appointments at all, return
   an empty dictionary.

To assist you in testing this new function, we have provided the
test_get_average_appointment_duration_by_type test.
"""
import unittest
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class AppointmentType(Enum):
    CONSULTATION = "CONSULTATION"
    FOLLOWUP = "FOLLOWUP"
    EMERGENCY = "EMERGENCY"


class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name


class Appointment:
    def __init__(
        self,
        appointment_id,
        doctor_id,
        patient_id,
        duration_minutes,
        status,
        appointment_type,
    ):
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.duration_minutes = duration_minutes
        self.status = status
        self.appointment_type = appointment_type


class AppointmentStats:
    def __init__(self, total_appointments, completed_appointments, no_show_rate):
        self.total_appointments = total_appointments
        self.completed_appointments = completed_appointments
        self.no_show_rate = no_show_rate


class ClinicManager:
    def __init__(self):
        self.doctors = {}
        self.appointments = []

    def add_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor

    def add_appointment(self, appointment):
        if appointment.doctor_id not in self.doctors:
            return

        self.appointments.append(appointment)

    def get_appointment_statistics(self):
        total = len(self.appointments)

        completed = sum(
            1
            for appointment in self.appointments
            if appointment.status == AppointmentStatus.COMPLETED
        )

        no_shows = sum(
            1
            for appointment in self.appointments
            if appointment.status == AppointmentStatus.NO_SHOW
        )

        no_show_rate = no_shows / total if total > 0 else 0.0

        return AppointmentStats(
            total,
            completed,
            no_show_rate,
        )

    def get_average_appointment_duration_by_type(self, doctor_id):
        if doctor_id not in self.doctors:
            return {}

        durations_by_type = {}

        for appointment in self.appointments:
            if (
                appointment.doctor_id == doctor_id
                and appointment.status == AppointmentStatus.COMPLETED
            ):
                appointment_type = appointment.appointment_type

                if appointment_type not in durations_by_type:
                    durations_by_type[appointment_type] = []

                durations_by_type[appointment_type].append(
                    appointment.duration_minutes
                )

        averages = {}

        for appointment_type, durations in durations_by_type.items():
            averages[appointment_type] = sum(durations) / len(durations)

        return averages


class TestSuite(unittest.TestCase):

    def test_get_appointment_statistics(self):
        print("Running test_get_appointment_statistics")

        cm = ClinicManager()
        cm.add_doctor(Doctor(10, "dr_smith"))

        cm.add_appointment(
            Appointment(
                1,
                10,
                100,
                30,
                AppointmentStatus.COMPLETED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                2,
                10,
                101,
                45,
                AppointmentStatus.COMPLETED,
                AppointmentType.FOLLOWUP,
            )
        )

        cm.add_appointment(
            Appointment(
                3,
                10,
                102,
                30,
                AppointmentStatus.NO_SHOW,
                AppointmentType.EMERGENCY,
            )
        )

        cm.add_appointment(
            Appointment(
                4,
                10,
                103,
                60,
                AppointmentStatus.CANCELLED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                5,
                10,
                104,
                30,
                AppointmentStatus.SCHEDULED,
                AppointmentType.FOLLOWUP,
            )
        )

        stats = cm.get_appointment_statistics()

        self.assertEqual(5, stats.total_appointments)
        self.assertEqual(2, stats.completed_appointments)
        self.assertAlmostEqual(0.2, stats.no_show_rate, places=4)

    def test_get_average_appointment_duration_by_type(self):
        print("Running test_get_average_appointment_duration_by_type")

        cm = ClinicManager()

        cm.add_doctor(Doctor(1, "dr_smith"))
        cm.add_doctor(Doctor(2, "dr_jones"))
        cm.add_doctor(Doctor(3, "dr_brown"))
        cm.add_doctor(Doctor(4, "dr_lee"))
        cm.add_doctor(Doctor(5, "dr_kim"))

        cm.add_appointment(
            Appointment(
                1,
                1,
                100,
                30,
                AppointmentStatus.COMPLETED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                2,
                1,
                101,
                41,
                AppointmentStatus.COMPLETED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                3,
                1,
                102,
                20,
                AppointmentStatus.COMPLETED,
                AppointmentType.FOLLOWUP,
            )
        )

        cm.add_appointment(
            Appointment(
                5,
                1,
                105,
                100,
                AppointmentStatus.CANCELLED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                8,
                1,
                200,
                220,
                AppointmentStatus.SCHEDULED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                4,
                2,
                103,
                40,
                AppointmentStatus.COMPLETED,
                AppointmentType.EMERGENCY,
            )
        )

        cm.add_appointment(
            Appointment(
                6,
                4,
                106,
                25,
                AppointmentStatus.COMPLETED,
                AppointmentType.CONSULTATION,
            )
        )

        cm.add_appointment(
            Appointment(
                7,
                5,
                107,
                15,
                AppointmentStatus.COMPLETED,
                AppointmentType.FOLLOWUP,
            )
        )

        avg1 = cm.get_average_appointment_duration_by_type(1)

        self.assertAlmostEqual(
            35.5,
            avg1[AppointmentType.CONSULTATION],
            places=4,
        )

        self.assertAlmostEqual(
            20.0,
            avg1[AppointmentType.FOLLOWUP],
            places=4,
        )

        self.assertNotIn(
            AppointmentType.EMERGENCY,
            avg1,
        )

        avg2 = cm.get_average_appointment_duration_by_type(2)

        self.assertAlmostEqual(
            40.0,
            avg2[AppointmentType.EMERGENCY],
            places=4,
        )

        self.assertNotIn(
            AppointmentType.CONSULTATION,
            avg2,
        )

        self.assertNotIn(
            AppointmentType.FOLLOWUP,
            avg2,
        )

        avg4 = cm.get_average_appointment_duration_by_type(4)

        self.assertAlmostEqual(
            25.0,
            avg4[AppointmentType.CONSULTATION],
            places=4,
        )

        self.assertNotIn(
            AppointmentType.FOLLOWUP,
            avg4,
        )

        self.assertNotIn(
            AppointmentType.EMERGENCY,
            avg4,
        )

        avg5 = cm.get_average_appointment_duration_by_type(5)

        self.assertAlmostEqual(
            15.0,
            avg5[AppointmentType.FOLLOWUP],
            places=4,
        )

        self.assertNotIn(
            AppointmentType.CONSULTATION,
            avg5,
        )

        self.assertNotIn(
            AppointmentType.EMERGENCY,
            avg5,
        )

        self.assertEqual(
            {},
            cm.get_average_appointment_duration_by_type(3),
        )

        self.assertEqual(
            {},
            cm.get_average_appointment_duration_by_type(999),
        )

        stats = cm.get_appointment_statistics()

        self.assertEqual(5, stats.total_appointments)
        self.assertEqual(2, stats.completed_appointments)
        self.assertAlmostEqual(0.2, stats.no_show_rate, places=4)


if __name__ == "__main__":
    unittest.main()


