from __future__ import unicode_literals

from django.db import models


class AcademicYear(models.Model):
    academic_year_code = models.IntegerField(primary_key=True)
    academic_year = models.CharField(max_length=10)

    def __str__(self):
        return str(self.academic_year_code)


class Department(models.Model):
    department_code = models.CharField(primary_key=True, max_length=10)
    department_name = models.CharField(max_length=30)
    inception_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)

    def __str__(self):
        return self.department_code


class Faculty(models.Model):
    faculty_code = models.CharField(primary_key=True, max_length=10)
    faculty_first_name = models.CharField(max_length=30)
    faculty_last_name = models.CharField(max_length=30)
    faculty_tel = models.CharField(max_length=30)
    faculty_email = models.CharField(max_length=30)
    home_department = models.ForeignKey(Department, on_delete=models.PROTECT)
    joining_date = models.DateField()
    relieved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.faculty_code


class Regulation(models.Model):
    regulation_code = models.CharField(primary_key=True, max_length=10)
    effective_from = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    total_required_credits = models.IntegerField()

    def __str__(self):
        return self.regulation_code


class Program(models.Model):
    program_code = models.IntegerField(primary_key=True)
    program_name = models.CharField(max_length=30)
    inception_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    owner_department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.program_name


class SubjectType(models.Model):
    subject_type = models.IntegerField(primary_key=True)
    subject_type_desc = models.CharField(max_length=30)

    def __str__(self):
        return str(self.subject_type)


class SubjectDeliveryType(models.Model):
    subject_delivery_type = models.IntegerField(primary_key=True)
    delivery_type_desc = models.CharField(max_length=30)

    def __str__(self):
        return str(self.subject_delivery_type)


class ProgramStructure(models.Model):
    class Meta:
        unique_together = (('regulation_code', 'program_code', 'subject_code'),)
    regulation_code = models.ForeignKey(Regulation, on_delete=models.PROTECT)
    program_code = models.ForeignKey(Program, on_delete=models.PROTECT)
    semester = models.IntegerField()
    subject_code = models.CharField(primary_key=True, max_length=30)
    subject_name = models.CharField(max_length=30)
    subject_type = models.ForeignKey(SubjectType, on_delete=models.PROTECT)
    subject_delivery_type = models.ForeignKey(SubjectDeliveryType, on_delete=models.PROTECT)
    number_hpw = models.IntegerField()
    number_credits = models.IntegerField()

    def __str__(self):
        return self.subject_code


class SubjectOption(models.Model):
    class Meta:
        unique_together = (('regulation_code', 'program_code', 'subject_code', 'subject_option_code'),)
    regulation_code = models.ForeignKey(ProgramStructure, related_name='Feedback_regulation_code', on_delete=models.PROTECT)
    program_code = models.ForeignKey(ProgramStructure, related_name='Feedback_program_code', on_delete=models.PROTECT)
    subject_code = models.ForeignKey(ProgramStructure, related_name='Feedback_subject_code', on_delete=models.PROTECT)
    subject_option_code = models.CharField(primary_key=True, max_length=30)
    subject_option_name = models.CharField(max_length=30)
    offered_by = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject_option_code


class FeedbackType(models.Model):
    cycle_no = models.IntegerField(primary_key=True)
    feedback_type_desc = models.CharField(max_length=70)

    def __str__(self):
        return str(self.cycle_no)


class FeedbackQuestion(models.Model):
    class Meta:
        unique_together = (('effective_from', 'cycle_no', 'question_no'),)
    effective_from = models.DateField()
    cycle_no = models.ForeignKey(FeedbackType, on_delete=models.PROTECT)
    question_no = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=100)

    def __str__(self):
        return str(self.question_no)


class CourseOffered(models.Model):
    course_code = models.IntegerField(primary_key=True)
    regulation_code = models.ForeignKey(ProgramStructure, related_name='Feedback_regulation_code2', on_delete=models.PROTECT)
    program_code = models.ForeignKey(ProgramStructure, related_name='Feedback_program_code2', on_delete=models.PROTECT)
    subject_code = models.ForeignKey(ProgramStructure, related_name='Feedback_subject_code2', on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    semester = models.CharField(max_length=7)
    course_name = models.CharField(max_length=30)
    faculty_name = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.course_code)


class StudentType(models.Model):
    student_type = models.IntegerField(primary_key=True)
    student_type_desc = models.CharField(max_length=30)

    def __str__(self):
        return str(self.student_type)


class Student(models.Model):
    student_reg_no = models.CharField(primary_key=True, max_length=15)
    student_first_name = models.CharField(max_length=30)
    student_last_name = models.CharField(max_length=30)
    student_type = models.ForeignKey(StudentType, on_delete=models.PROTECT)
    academic_year_code = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    regulation_code = models.ForeignKey(Regulation, on_delete=models.PROTECT)

    def __str__(self):
        return self.student_reg_no


# CHECK THIS

class CourseRegistration(models.Model):
    class Meta:
        unique_together = (('course_code','student_reg_no'),)
    course_code = models.ForeignKey(CourseOffered, on_delete=models.PROTECT)
    student_reg_no = models.OneToOneField(Student, primary_key=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.student_reg_no)



class CourseFeedbackAssignment(models.Model):
    class Meta:
        unique_together = (('course_code', 'student_reg_no', 'cycle_no'),)
    course_code = models.ForeignKey(CourseRegistration, related_name='CourseRegistration_course_code', on_delete=models.PROTECT)
    student_reg_no = models.OneToOneField(CourseRegistration, primary_key=True, related_name='CourseRegistration_student_reg_no', on_delete=models.PROTECT)
    cycle_no = models.ForeignKey(FeedbackType, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    feedback_weighting = models.IntegerField()
    is_given = models.IntegerField()

    def __str__(self):
        return str(self.course_code) + self.student_reg_no


class FeedbackCommentLog(models.Model):
    class Meta:
        unique_together=(('feedback_no', 'course_code', 'cycle_no'),)
    feedback_no = models.IntegerField(primary_key=True)
    course_code = models.ForeignKey(CourseOffered, on_delete=models.PROTECT)
    cycle_no = models.ForeignKey(FeedbackType, on_delete=models.PROTECT)
    feedback_weightING = models.IntegerField()
    feedback_comments = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.feedback_no)


class FeedbackRatingLog(models.Model):
    class Meta:
        unique_together = (('feedback_no', 'course_code', 'cycle_no', 'question_no'),)

    feedback_no = models.ForeignKey(FeedbackCommentLog, related_name='FeedbackCommentLog_feedback_no', on_delete=models.PROTECT)
    course_code = models.ForeignKey(FeedbackCommentLog, related_name='FeedbackCommentLog_course_code', on_delete=models.PROTECT)
    cycle_no = models.ForeignKey(FeedbackCommentLog, related_name='FeedbackCommentLog_cycle_no', on_delete=models.PROTECT)
    question_no = models.IntegerField(primary_key=True)
    feedback_weighting = models.IntegerField()
    rating_answer = models.IntegerField()

    def __str__(self):
        return str(self.feedback_no) + str(self.question_no)


class FeedbackRatingAggregate(models.Model):
    class Meta:
        unique_together = (('course_code', 'cycle_no'),)
    course_code = models.OneToOneField(CourseOffered, primary_key=True, on_delete=models.PROTECT)
    cycle_no = models.ForeignKey(FeedbackType, on_delete=models.PROTECT)
    Rating_5_count_1 = models.IntegerField()
    Rating_5_count_2 = models.IntegerField()
    Rating_4_count_1 = models.IntegerField()
    Rating_4_count_2 = models.IntegerField()
    Rating_3_count_1 = models.IntegerField()
    Rating_3_count_2 = models.IntegerField()
    Rating_2_count_1 = models.IntegerField()
    Rating_2_count_2 = models.IntegerField()
    Rating_1_count_1 = models.IntegerField()
    Rating_1_count_2 = models.IntegerField()

    def __str__(self):
        return str(self.course_code)


class UserType(models.Model):
    user_type = models.IntegerField(primary_key=True)
    user_type_desc = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user_type)


class Users(models.Model):
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT)
    id_no = models.CharField(max_length=30, primary_key=True)
    crypt_password = models.CharField(max_length=30)
    last_login_time = models.DateTimeField()

    def __str__(self):
        return self.id_no


