-- Sequence: "Platform_PlatformID_seq"

--DROP SEQUENCE "Platform_PlatformID_seq";

CREATE SEQUENCE "Platform_PlatformID_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE "Platform_PlatformID_seq"
  OWNER TO postgres;
-- Sequence: "TestRun_TestRunID_seq"

--DROP SEQUENCE "TestRun_TestRunID_seq";

CREATE SEQUENCE "TestRun_TestRunID_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE "TestRun_TestRunID_seq"
  OWNER TO postgres;
-- Sequence: "TestStep_TestStepID_seq"

--DROP SEQUENCE "TestStep_TestStepID_seq";

CREATE SEQUENCE "TestStep_TestStepID_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE "TestStep_TestStepID_seq"
  OWNER TO postgres;
-- Sequence: config_values_id_seq

--DROP SEQUENCE config_values_id_seq;

CREATE SEQUENCE config_values_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 140
  CACHE 1;
ALTER TABLE config_values_id_seq
  OWNER TO postgres;
-- Sequence: containertypedata_id_seq

--DROP SEQUENCE containertypedata_id_seq;

CREATE SEQUENCE containertypedata_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 661
  CACHE 1;
ALTER TABLE containertypedata_id_seq
  OWNER TO postgres;
-- Sequence: daily_build_status_id_seq

--DROP SEQUENCE daily_build_status_id_seq;

CREATE SEQUENCE daily_build_status_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE daily_build_status_id_seq
  OWNER TO postgres;
-- Sequence: executionlog_executionlogid_seq

--DROP SEQUENCE executionlog_executionlogid_seq;

CREATE SEQUENCE executionlog_executionlogid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 7247
  CACHE 1;
ALTER TABLE executionlog_executionlogid_seq
  OWNER TO postgres;
-- Sequence: expected_expectedid_seq

--DROP SEQUENCE expected_expectedid_seq;

CREATE SEQUENCE expected_expectedid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE expected_expectedid_seq
  OWNER TO postgres;
-- Sequence: expectedcontainer_expectedplaylistid_seq

--DROP SEQUENCE expectedcontainer_expectedplaylistid_seq;

CREATE SEQUENCE expectedcontainer_expectedplaylistid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 146
  CACHE 1;
ALTER TABLE expectedcontainer_expectedplaylistid_seq
  OWNER TO postgres;
-- Sequence: performanceresults_id_seq

--DROP SEQUENCE performanceresults_id_seq;

CREATE SEQUENCE performanceresults_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE performanceresults_id_seq
  OWNER TO postgres;
-- Sequence: product_sections_section_id_seq

--DROP SEQUENCE product_sections_section_id_seq;

CREATE SEQUENCE product_sections_section_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 14
  CACHE 1;
ALTER TABLE product_sections_section_id_seq
  OWNER TO postgres;
-- Sequence: testcase_testcaseid_seq

--DROP SEQUENCE testcase_testcaseid_seq;

CREATE SEQUENCE testcase_testcaseid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 317
  CACHE 1;
ALTER TABLE testcase_testcaseid_seq
  OWNER TO postgres;
-- Sequence: testenvresults_id

--DROP SEQUENCE testenvresults_id;

CREATE SEQUENCE testenvresults_id
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE testenvresults_id
  OWNER TO postgres;
-- Sequence: testenvresults_id_seq

--DROP SEQUENCE testenvresults_id_seq;

CREATE SEQUENCE testenvresults_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 394
  CACHE 1;
ALTER TABLE testenvresults_id_seq
  OWNER TO postgres;
-- Sequence: testresults_id_seq

--DROP SEQUENCE testresults_id_seq;

CREATE SEQUENCE testresults_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 933
  CACHE 1;
ALTER TABLE testresults_id_seq
  OWNER TO postgres;
-- Sequence: testrun_id_seq

--DROP SEQUENCE testrun_id_seq;

CREATE SEQUENCE testrun_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1232
  CACHE 1;
ALTER TABLE testrun_id_seq
  OWNER TO postgres;
-- Sequence: testrun_testrunid_seq

--DROP SEQUENCE testrun_testrunid_seq;

CREATE SEQUENCE testrun_testrunid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 1
  CACHE 1;
ALTER TABLE testrun_testrunid_seq
  OWNER TO postgres;
-- Sequence: testrunenv_id_seq

--DROP SEQUENCE testrunenv_id_seq;

CREATE SEQUENCE testrunenv_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 758
  CACHE 1;
ALTER TABLE testrunenv_id_seq
  OWNER TO postgres;
-- Sequence: teststepdata_id_seq

--DROP SEQUENCE teststepdata_id_seq;

CREATE SEQUENCE teststepdata_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 369
  CACHE 1;
ALTER TABLE teststepdata_id_seq
  OWNER TO postgres;
-- Sequence: teststepresults_id_seq

--DROP SEQUENCE teststepresults_id_seq;

CREATE SEQUENCE teststepresults_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 2969
  CACHE 1;
ALTER TABLE teststepresults_id_seq
  OWNER TO postgres;
-- Sequence: teststeps_stepsid_seq

--DROP SEQUENCE teststeps_stepsid_seq;

CREATE SEQUENCE teststeps_stepsid_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 2
  CACHE 1;
ALTER TABLE teststeps_stepsid_seq
  OWNER TO postgres;
-- Sequence: teststepslist_step_id_seq

--DROP SEQUENCE teststepslist_step_id_seq;

CREATE SEQUENCE teststepslist_step_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 49
  CACHE 1;
ALTER TABLE teststepslist_step_id_seq
  OWNER TO postgres;
-- Sequence: teststepstemp_id_seq

--DROP SEQUENCE teststepstemp_id_seq;

CREATE SEQUENCE teststepstemp_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1151
  CACHE 1;
ALTER TABLE teststepstemp_id_seq
  OWNER TO postgres;
-- Sequence: teststepstemp_teststepsequence_seq

--DROP SEQUENCE teststepstemp_teststepsequence_seq;

CREATE SEQUENCE teststepstemp_teststepsequence_seq
  INCREMENT 10
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 11390
  CACHE 1;
ALTER TABLE teststepstemp_teststepsequence_seq
  OWNER TO postgres;
