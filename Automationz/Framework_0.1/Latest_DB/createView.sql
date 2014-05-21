-- View: test

--DROP VIEW test;

CREATE OR REPLACE VIEW test AS 
 SELECT testcases.tc_id, 
    testcases.tc_name, 
    testcases.tc_type, 
    testcases.tc_executiontype, 
    testcases.tc_priority, 
    testcases.tc_localization, 
    testcases.tc_createdby, 
    testcases.tc_creationdate, 
    testcases.tc_modifiedby, 
    testcases.tc_modifydate, 
    testcases.defectid, 
    testcases.prd_no
   FROM test_cases testcases;

ALTER TABLE test
  OWNER TO postgres;
-- Rule: "_RETURN" ON test

--DROP RULE "_RETURN" ON test;

CREATE OR REPLACE RULE "_RETURN" AS
    ON SELECT TO test DO INSTEAD  SELECT testcases.tc_id, 
    testcases.tc_name, 
    testcases.tc_type, 
    testcases.tc_executiontype, 
    testcases.tc_priority, 
    testcases.tc_localization, 
    testcases.tc_createdby, 
    testcases.tc_creationdate, 
    testcases.tc_modifiedby, 
    testcases.tc_modifydate, 
    testcases.defectid, 
    testcases.prd_no
   FROM test_cases testcases;
