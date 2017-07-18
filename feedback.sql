-- MySQL dump 10.13  Distrib 5.5.55, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: feedback
-- ------------------------------------------------------
-- Server version	5.5.55-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Feedback_academicyear`
--

DROP TABLE IF EXISTS `Feedback_academicyear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_academicyear` (
  `academic_year_code` int(11) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  PRIMARY KEY (`academic_year_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_academicyear`
--

LOCK TABLES `Feedback_academicyear` WRITE;
/*!40000 ALTER TABLE `Feedback_academicyear` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_academicyear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_coursefeedbackassignment`
--

DROP TABLE IF EXISTS `Feedback_coursefeedbackassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_coursefeedbackassignment` (
  `student_reg_no_id` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `feedback_weighting` int(11) NOT NULL,
  `is_given` int(11) NOT NULL,
  `course_code_id` int(11) NOT NULL,
  `cycle_no_id` int(11) NOT NULL,
  PRIMARY KEY (`student_reg_no_id`),
  UNIQUE KEY `Feedback_coursefeedbacka_course_code_id_student_r_bc802f25_uniq` (`course_code_id`,`student_reg_no_id`,`cycle_no_id`),
  KEY `Feedback_coursefeedb_cycle_no_id_e1fbda49_fk_Feedback_` (`cycle_no_id`),
  CONSTRAINT `Feedback_coursefeedb_cycle_no_id_e1fbda49_fk_Feedback_` FOREIGN KEY (`cycle_no_id`) REFERENCES `Feedback_feedbacktype` (`cycle_no`),
  CONSTRAINT `Feedback_coursefeedb_course_code_id_eea26be8_fk_Feedback_` FOREIGN KEY (`course_code_id`) REFERENCES `Feedback_courseregistration` (`auto_increment_id`),
  CONSTRAINT `Feedback_coursefeedb_student_reg_no_id_088d24e5_fk_Feedback_` FOREIGN KEY (`student_reg_no_id`) REFERENCES `Feedback_courseregistration` (`auto_increment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_coursefeedbackassignment`
--

LOCK TABLES `Feedback_coursefeedbackassignment` WRITE;
/*!40000 ALTER TABLE `Feedback_coursefeedbackassignment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_coursefeedbackassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_courseoffered`
--

DROP TABLE IF EXISTS `Feedback_courseoffered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_courseoffered` (
  `course_code` int(11) NOT NULL,
  `semester` varchar(7) NOT NULL,
  `course_name` varchar(30) NOT NULL,
  `academic_year_id` int(11) NOT NULL,
  `faculty_name_id` varchar(10) NOT NULL,
  `program_code_id` varchar(30) NOT NULL,
  `regulation_code_id` varchar(30) NOT NULL,
  `subject_code_id` varchar(30) NOT NULL,
  PRIMARY KEY (`course_code`),
  KEY `Feedback_courseoffer_academic_year_id_4bd51772_fk_Feedback_` (`academic_year_id`),
  KEY `Feedback_courseoffer_faculty_name_id_521e63b2_fk_Feedback_` (`faculty_name_id`),
  KEY `Feedback_courseoffer_program_code_id_f571e215_fk_Feedback_` (`program_code_id`),
  KEY `Feedback_courseoffer_regulation_code_id_6d8bb0e9_fk_Feedback_` (`regulation_code_id`),
  KEY `Feedback_courseoffer_subject_code_id_cdff1d0c_fk_Feedback_` (`subject_code_id`),
  CONSTRAINT `Feedback_courseoffer_subject_code_id_cdff1d0c_fk_Feedback_` FOREIGN KEY (`subject_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`),
  CONSTRAINT `Feedback_courseoffer_academic_year_id_4bd51772_fk_Feedback_` FOREIGN KEY (`academic_year_id`) REFERENCES `Feedback_academicyear` (`academic_year_code`),
  CONSTRAINT `Feedback_courseoffer_faculty_name_id_521e63b2_fk_Feedback_` FOREIGN KEY (`faculty_name_id`) REFERENCES `Feedback_faculty` (`faculty_code`),
  CONSTRAINT `Feedback_courseoffer_program_code_id_f571e215_fk_Feedback_` FOREIGN KEY (`program_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`),
  CONSTRAINT `Feedback_courseoffer_regulation_code_id_6d8bb0e9_fk_Feedback_` FOREIGN KEY (`regulation_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_courseoffered`
--

LOCK TABLES `Feedback_courseoffered` WRITE;
/*!40000 ALTER TABLE `Feedback_courseoffered` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_courseoffered` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_courseregistration`
--

DROP TABLE IF EXISTS `Feedback_courseregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_courseregistration` (
  `auto_increment_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_code_id` int(11) NOT NULL,
  `student_reg_no_id` varchar(15) NOT NULL,
  PRIMARY KEY (`auto_increment_id`),
  UNIQUE KEY `Feedback_courseregistrat_course_code_id_student_r_815b5da5_uniq` (`course_code_id`,`student_reg_no_id`),
  KEY `Feedback_courseregis_student_reg_no_id_bea6f492_fk_Feedback_` (`student_reg_no_id`),
  CONSTRAINT `Feedback_courseregis_student_reg_no_id_bea6f492_fk_Feedback_` FOREIGN KEY (`student_reg_no_id`) REFERENCES `Feedback_student` (`student_reg_no`),
  CONSTRAINT `Feedback_courseregis_course_code_id_3b20afcc_fk_Feedback_` FOREIGN KEY (`course_code_id`) REFERENCES `Feedback_courseoffered` (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_courseregistration`
--

LOCK TABLES `Feedback_courseregistration` WRITE;
/*!40000 ALTER TABLE `Feedback_courseregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_courseregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_department`
--

DROP TABLE IF EXISTS `Feedback_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_department` (
  `department_code` varchar(10) NOT NULL,
  `department_name` varchar(30) NOT NULL,
  `inception_year_id` int(11) NOT NULL,
  PRIMARY KEY (`department_code`),
  KEY `Feedback_department_inception_year_id_0fdb938c_fk_Feedback_` (`inception_year_id`),
  CONSTRAINT `Feedback_department_inception_year_id_0fdb938c_fk_Feedback_` FOREIGN KEY (`inception_year_id`) REFERENCES `Feedback_academicyear` (`academic_year_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_department`
--

LOCK TABLES `Feedback_department` WRITE;
/*!40000 ALTER TABLE `Feedback_department` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_faculty`
--

DROP TABLE IF EXISTS `Feedback_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_faculty` (
  `faculty_code` varchar(10) NOT NULL,
  `faculty_first_name` varchar(30) NOT NULL,
  `faculty_last_name` varchar(30) NOT NULL,
  `faculty_tel` varchar(30) NOT NULL,
  `faculty_email` varchar(30) NOT NULL,
  `joining_date` date NOT NULL,
  `relieved_date` date DEFAULT NULL,
  `home_department_id` varchar(10) NOT NULL,
  PRIMARY KEY (`faculty_code`),
  KEY `Feedback_faculty_home_department_id_ec9c10d9_fk_Feedback_` (`home_department_id`),
  CONSTRAINT `Feedback_faculty_home_department_id_ec9c10d9_fk_Feedback_` FOREIGN KEY (`home_department_id`) REFERENCES `Feedback_department` (`department_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_faculty`
--

LOCK TABLES `Feedback_faculty` WRITE;
/*!40000 ALTER TABLE `Feedback_faculty` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_feedbackcommentlog`
--

DROP TABLE IF EXISTS `Feedback_feedbackcommentlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_feedbackcommentlog` (
  `feedback_no` int(11) NOT NULL AUTO_INCREMENT,
  `feedback_weighting` int(11) NOT NULL,
  `feedback_comments` varchar(100) DEFAULT NULL,
  `course_code_id` int(11) NOT NULL,
  `cycle_no_id` int(11) NOT NULL,
  PRIMARY KEY (`feedback_no`),
  UNIQUE KEY `Feedback_feedbackcomment_feedback_no_course_code__dbf14bb7_uniq` (`feedback_no`,`course_code_id`,`cycle_no_id`),
  KEY `Feedback_feedbackcom_course_code_id_d4a7212f_fk_Feedback_` (`course_code_id`),
  KEY `Feedback_feedbackcom_cycle_no_id_fbae6e1d_fk_Feedback_` (`cycle_no_id`),
  CONSTRAINT `Feedback_feedbackcom_cycle_no_id_fbae6e1d_fk_Feedback_` FOREIGN KEY (`cycle_no_id`) REFERENCES `Feedback_feedbacktype` (`cycle_no`),
  CONSTRAINT `Feedback_feedbackcom_course_code_id_d4a7212f_fk_Feedback_` FOREIGN KEY (`course_code_id`) REFERENCES `Feedback_courseoffered` (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_feedbackcommentlog`
--

LOCK TABLES `Feedback_feedbackcommentlog` WRITE;
/*!40000 ALTER TABLE `Feedback_feedbackcommentlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_feedbackcommentlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_feedbackquestion`
--

DROP TABLE IF EXISTS `Feedback_feedbackquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_feedbackquestion` (
  `effective_from` date NOT NULL,
  `question_no` int(11) NOT NULL,
  `question_text` varchar(1000) NOT NULL,
  `cycle_no_id` int(11) NOT NULL,
  PRIMARY KEY (`question_no`),
  UNIQUE KEY `Feedback_feedbackquestio_effective_from_cycle_no__3c8c4991_uniq` (`effective_from`,`cycle_no_id`,`question_no`),
  KEY `Feedback_feedbackque_cycle_no_id_4ec6e673_fk_Feedback_` (`cycle_no_id`),
  CONSTRAINT `Feedback_feedbackque_cycle_no_id_4ec6e673_fk_Feedback_` FOREIGN KEY (`cycle_no_id`) REFERENCES `Feedback_feedbacktype` (`cycle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_feedbackquestion`
--

LOCK TABLES `Feedback_feedbackquestion` WRITE;
/*!40000 ALTER TABLE `Feedback_feedbackquestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_feedbackquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_feedbackratingaggregate`
--

DROP TABLE IF EXISTS `Feedback_feedbackratingaggregate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_feedbackratingaggregate` (
  `course_code_id` int(11) NOT NULL,
  `rating_5_count_1` int(11) NOT NULL,
  `rating_5_count_2` int(11) NOT NULL,
  `rating_4_count_1` int(11) NOT NULL,
  `rating_4_count_2` int(11) NOT NULL,
  `rating_3_count_1` int(11) NOT NULL,
  `rating_3_count_2` int(11) NOT NULL,
  `rating_2_count_1` int(11) NOT NULL,
  `rating_2_count_2` int(11) NOT NULL,
  `rating_1_count_1` int(11) NOT NULL,
  `rating_1_count_2` int(11) NOT NULL,
  `cycle_no_id` int(11) NOT NULL,
  PRIMARY KEY (`course_code_id`),
  UNIQUE KEY `Feedback_feedbackratinga_course_code_id_cycle_no__bfb28922_uniq` (`course_code_id`,`cycle_no_id`),
  KEY `Feedback_feedbackrat_cycle_no_id_7807b7fe_fk_Feedback_` (`cycle_no_id`),
  CONSTRAINT `Feedback_feedbackrat_cycle_no_id_7807b7fe_fk_Feedback_` FOREIGN KEY (`cycle_no_id`) REFERENCES `Feedback_feedbacktype` (`cycle_no`),
  CONSTRAINT `Feedback_feedbackrat_course_code_id_6afb4769_fk_Feedback_` FOREIGN KEY (`course_code_id`) REFERENCES `Feedback_courseoffered` (`course_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_feedbackratingaggregate`
--

LOCK TABLES `Feedback_feedbackratingaggregate` WRITE;
/*!40000 ALTER TABLE `Feedback_feedbackratingaggregate` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_feedbackratingaggregate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_feedbackratinglog`
--

DROP TABLE IF EXISTS `Feedback_feedbackratinglog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_feedbackratinglog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_no` int(11) NOT NULL,
  `feedback_weighting` int(11) NOT NULL,
  `rating_answer` int(11) NOT NULL,
  `course_code_id` int(11) NOT NULL,
  `cycle_no_id` int(11) NOT NULL,
  `feedback_no_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Feedback_feedbackratingl_feedback_no_id_course_co_90275d4e_uniq` (`feedback_no_id`,`course_code_id`,`cycle_no_id`,`question_no`),
  KEY `Feedback_feedbackrat_course_code_id_95eba3f9_fk_Feedback_` (`course_code_id`),
  KEY `Feedback_feedbackrat_cycle_no_id_a3621331_fk_Feedback_` (`cycle_no_id`),
  CONSTRAINT `Feedback_feedbackrat_feedback_no_id_6508940c_fk_Feedback_` FOREIGN KEY (`feedback_no_id`) REFERENCES `Feedback_feedbackcommentlog` (`feedback_no`),
  CONSTRAINT `Feedback_feedbackrat_course_code_id_95eba3f9_fk_Feedback_` FOREIGN KEY (`course_code_id`) REFERENCES `Feedback_feedbackcommentlog` (`feedback_no`),
  CONSTRAINT `Feedback_feedbackrat_cycle_no_id_a3621331_fk_Feedback_` FOREIGN KEY (`cycle_no_id`) REFERENCES `Feedback_feedbackcommentlog` (`feedback_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_feedbackratinglog`
--

LOCK TABLES `Feedback_feedbackratinglog` WRITE;
/*!40000 ALTER TABLE `Feedback_feedbackratinglog` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_feedbackratinglog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_feedbacktype`
--

DROP TABLE IF EXISTS `Feedback_feedbacktype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_feedbacktype` (
  `cycle_no` int(11) NOT NULL,
  `feedback_type_desc` varchar(70) NOT NULL,
  PRIMARY KEY (`cycle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_feedbacktype`
--

LOCK TABLES `Feedback_feedbacktype` WRITE;
/*!40000 ALTER TABLE `Feedback_feedbacktype` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_feedbacktype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_program`
--

DROP TABLE IF EXISTS `Feedback_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_program` (
  `program_code` int(11) NOT NULL,
  `program_name` varchar(30) NOT NULL,
  `inception_year_id` int(11) NOT NULL,
  `owner_department_id` varchar(10) NOT NULL,
  PRIMARY KEY (`program_code`),
  KEY `Feedback_program_inception_year_id_d5540f98_fk_Feedback_` (`inception_year_id`),
  KEY `Feedback_program_owner_department_id_a77dc2db_fk_Feedback_` (`owner_department_id`),
  CONSTRAINT `Feedback_program_owner_department_id_a77dc2db_fk_Feedback_` FOREIGN KEY (`owner_department_id`) REFERENCES `Feedback_department` (`department_code`),
  CONSTRAINT `Feedback_program_inception_year_id_d5540f98_fk_Feedback_` FOREIGN KEY (`inception_year_id`) REFERENCES `Feedback_academicyear` (`academic_year_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_program`
--

LOCK TABLES `Feedback_program` WRITE;
/*!40000 ALTER TABLE `Feedback_program` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_programstructure`
--

DROP TABLE IF EXISTS `Feedback_programstructure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_programstructure` (
  `semester` int(11) NOT NULL,
  `subject_code` varchar(30) NOT NULL,
  `subject_name` varchar(30) NOT NULL,
  `number_hpw` int(11) NOT NULL,
  `number_credits` int(11) NOT NULL,
  `program_code_id` int(11) NOT NULL,
  `regulation_code_id` varchar(10) NOT NULL,
  `subject_delivery_type_id` int(11) NOT NULL,
  `subject_type_id` int(11) NOT NULL,
  PRIMARY KEY (`subject_code`),
  UNIQUE KEY `Feedback_programstructur_regulation_code_id_progr_a5c0543c_uniq` (`regulation_code_id`,`program_code_id`,`subject_code`),
  KEY `Feedback_programstru_program_code_id_aeea4a41_fk_Feedback_` (`program_code_id`),
  KEY `Feedback_programstru_subject_delivery_typ_9b346723_fk_Feedback_` (`subject_delivery_type_id`),
  KEY `Feedback_programstru_subject_type_id_2eb5f6bc_fk_Feedback_` (`subject_type_id`),
  CONSTRAINT `Feedback_programstru_subject_type_id_2eb5f6bc_fk_Feedback_` FOREIGN KEY (`subject_type_id`) REFERENCES `Feedback_subjecttype` (`subject_type`),
  CONSTRAINT `Feedback_programstru_program_code_id_aeea4a41_fk_Feedback_` FOREIGN KEY (`program_code_id`) REFERENCES `Feedback_program` (`program_code`),
  CONSTRAINT `Feedback_programstru_regulation_code_id_eea9a532_fk_Feedback_` FOREIGN KEY (`regulation_code_id`) REFERENCES `Feedback_regulation` (`regulation_code`),
  CONSTRAINT `Feedback_programstru_subject_delivery_typ_9b346723_fk_Feedback_` FOREIGN KEY (`subject_delivery_type_id`) REFERENCES `Feedback_subjectdeliverytype` (`subject_delivery_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_programstructure`
--

LOCK TABLES `Feedback_programstructure` WRITE;
/*!40000 ALTER TABLE `Feedback_programstructure` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_programstructure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_regulation`
--

DROP TABLE IF EXISTS `Feedback_regulation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_regulation` (
  `regulation_code` varchar(10) NOT NULL,
  `total_required_credits` int(11) NOT NULL,
  `effective_from_id` int(11) NOT NULL,
  PRIMARY KEY (`regulation_code`),
  KEY `Feedback_regulation_effective_from_id_f3da4b86_fk_Feedback_` (`effective_from_id`),
  CONSTRAINT `Feedback_regulation_effective_from_id_f3da4b86_fk_Feedback_` FOREIGN KEY (`effective_from_id`) REFERENCES `Feedback_academicyear` (`academic_year_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_regulation`
--

LOCK TABLES `Feedback_regulation` WRITE;
/*!40000 ALTER TABLE `Feedback_regulation` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_regulation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_student`
--

DROP TABLE IF EXISTS `Feedback_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_student` (
  `student_reg_no` varchar(15) NOT NULL,
  `student_first_name` varchar(30) NOT NULL,
  `student_last_name` varchar(30) NOT NULL,
  `academic_year_code_id` int(11) NOT NULL,
  `regulation_code_id` varchar(10) NOT NULL,
  `student_type_id` int(11) NOT NULL,
  PRIMARY KEY (`student_reg_no`),
  KEY `Feedback_student_academic_year_code_i_505b8823_fk_Feedback_` (`academic_year_code_id`),
  KEY `Feedback_student_regulation_code_id_565c6206_fk_Feedback_` (`regulation_code_id`),
  KEY `Feedback_student_student_type_id_98fab7ae_fk_Feedback_` (`student_type_id`),
  CONSTRAINT `Feedback_student_student_type_id_98fab7ae_fk_Feedback_` FOREIGN KEY (`student_type_id`) REFERENCES `Feedback_studenttype` (`student_type`),
  CONSTRAINT `Feedback_student_academic_year_code_i_505b8823_fk_Feedback_` FOREIGN KEY (`academic_year_code_id`) REFERENCES `Feedback_academicyear` (`academic_year_code`),
  CONSTRAINT `Feedback_student_regulation_code_id_565c6206_fk_Feedback_` FOREIGN KEY (`regulation_code_id`) REFERENCES `Feedback_regulation` (`regulation_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_student`
--

LOCK TABLES `Feedback_student` WRITE;
/*!40000 ALTER TABLE `Feedback_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_studenttype`
--

DROP TABLE IF EXISTS `Feedback_studenttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_studenttype` (
  `student_type` int(11) NOT NULL,
  `student_type_desc` varchar(30) NOT NULL,
  PRIMARY KEY (`student_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_studenttype`
--

LOCK TABLES `Feedback_studenttype` WRITE;
/*!40000 ALTER TABLE `Feedback_studenttype` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_studenttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_subjectdeliverytype`
--

DROP TABLE IF EXISTS `Feedback_subjectdeliverytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_subjectdeliverytype` (
  `subject_delivery_type` int(11) NOT NULL,
  `delivery_type_desc` varchar(30) NOT NULL,
  PRIMARY KEY (`subject_delivery_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_subjectdeliverytype`
--

LOCK TABLES `Feedback_subjectdeliverytype` WRITE;
/*!40000 ALTER TABLE `Feedback_subjectdeliverytype` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_subjectdeliverytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_subjectoption`
--

DROP TABLE IF EXISTS `Feedback_subjectoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_subjectoption` (
  `subject_option_code` varchar(30) NOT NULL,
  `subject_option_name` varchar(30) NOT NULL,
  `offered_by_id` varchar(10) NOT NULL,
  `program_code_id` varchar(30) NOT NULL,
  `regulation_code_id` varchar(30) NOT NULL,
  `subject_code_id` varchar(30) NOT NULL,
  PRIMARY KEY (`subject_option_code`),
  UNIQUE KEY `Feedback_subjectoption_regulation_code_id_progr_61c93f87_uniq` (`regulation_code_id`,`program_code_id`,`subject_code_id`,`subject_option_code`),
  KEY `Feedback_subjectopti_offered_by_id_772172d3_fk_Feedback_` (`offered_by_id`),
  KEY `Feedback_subjectopti_program_code_id_c99168b8_fk_Feedback_` (`program_code_id`),
  KEY `Feedback_subjectopti_subject_code_id_487eaeee_fk_Feedback_` (`subject_code_id`),
  CONSTRAINT `Feedback_subjectopti_subject_code_id_487eaeee_fk_Feedback_` FOREIGN KEY (`subject_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`),
  CONSTRAINT `Feedback_subjectopti_offered_by_id_772172d3_fk_Feedback_` FOREIGN KEY (`offered_by_id`) REFERENCES `Feedback_department` (`department_code`),
  CONSTRAINT `Feedback_subjectopti_program_code_id_c99168b8_fk_Feedback_` FOREIGN KEY (`program_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`),
  CONSTRAINT `Feedback_subjectopti_regulation_code_id_666c475a_fk_Feedback_` FOREIGN KEY (`regulation_code_id`) REFERENCES `Feedback_programstructure` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_subjectoption`
--

LOCK TABLES `Feedback_subjectoption` WRITE;
/*!40000 ALTER TABLE `Feedback_subjectoption` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_subjectoption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_subjecttype`
--

DROP TABLE IF EXISTS `Feedback_subjecttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_subjecttype` (
  `subject_type` int(11) NOT NULL,
  `subject_type_desc` varchar(30) NOT NULL,
  PRIMARY KEY (`subject_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_subjecttype`
--

LOCK TABLES `Feedback_subjecttype` WRITE;
/*!40000 ALTER TABLE `Feedback_subjecttype` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_subjecttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_users`
--

DROP TABLE IF EXISTS `Feedback_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_users` (
  `id_no` varchar(30) NOT NULL,
  `crypt_password` varchar(30) NOT NULL,
  `last_login_time` datetime NOT NULL,
  `user_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id_no`),
  KEY `Feedback_users_user_type_id_93ceb956_fk_Feedback_` (`user_type_id`),
  CONSTRAINT `Feedback_users_user_type_id_93ceb956_fk_Feedback_` FOREIGN KEY (`user_type_id`) REFERENCES `Feedback_usertype` (`user_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_users`
--

LOCK TABLES `Feedback_users` WRITE;
/*!40000 ALTER TABLE `Feedback_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feedback_usertype`
--

DROP TABLE IF EXISTS `Feedback_usertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feedback_usertype` (
  `user_type` int(11) NOT NULL,
  `user_type_desc` varchar(30) NOT NULL,
  PRIMARY KEY (`user_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feedback_usertype`
--

LOCK TABLES `Feedback_usertype` WRITE;
/*!40000 ALTER TABLE `Feedback_usertype` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feedback_usertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user type',1,'add_usertype'),(2,'Can change user type',1,'change_usertype'),(3,'Can delete user type',1,'delete_usertype'),(4,'Can add program',2,'add_program'),(5,'Can change program',2,'change_program'),(6,'Can delete program',2,'delete_program'),(7,'Can add course registration',3,'add_courseregistration'),(8,'Can change course registration',3,'change_courseregistration'),(9,'Can delete course registration',3,'delete_courseregistration'),(10,'Can add subject option',4,'add_subjectoption'),(11,'Can change subject option',4,'change_subjectoption'),(12,'Can delete subject option',4,'delete_subjectoption'),(13,'Can add course offered',5,'add_courseoffered'),(14,'Can change course offered',5,'change_courseoffered'),(15,'Can delete course offered',5,'delete_courseoffered'),(16,'Can add course feedback assignment',6,'add_coursefeedbackassignment'),(17,'Can change course feedback assignment',6,'change_coursefeedbackassignment'),(18,'Can delete course feedback assignment',6,'delete_coursefeedbackassignment'),(19,'Can add subject type',7,'add_subjecttype'),(20,'Can change subject type',7,'change_subjecttype'),(21,'Can delete subject type',7,'delete_subjecttype'),(22,'Can add regulation',8,'add_regulation'),(23,'Can change regulation',8,'change_regulation'),(24,'Can delete regulation',8,'delete_regulation'),(25,'Can add feedback type',9,'add_feedbacktype'),(26,'Can change feedback type',9,'change_feedbacktype'),(27,'Can delete feedback type',9,'delete_feedbacktype'),(28,'Can add academic year',10,'add_academicyear'),(29,'Can change academic year',10,'change_academicyear'),(30,'Can delete academic year',10,'delete_academicyear'),(31,'Can add faculty',11,'add_faculty'),(32,'Can change faculty',11,'change_faculty'),(33,'Can delete faculty',11,'delete_faculty'),(34,'Can add users',12,'add_users'),(35,'Can change users',12,'change_users'),(36,'Can delete users',12,'delete_users'),(37,'Can add subject delivery type',13,'add_subjectdeliverytype'),(38,'Can change subject delivery type',13,'change_subjectdeliverytype'),(39,'Can delete subject delivery type',13,'delete_subjectdeliverytype'),(40,'Can add department',14,'add_department'),(41,'Can change department',14,'change_department'),(42,'Can delete department',14,'delete_department'),(43,'Can add feedback rating log',15,'add_feedbackratinglog'),(44,'Can change feedback rating log',15,'change_feedbackratinglog'),(45,'Can delete feedback rating log',15,'delete_feedbackratinglog'),(46,'Can add student',16,'add_student'),(47,'Can change student',16,'change_student'),(48,'Can delete student',16,'delete_student'),(49,'Can add feedback rating aggregate',17,'add_feedbackratingaggregate'),(50,'Can change feedback rating aggregate',17,'change_feedbackratingaggregate'),(51,'Can delete feedback rating aggregate',17,'delete_feedbackratingaggregate'),(52,'Can add program structure',18,'add_programstructure'),(53,'Can change program structure',18,'change_programstructure'),(54,'Can delete program structure',18,'delete_programstructure'),(55,'Can add feedback question',19,'add_feedbackquestion'),(56,'Can change feedback question',19,'change_feedbackquestion'),(57,'Can delete feedback question',19,'delete_feedbackquestion'),(58,'Can add student type',20,'add_studenttype'),(59,'Can change student type',20,'change_studenttype'),(60,'Can delete student type',20,'delete_studenttype'),(61,'Can add feedback comment log',21,'add_feedbackcommentlog'),(62,'Can change feedback comment log',21,'change_feedbackcommentlog'),(63,'Can delete feedback comment log',21,'delete_feedbackcommentlog'),(64,'Can add log entry',22,'add_logentry'),(65,'Can change log entry',22,'change_logentry'),(66,'Can delete log entry',22,'delete_logentry'),(67,'Can add group',23,'add_group'),(68,'Can change group',23,'change_group'),(69,'Can delete group',23,'delete_group'),(70,'Can add permission',24,'add_permission'),(71,'Can change permission',24,'change_permission'),(72,'Can delete permission',24,'delete_permission'),(73,'Can add user',25,'add_user'),(74,'Can change user',25,'change_user'),(75,'Can delete user',25,'delete_user'),(76,'Can add content type',26,'add_contenttype'),(77,'Can change content type',26,'change_contenttype'),(78,'Can delete content type',26,'delete_contenttype'),(79,'Can add session',27,'add_session'),(80,'Can change session',27,'change_session'),(81,'Can delete session',27,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$3T2Ile0BkgLV$Xvq8yQS8cN5dEsmkCF88J6q4a3VPSlz20ZyMxzHdT+I=','2017-07-18 10:24:39',1,'praveen','','','',1,1,'2017-07-18 10:21:46');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (22,'admin','logentry'),(23,'auth','group'),(24,'auth','permission'),(25,'auth','user'),(26,'contenttypes','contenttype'),(10,'Feedback','academicyear'),(6,'Feedback','coursefeedbackassignment'),(5,'Feedback','courseoffered'),(3,'Feedback','courseregistration'),(14,'Feedback','department'),(11,'Feedback','faculty'),(21,'Feedback','feedbackcommentlog'),(19,'Feedback','feedbackquestion'),(17,'Feedback','feedbackratingaggregate'),(15,'Feedback','feedbackratinglog'),(9,'Feedback','feedbacktype'),(2,'Feedback','program'),(18,'Feedback','programstructure'),(8,'Feedback','regulation'),(16,'Feedback','student'),(20,'Feedback','studenttype'),(13,'Feedback','subjectdeliverytype'),(4,'Feedback','subjectoption'),(7,'Feedback','subjecttype'),(12,'Feedback','users'),(1,'Feedback','usertype'),(27,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'Feedback','0001_initial','2017-07-18 10:19:54'),(2,'contenttypes','0001_initial','2017-07-18 10:19:54'),(3,'auth','0001_initial','2017-07-18 10:19:57'),(4,'admin','0001_initial','2017-07-18 10:19:57'),(5,'admin','0002_logentry_remove_auto_add','2017-07-18 10:19:57'),(6,'contenttypes','0002_remove_content_type_name','2017-07-18 10:19:58'),(7,'auth','0002_alter_permission_name_max_length','2017-07-18 10:19:58'),(8,'auth','0003_alter_user_email_max_length','2017-07-18 10:19:58'),(9,'auth','0004_alter_user_username_opts','2017-07-18 10:19:58'),(10,'auth','0005_alter_user_last_login_null','2017-07-18 10:19:58'),(11,'auth','0006_require_contenttypes_0002','2017-07-18 10:19:58'),(12,'auth','0007_alter_validators_add_error_messages','2017-07-18 10:19:58'),(13,'auth','0008_alter_user_username_max_length','2017-07-18 10:19:58'),(14,'sessions','0001_initial','2017-07-18 10:19:59');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3hpop2nclz8f4vlgbkgxhp6mq57yk21j','MTRkNzA5OGE0NWFiMzNjYTFjZWNiMmI3YWVjYzk5ODBkZDIwYTBhZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjMxZjNlYzI5NzM0ZWYzN2M2MWM4YzYzOWFlODRkNzNkYWEyY2EzNGYiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2017-08-01 10:24:46');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-18 15:59:02
