-- Function: update_test_case_tag()

DROP FUNCTION update_test_case_tag();

CREATE OR REPLACE FUNCTION update_test_case_tag()
  RETURNS void AS
$BODY$
DECLARE
	x record;
	project text;
	type text;
	
 BEGIN
    project:='PROJ-19';
    type:='Project';
    FOR x IN select distinct tc_id from test_cases 
	  LOOP
		insert into test_case_tag(tc_id,name,property) values(x.tc_id,project,type);
	  END LOOP;
    RETURN;
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION update_test_case_tag()
  OWNER TO postgres;

delete from test_case_tag where property='Project';
select update_test_case_tag();
-- Function: update_test_case_tag()

DROP FUNCTION update_test_case_tag();

CREATE OR REPLACE FUNCTION update_test_case_tag()
  RETURNS void AS
$BODY$
DECLARE
	x record;
	project text;
	type text;
	
 BEGIN
    project:='135';
    type:='Team';
    FOR x IN select distinct tc_id from test_cases 
	  LOOP
		insert into test_case_tag(tc_id,name,property) values(x.tc_id,project,type);
	  END LOOP;
    RETURN;
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION update_test_case_tag()
  OWNER TO postgres;
  delete from test_case_tag where property='Team';
  select update_test_case_tag();
  select * from test_case_tag where property='Team';

  insert into team_wise_settings values
('PROJ-19',135,4,'Section'),
('PROJ-19',135,7,'Section'),
('PROJ-19',135,9,'Section'),
('PROJ-19',135,10,'Section');