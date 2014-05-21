-- Table: config_values

-- DROP TABLE config_values;
CREATE TABLE config_values
(
  id integer NOT NULL DEFAULT nextval('config_values_id_seq'::regclass),
  type character varying(100) NOT NULL,
  sub_type character varying(100),
  value character varying(100) NOT NULL,
  CONSTRAINT config_values_pkey PRIMARY KEY (type, value)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE config_values
  OWNER TO postgres;

-- Table: container_type_data

-- DROP TABLE container_type_data;

CREATE TABLE container_type_data
(
  id integer NOT NULL DEFAULT nextval('containertypedata_id_seq'::regclass), -- Database index use only
  dataid character varying(20),
  curname character varying(200),
  newname character varying(300),
  items_count integer,
  CONSTRAINT playlistdata_pkey PRIMARY KEY (id),
  CONSTRAINT container_type_data_dataid_curname_newname_key UNIQUE (dataid, curname, newname)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE container_type_data
  OWNER TO postgres;
GRANT ALL ON TABLE container_type_data TO postgres;
GRANT ALL ON TABLE container_type_data TO public;
COMMENT ON COLUMN container_type_data.id IS 'Database index use only';

-- Table: daily_build_status

-- DROP TABLE daily_build_status;

CREATE TABLE daily_build_status
(
  id integer NOT NULL DEFAULT nextval('daily_build_status_id_seq'::regclass), -- Database index use only
  daily_build_user character varying(100) NOT NULL, -- Daily build User
  status character varying(100) NOT NULL, -- Used to report the Status of the daily build
  last_checked_time timestamp without time zone DEFAULT now(), -- timestamp of last checked for the daliy bulid
  bundle character varying(100) NOT NULL, -- Desktop Bundle number
  machine_os character varying(100), -- Operating System
  local_ip character varying(30), -- ip address of SUT
  branch character varying(30), -- Build Branch (ie. SCM, Tachyon, jenkins)
  release character varying(30), -- Desktop Release
  run_id character varying(100), -- Run ID for the Current Test Run
  build_path character varying(1000), -- path to build location
  CONSTRAINT daily_build_user_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE daily_build_status
  OWNER TO postgres;
COMMENT ON TABLE daily_build_status
  IS 'Contains daily build status information.
';
COMMENT ON COLUMN daily_build_status.id IS 'Database index use only';
COMMENT ON COLUMN daily_build_status.daily_build_user IS 'Daily build User';
COMMENT ON COLUMN daily_build_status.status IS 'Used to report the Status of the daily build';
COMMENT ON COLUMN daily_build_status.last_checked_time IS 'timestamp of last checked for the daliy bulid';
COMMENT ON COLUMN daily_build_status.bundle IS 'Desktop Bundle number';
COMMENT ON COLUMN daily_build_status.machine_os IS 'Operating System';
COMMENT ON COLUMN daily_build_status.local_ip IS 'ip address of SUT';
COMMENT ON COLUMN daily_build_status.branch IS 'Build Branch (ie. SCM, Tachyon, jenkins)';
COMMENT ON COLUMN daily_build_status.release IS 'Desktop Release';
COMMENT ON COLUMN daily_build_status.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN daily_build_status.build_path IS 'path to build location';

-- Table: execution_log

-- DROP TABLE execution_log;

CREATE TABLE execution_log
(
  executionlogid integer NOT NULL DEFAULT nextval('executionlog_executionlogid_seq'::regclass), -- execution log id
  logid character varying(40),
  modulename character varying(60) NOT NULL, -- module name that is being executed
  details text, -- A text description of the task being executed
  status character varying(100) NOT NULL,
  loglevel integer NOT NULL, -- log level = (1, 2, 3)
  tstamp timestamp without time zone DEFAULT now(), -- Timestamp
  CONSTRAINT executionlog_pkey PRIMARY KEY (executionlogid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE execution_log
  OWNER TO postgres;
GRANT ALL ON TABLE execution_log TO postgres;
GRANT ALL ON TABLE execution_log TO public;
COMMENT ON TABLE execution_log
  IS 'Contains detailed information on the execution of tasks.
For Example: Module CloseDTM: DTSGeneral was executed were Desktop Manager window not found ';
COMMENT ON COLUMN execution_log.executionlogid IS 'execution log id';
COMMENT ON COLUMN execution_log.modulename IS 'module name that is being executed';
COMMENT ON COLUMN execution_log.details IS 'A text description of the task being executed';
COMMENT ON COLUMN execution_log.loglevel IS 'log level = (1, 2, 3)';
COMMENT ON COLUMN execution_log.tstamp IS 'Timestamp';
-- Table: test_cases

-- DROP TABLE test_cases;

CREATE TABLE test_cases
(
  tc_id character varying(10) NOT NULL, -- Test Case id for referenceing a test case
  tc_name character varying(100) NOT NULL, -- Test Case Name
  tc_type character varying(10) NOT NULL, -- Test Case Type (ie. Auto, Perfor)
  tc_executiontype character varying(20),
  tc_priority character varying(10),
  tc_localization character varying(10) NOT NULL, -- Test Case Localization (yes, no)
  tc_createdby character varying(40) NOT NULL, -- name of the person who created the test case
  tc_creationdate date NOT NULL, -- Creation Date
  tc_modifiedby character varying(40) NOT NULL, -- Person who last modified the test case
  tc_modifydate date NOT NULL, -- Modification Date
  defectid character varying(15),
  prd_no character varying(15),
  CONSTRAINT testcases_pkey PRIMARY KEY (tc_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_cases
  OWNER TO postgres;
GRANT ALL ON TABLE test_cases TO postgres;
GRANT ALL ON TABLE test_cases TO public;
COMMENT ON COLUMN test_cases.tc_id IS 'Test Case id for referenceing a test case';
COMMENT ON COLUMN test_cases.tc_name IS 'Test Case Name';
COMMENT ON COLUMN test_cases.tc_type IS 'Test Case Type (ie. Auto, Perfor)';
COMMENT ON COLUMN test_cases.tc_localization IS 'Test Case Localization (yes, no)';
COMMENT ON COLUMN test_cases.tc_createdby IS 'name of the person who created the test case';
COMMENT ON COLUMN test_cases.tc_creationdate IS 'Creation Date';
COMMENT ON COLUMN test_cases.tc_modifiedby IS 'Person who last modified the test case';
COMMENT ON COLUMN test_cases.tc_modifydate IS 'Modification Date';
-- Table: test_case_datasets

-- DROP TABLE test_case_datasets;

CREATE TABLE test_case_datasets
(
  tcdatasetid character varying(20) NOT NULL, -- Test Case Data Set ID
  tc_id character varying(10), -- Test Case ID
  execornot character varying(10) NOT NULL, -- Execute Test Case = Yes or No
  data_type text NOT NULL, -- Default
  CONSTRAINT tcdataset_pkey PRIMARY KEY (tcdatasetid),
  CONSTRAINT tcdataset_tc_id_fkey FOREIGN KEY (tc_id)
      REFERENCES test_cases (tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_case_datasets
  OWNER TO postgres;
GRANT ALL ON TABLE test_case_datasets TO postgres;
GRANT ALL ON TABLE test_case_datasets TO public;
COMMENT ON COLUMN test_case_datasets.tcdatasetid IS 'Test Case Data Set ID';
COMMENT ON COLUMN test_case_datasets.tc_id IS 'Test Case ID';
COMMENT ON COLUMN test_case_datasets.execornot IS 'Execute Test Case = Yes or No';
COMMENT ON COLUMN test_case_datasets.data_type IS 'Default';

-- Table: expected_datasets

-- DROP TABLE expected_datasets;

CREATE TABLE expected_datasets
(
  expectedrefid character varying(20) NOT NULL, -- Database use only.
  dataid character varying(20) NOT NULL, -- Data Id for referenceing table elements
  datasetid character varying(20), -- Data Set ID
  stepsseq integer NOT NULL, -- Step Sequence number
  CONSTRAINT expectedref_pkey PRIMARY KEY (expectedrefid),
  CONSTRAINT expectedref_datasetid_fkey FOREIGN KEY (datasetid)
      REFERENCES test_case_datasets (tcdatasetid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE expected_datasets
  OWNER TO postgres;
GRANT ALL ON TABLE expected_datasets TO postgres;
GRANT ALL ON TABLE expected_datasets TO public;
COMMENT ON COLUMN expected_datasets.expectedrefid IS 'Database use only.';
COMMENT ON COLUMN expected_datasets.dataid IS 'Data Id for referenceing table elements';
COMMENT ON COLUMN expected_datasets.datasetid IS 'Data Set ID';
COMMENT ON COLUMN expected_datasets.stepsseq IS 'Step Sequence number';

-- Table: expected

-- DROP TABLE expected;

CREATE TABLE expected
(
  expectedid integer NOT NULL DEFAULT nextval('expected_expectedid_seq'::regclass), -- Database index use only
  expectedrefid character varying(20) NOT NULL, -- Expected Reference ID
  entity character varying(20) NOT NULL, -- Type of entity (ie. Track, File, Folder, etc)
  devicefilepath text NOT NULL, -- Device filepath to entity
  md5whole character varying(100), -- MD5 value
  md5content character varying(100),
  propertyid character varying(20),
  CONSTRAINT expected_pkey PRIMARY KEY (expectedid),
  CONSTRAINT expected_expectedrefid_fkey FOREIGN KEY (expectedrefid)
      REFERENCES expected_datasets (expectedrefid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE expected
  OWNER TO postgres;
GRANT ALL ON TABLE expected TO postgres;
GRANT ALL ON TABLE expected TO public;
COMMENT ON TABLE expected
  IS 'Contains expected data items for a particular data set.
For Example: MD5 values for a track.';
COMMENT ON COLUMN expected.expectedid IS 'Database index use only';
COMMENT ON COLUMN expected.expectedrefid IS 'Expected Reference ID';
COMMENT ON COLUMN expected.entity IS 'Type of entity (ie. Track, File, Folder, etc)';
COMMENT ON COLUMN expected.devicefilepath IS 'Device filepath to entity';
COMMENT ON COLUMN expected.md5whole IS 'MD5 value';

-- Table: expected_container

-- DROP TABLE expected_container;

CREATE TABLE expected_container
(
  expectedplaylistid integer NOT NULL DEFAULT nextval('expectedcontainer_expectedplaylistid_seq'::regclass), -- Database index use only
  exprefid character varying(20) NOT NULL, -- Expected Reference ID
  container_name character varying(30) NOT NULL, -- Container Name (ie. playlist)
  exporderid character varying(20), -- Expected Order
  CONSTRAINT expectedplaylist_pkey PRIMARY KEY (expectedplaylistid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE expected_container
  OWNER TO postgres;
GRANT ALL ON TABLE expected_container TO postgres;
GRANT ALL ON TABLE expected_container TO public;
COMMENT ON TABLE expected_container
  IS 'Contains expected data information.
For Example: exprefid Exp1 contains 3 container_name (aka playlists)';
COMMENT ON COLUMN expected_container.expectedplaylistid IS 'Database index use only';
COMMENT ON COLUMN expected_container.exprefid IS 'Expected Reference ID';
COMMENT ON COLUMN expected_container.container_name IS 'Container Name (ie. playlist)';
COMMENT ON COLUMN expected_container.exporderid IS 'Expected Order';

-- Table: master_data

-- DROP TABLE master_data;

CREATE TABLE master_data
(
  id character varying(30) NOT NULL,
  field character varying(50) NOT NULL,
  value text NOT NULL,
  description character varying(200),
  CONSTRAINT pim_master_data_pkey PRIMARY KEY (id, field, value)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE master_data
  OWNER TO postgres;
-- Table: performance_results

-- DROP TABLE performance_results;

CREATE TABLE performance_results
(
  id integer NOT NULL DEFAULT nextval('performanceresults_id_seq'::regclass), -- Database index use only
  product_version character varying(300) NOT NULL,
  tc_id character varying(20) NOT NULL,
  run_id character varying(100),
  duration interval,
  cpu_avg integer,
  cpu_peak integer,
  machine_os character varying(100),
  hw_model character varying(50),
  memory_delta integer,
  cpu_peaktime time without time zone,
  CONSTRAINT performanceresults_pkey PRIMARY KEY (id),
  CONSTRAINT performanceresults_tc_id_fkey FOREIGN KEY (tc_id)
      REFERENCES test_cases (tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE performance_results
  OWNER TO postgres;
COMMENT ON COLUMN performance_results.id IS 'Database index use only';


-- Table: permitted_user_list

-- DROP TABLE permitted_user_list;

CREATE TABLE permitted_user_list
(
  user_names character varying(255) NOT NULL,
  user_level character varying(255) NOT NULL,
  email character varying(100) NOT NULL,
  CONSTRAINT permitted_user_list_pkey PRIMARY KEY (user_names, user_level)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE permitted_user_list
  OWNER TO postgres;
GRANT ALL ON TABLE permitted_user_list TO postgres;
GRANT ALL ON TABLE permitted_user_list TO public;
-- Table: product_sections

-- DROP TABLE product_sections;

CREATE TABLE product_sections
(
  section_id integer NOT NULL DEFAULT nextval('product_sections_section_id_seq'::regclass),
  section_path ltree NOT NULL,
  CONSTRAINT product_sections_pkey PRIMARY KEY (section_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE product_sections
  OWNER TO postgres;
-- Table: result_test_cases

-- DROP TABLE result_test_cases;

CREATE TABLE result_test_cases
(
  run_id character varying(100) NOT NULL,
  tc_id character varying(10) NOT NULL,
  tc_name character varying(100) NOT NULL,
  tc_type character varying(10) NOT NULL,
  tc_executiontype character varying(20),
  tc_priority character varying(10),
  tc_localization character varying(10) NOT NULL,
  tc_createdby character varying(40) NOT NULL,
  tc_creationdate date NOT NULL,
  tc_modifiedby character varying(40) NOT NULL,
  tc_modifydate date NOT NULL,
  defectid character varying(15),
  prd_no character varying(15),
  CONSTRAINT resulttestcases_pkey PRIMARY KEY (run_id, tc_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_cases
  OWNER TO postgres;

-- Table: result_container_type_data

-- DROP TABLE result_container_type_data;

CREATE TABLE result_container_type_data
(
  run_id character varying(100) NOT NULL,
  id integer NOT NULL,
  dataid character varying(20),
  curname character varying(200),
  newname character varying(300),
  items_count integer,
  CONSTRAINT result_container_type_data_pkey PRIMARY KEY (run_id, id),
  CONSTRAINT result_container_type_data_dataid_curname_newname_key UNIQUE (run_id, dataid, curname, newname)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_container_type_data
  OWNER TO postgres;
-- Table: result_master_data

-- DROP TABLE result_master_data;

CREATE TABLE result_master_data
(
  run_id character varying(100) NOT NULL,
  id character varying(30) NOT NULL,
  field character varying(50) NOT NULL,
  value text NOT NULL,
  description character varying(200),
  CONSTRAINT result_master_data_pkey PRIMARY KEY (run_id, id, field, value)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_master_data
  OWNER TO postgres;
-- Table: result_test_case_datasets

-- DROP TABLE result_test_case_datasets;

CREATE TABLE result_test_case_datasets
(
  run_id character varying(100) NOT NULL,
  tcdatasetid character varying(20) NOT NULL,
  tc_id character varying(10),
  execornot character varying(10) NOT NULL,
  data_type text NOT NULL,
  CONSTRAINT result_test_case_datasets_pkey PRIMARY KEY (run_id, tcdatasetid),
  CONSTRAINT result_test_case_datasets_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_case_datasets
  OWNER TO postgres;
-- Table: result_test_case_tag

-- DROP TABLE result_test_case_tag;

CREATE TABLE result_test_case_tag
(
  run_id character varying(100) NOT NULL,
  tc_id character varying(10) NOT NULL,
  name character varying(100) NOT NULL,
  property character varying(100) NOT NULL,
  CONSTRAINT resulttestcasetag_pkey PRIMARY KEY (run_id, tc_id, name, property),
  CONSTRAINT resulttestcasetag_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_case_tag
  OWNER TO postgres;
-- Table: result_test_steps_list

-- DROP TABLE result_test_steps_list;

CREATE TABLE result_test_steps_list
(
  run_id character varying(100) NOT NULL,
  step_id integer NOT NULL,
  stepname character varying(200) NOT NULL,
  description character varying(200),
  driver character varying(200) NOT NULL,
  steptype character varying(100) NOT NULL,
  data_required boolean,
  stepfeature character varying(200),
  stepenable boolean,
  step_editable boolean,
  case_desc character varying(200),
  expected character varying(200),
  verify_point boolean,
  step_continue boolean,
  estd_time character varying(100),
  CONSTRAINT resultteststepslist_pkey PRIMARY KEY (run_id, step_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_steps_list
  OWNER TO postgres;

-- Table: result_test_steps

-- DROP TABLE result_test_steps;

CREATE TABLE result_test_steps
(
  run_id character varying(100) NOT NULL,
  id integer NOT NULL,
  tc_id character varying(10),
  step_id integer NOT NULL,
  teststepsequence integer,
  test_step_type character varying(20),
  CONSTRAINT resultteststepstemp_pkey PRIMARY KEY (run_id, id),
  CONSTRAINT resultteststepstemp_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT teststepstemp_step_id_fkey FOREIGN KEY (run_id, step_id)
      REFERENCES result_test_steps_list (run_id, step_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT resultteststepstemp_tc_id_step_id_teststepsequence_key UNIQUE (run_id, tc_id, step_id, teststepsequence)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_steps
  OWNER TO postgres;
-- Table: result_test_steps_data

-- DROP TABLE result_test_steps_data;

CREATE TABLE result_test_steps_data
(
  run_id character varying(100) NOT NULL,
  id integer NOT NULL,
  tcdatasetid character varying(20),
  testdatasetid character varying(20) NOT NULL,
  teststepseq integer NOT NULL,
  CONSTRAINT resultteststepdata_pkey PRIMARY KEY (run_id, id),
  CONSTRAINT resultteststepdata_tcdatasetid_fkey FOREIGN KEY (run_id, tcdatasetid)
      REFERENCES result_test_case_datasets (run_id, tcdatasetid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_test_steps_data
  OWNER TO postgres;


-- Table: test_case_results

-- DROP TABLE test_case_results;

CREATE TABLE test_case_results
(
  id integer NOT NULL DEFAULT nextval('testresults_id_seq'::regclass), -- Database index use only
  run_id character varying(100) NOT NULL, -- Run ID for the Current Test Run
  tc_id character varying(20) NOT NULL, -- Test Case ID
  status character varying(20), -- Status = (In-Progress, Submitted, Failed, Passed)
  teststarttime timestamp without time zone, -- Test Start Time
  testendtime timestamp without time zone, -- Test End Time
  duration interval, -- Duration of Test Case to complete
  failreason character varying(200),
  faildetail text,
  logid character varying(150), -- location of log file (zipped format)
  screenshotsid character varying(40),
  automationlogid character varying(40),
  CONSTRAINT testresults_pkey PRIMARY KEY (id),
  CONSTRAINT testresults_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_case_results
  OWNER TO postgres;
GRANT ALL ON TABLE test_case_results TO postgres;
GRANT ALL ON TABLE test_case_results TO public;
COMMENT ON COLUMN test_case_results.id IS 'Database index use only';
COMMENT ON COLUMN test_case_results.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN test_case_results.tc_id IS 'Test Case ID';
COMMENT ON COLUMN test_case_results.status IS 'Status = (In-Progress, Submitted, Failed, Passed)';
COMMENT ON COLUMN test_case_results.teststarttime IS 'Test Start Time';
COMMENT ON COLUMN test_case_results.testendtime IS 'Test End Time';
COMMENT ON COLUMN test_case_results.duration IS 'Duration of Test Case to complete';
COMMENT ON COLUMN test_case_results.logid IS 'location of log file (zipped format)';

-- Table: test_case_tag

-- DROP TABLE test_case_tag;

CREATE TABLE test_case_tag
(
  tc_id character varying(10) NOT NULL, -- Test Case ID
  name character varying(100) NOT NULL, -- Tag Valule
  property character varying(100) NOT NULL,
  CONSTRAINT testcasetag_pkey PRIMARY KEY (tc_id, name, property),
  CONSTRAINT testcasetag_tc_id_fkey FOREIGN KEY (tc_id)
      REFERENCES test_cases (tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_case_tag
  OWNER TO postgres;
COMMENT ON COLUMN test_case_tag.tc_id IS 'Test Case ID';
COMMENT ON COLUMN test_case_tag.name IS 'Tag Valule';


-- Table: test_env_results

-- DROP TABLE test_env_results;

CREATE TABLE test_env_results
(
  id integer NOT NULL DEFAULT nextval('testenvresults_id_seq'::regclass), -- Database index use only
  run_id text NOT NULL, -- Run ID for the Current Test Run
  tester_id character varying(100) NOT NULL, -- Tester User ID
  status character varying(20), -- Status (In-Progress, Complete, Failed, Passed, Submitted)
  teststarttime timestamp without time zone, -- Test Start Time
  testendtime timestamp without time zone, -- Test End Time
  duration interval, -- Duration of Test Case
  rundescription character varying(200), -- Description of the Test Run (test run parameter from the web site)
  CONSTRAINT testenvresults_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_env_results
  OWNER TO postgres;
GRANT ALL ON TABLE test_env_results TO postgres;
GRANT ALL ON TABLE test_env_results TO public;
COMMENT ON COLUMN test_env_results.id IS 'Database index use only';
COMMENT ON COLUMN test_env_results.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN test_env_results.tester_id IS 'Tester User ID';
COMMENT ON COLUMN test_env_results.status IS 'Status (In-Progress, Complete, Failed, Passed, Submitted)';
COMMENT ON COLUMN test_env_results.teststarttime IS 'Test Start Time';
COMMENT ON COLUMN test_env_results.testendtime IS 'Test End Time';
COMMENT ON COLUMN test_env_results.duration IS 'Duration of Test Case';
COMMENT ON COLUMN test_env_results.rundescription IS 'Description of the Test Run (test run parameter from the web site)';

-- Table: test_run

-- DROP TABLE test_run;

CREATE TABLE test_run
(
  id integer NOT NULL DEFAULT nextval('testrun_id_seq'::regclass), -- Database index use only
  run_id character varying(100) NOT NULL, -- Run ID for the Current Test Run
  tc_id character varying(20) NOT NULL, -- Test Case ID
  status character varying(20),
  executiontime date,
  CONSTRAINT testrun_pkey PRIMARY KEY (id),
  CONSTRAINT testrun_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_run
  OWNER TO postgres;
GRANT ALL ON TABLE test_run TO postgres;
GRANT ALL ON TABLE test_run TO public;
COMMENT ON COLUMN test_run.id IS 'Database index use only';
COMMENT ON COLUMN test_run.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN test_run.tc_id IS 'Test Case ID';

-- Table: test_run_env

-- DROP TABLE test_run_env;

CREATE TABLE test_run_env
(
  id integer NOT NULL DEFAULT nextval('testrunenv_id_seq'::regclass), -- Database index use only
  run_id character varying(100), -- Run ID for the Current Test Run
  rundescription character varying(200), -- Description of the Test Run (test run parameter from the web site)
  tester_id character varying(100) NOT NULL, -- User ID of Tester
  status character varying(20), -- Status (Cancelled, Unassigned, In-Progress, Completed)
  test_run_type character varying(100),
  machine_os character varying(100), -- Operating System
  client character varying(100), -- Client (iTunes, WMP, Outlook, etc)
  data_type character varying(100), -- Default
  last_updated_time character varying(255), -- timestamp for last update
  product_version character varying(300), -- Desktop Veriosn
  machine_ip character varying(30), -- IP Address of SUT.
  email_notification text, -- E-mail Notification
  test_objective character varying(50),
  os_version character varying(30),
  os_name character varying(30),
  os_bit character varying(30),
  assigned_tester character varying(50),
  run_type character varying(50),
  test_milestone character varying(100),
  CONSTRAINT testrunenv_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_run_env
  OWNER TO postgres;
GRANT ALL ON TABLE test_run_env TO postgres;
GRANT ALL ON TABLE test_run_env TO public;
COMMENT ON COLUMN test_run_env.id IS 'Database index use only';
COMMENT ON COLUMN test_run_env.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN test_run_env.rundescription IS 'Description of the Test Run (test run parameter from the web site)';
COMMENT ON COLUMN test_run_env.tester_id IS 'User ID of Tester';
COMMENT ON COLUMN test_run_env.status IS 'Status (Cancelled, Unassigned, In-Progress, Completed)';
COMMENT ON COLUMN test_run_env.machine_os IS 'Operating System';
COMMENT ON COLUMN test_run_env.client IS 'Client (iTunes, WMP, Outlook, etc)';
COMMENT ON COLUMN test_run_env.data_type IS 'Default';
COMMENT ON COLUMN test_run_env.last_updated_time IS 'timestamp for last update';
COMMENT ON COLUMN test_run_env.product_version IS 'Desktop Veriosn';
COMMENT ON COLUMN test_run_env.machine_ip IS 'IP Address of SUT.';
COMMENT ON COLUMN test_run_env.email_notification IS 'E-mail Notification';

-- Table: test_step_results

-- DROP TABLE test_step_results;

CREATE TABLE test_step_results
(
  id integer NOT NULL DEFAULT nextval('teststepresults_id_seq'::regclass), -- Database index use only
  run_id character varying(100) NOT NULL, -- Run ID for the Current Test Run
  tc_id character varying(20) NOT NULL, -- Test Case ID
  teststep_id integer NOT NULL, -- Test Step ID
  status character varying(20), -- Test Step Status (Pass, Fail, In-Progress)
  stepstarttime timestamp without time zone, -- Start Time of Test Step
  stependtime timestamp without time zone, -- End Time of Test Step
  duration interval, -- Duration of Test Step
  failreason character varying(200),
  faildetail text,
  logid character varying(100),
  start_memory character varying(100),
  end_memory character varying(100),
  memory_consumed character varying(100), -- memory consumtion metric
  teststepsequence integer, -- Test Step Sequence Number
  testcaseresulttindex integer, -- Test Case Results Index
  CONSTRAINT teststepresults_pkey PRIMARY KEY (id),
  CONSTRAINT teststepresults_tc_id_fkey FOREIGN KEY (run_id, tc_id)
      REFERENCES result_test_cases (run_id, tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_step_results
  OWNER TO postgres;
GRANT ALL ON TABLE test_step_results TO postgres;
GRANT ALL ON TABLE test_step_results TO public;
COMMENT ON COLUMN test_step_results.id IS 'Database index use only';
COMMENT ON COLUMN test_step_results.run_id IS 'Run ID for the Current Test Run';
COMMENT ON COLUMN test_step_results.tc_id IS 'Test Case ID';
COMMENT ON COLUMN test_step_results.teststep_id IS 'Test Step ID';
COMMENT ON COLUMN test_step_results.status IS 'Test Step Status (Pass, Fail, In-Progress)';
COMMENT ON COLUMN test_step_results.stepstarttime IS 'Start Time of Test Step';
COMMENT ON COLUMN test_step_results.stependtime IS 'End Time of Test Step';
COMMENT ON COLUMN test_step_results.duration IS 'Duration of Test Step';
COMMENT ON COLUMN test_step_results.memory_consumed IS 'memory consumtion metric';
COMMENT ON COLUMN test_step_results.teststepsequence IS 'Test Step Sequence Number';
COMMENT ON COLUMN test_step_results.testcaseresulttindex IS 'Test Case Results Index';

-- Table: test_steps_list

-- DROP TABLE test_steps_list;

CREATE TABLE test_steps_list
(
  step_id integer NOT NULL DEFAULT nextval('teststepslist_step_id_seq'::regclass), -- Database use only.
  stepname character varying(200) NOT NULL, -- Name of the Test Stemp...
  description character varying(200),
  driver character varying(200) NOT NULL, -- Test Step functionality area (Music, Picture, Common, PIM)
  steptype character varying(100) NOT NULL, -- Test Step Type (DTS, Client, Common)
  data_required boolean,
  stepfeature character varying(200),
  stepenable boolean,
  step_editable boolean,
  case_desc character varying(200),
  expected character varying(200),
  verify_point boolean,
  step_continue boolean,
  estd_time character varying(100),
  CONSTRAINT teststepslist_pkey PRIMARY KEY (step_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_steps_list
  OWNER TO postgres;
GRANT ALL ON TABLE test_steps_list TO postgres;
GRANT ALL ON TABLE test_steps_list TO public;
COMMENT ON COLUMN test_steps_list.step_id IS 'Database use only.';
COMMENT ON COLUMN test_steps_list.stepname IS 'Name of the Test Stemp
For Example: Open DTS';
COMMENT ON COLUMN test_steps_list.driver IS 'Test Step functionality area (Music, Picture, Common, PIM)';
COMMENT ON COLUMN test_steps_list.steptype IS 'Test Step Type (DTS, Client, Common)';

-- Table: test_steps

-- DROP TABLE test_steps;

CREATE TABLE test_steps
(
  id integer NOT NULL DEFAULT nextval('teststepstemp_id_seq'::regclass), -- Database index use only
  tc_id character varying(10), -- Test Case ID
  step_id integer NOT NULL, -- Test Step ID (A reference to the test_steps_list of test steps)
  teststepsequence integer DEFAULT nextval('teststepstemp_teststepsequence_seq'::regclass), -- Test Step Sequence
  test_step_type character varying(20),
  CONSTRAINT teststepstemp_pkey PRIMARY KEY (id),
  CONSTRAINT teststepstemp_step_id_fkey FOREIGN KEY (step_id)
      REFERENCES test_steps_list (step_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT teststepstemp_tc_id_fkey FOREIGN KEY (tc_id)
      REFERENCES test_cases (tc_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT teststepstemp_tc_id_step_id_teststepsequence_key UNIQUE (tc_id, step_id, teststepsequence)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_steps
  OWNER TO postgres;
GRANT ALL ON TABLE test_steps TO postgres;
GRANT ALL ON TABLE test_steps TO public;
COMMENT ON COLUMN test_steps.id IS 'Database index use only';
COMMENT ON COLUMN test_steps.tc_id IS 'Test Case ID';
COMMENT ON COLUMN test_steps.step_id IS 'Test Step ID (A reference to the test_steps_list of test steps)';
COMMENT ON COLUMN test_steps.teststepsequence IS 'Test Step Sequence';

-- Table: test_steps_data

-- DROP TABLE test_steps_data;

CREATE TABLE test_steps_data
(
  id integer NOT NULL DEFAULT nextval('teststepdata_id_seq'::regclass), -- Database index use only
  tcdatasetid character varying(20), -- Test Case Data Set ID
  testdatasetid character varying(20) NOT NULL, -- Test Data Set ID
  teststepseq integer NOT NULL, -- Test Step Sequence Number
  CONSTRAINT teststepdata_pkey PRIMARY KEY (id),
  CONSTRAINT teststepdata_tcdatasetid_fkey FOREIGN KEY (tcdatasetid)
      REFERENCES test_case_datasets (tcdatasetid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE test_steps_data
  OWNER TO postgres;
COMMENT ON TABLE test_steps_data
  IS 'Contains test step data adn the sequence number
For Example: ';
COMMENT ON COLUMN test_steps_data.id IS 'Database index use only';
COMMENT ON COLUMN test_steps_data.tcdatasetid IS 'Test Case Data Set ID';
COMMENT ON COLUMN test_steps_data.testdatasetid IS 'Test Data Set ID';
COMMENT ON COLUMN test_steps_data.teststepseq IS 'Test Step Sequence Number';

-- Table: user_info

-- DROP TABLE user_info;

CREATE TABLE user_info
(
  username character varying(255) NOT NULL,
  password character varying(255),
  full_name character varying(511),
  CONSTRAINT "user" PRIMARY KEY (username)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_info
  OWNER TO postgres;

