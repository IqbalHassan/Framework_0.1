-- Function: _lt_q_regex(ltree[], lquery[])

-- DROP FUNCTION _lt_q_regex(ltree[], lquery[]);

CREATE OR REPLACE FUNCTION _lt_q_regex(ltree[], lquery[])
  RETURNS boolean AS
'$libdir/ltree', '_lt_q_regex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _lt_q_regex(ltree[], lquery[])
  OWNER TO postgres;

-- Function: _lt_q_rregex(lquery[], ltree[])

-- DROP FUNCTION _lt_q_rregex(lquery[], ltree[]);

CREATE OR REPLACE FUNCTION _lt_q_rregex(lquery[], ltree[])
  RETURNS boolean AS
'$libdir/ltree', '_lt_q_rregex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _lt_q_rregex(lquery[], ltree[])
  OWNER TO postgres;

-- Function: _ltq_extract_regex(ltree[], lquery)

-- DROP FUNCTION _ltq_extract_regex(ltree[], lquery);

CREATE OR REPLACE FUNCTION _ltq_extract_regex(ltree[], lquery)
  RETURNS ltree AS
'$libdir/ltree', '_ltq_extract_regex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltq_extract_regex(ltree[], lquery)
  OWNER TO postgres;
-- Function: _ltq_regex(ltree[], lquery)

-- DROP FUNCTION _ltq_regex(ltree[], lquery);

CREATE OR REPLACE FUNCTION _ltq_regex(ltree[], lquery)
  RETURNS boolean AS
'$libdir/ltree', '_ltq_regex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltq_regex(ltree[], lquery)
  OWNER TO postgres;
-- Function: _ltq_rregex(lquery, ltree[])

-- DROP FUNCTION _ltq_rregex(lquery, ltree[]);

CREATE OR REPLACE FUNCTION _ltq_rregex(lquery, ltree[])
  RETURNS boolean AS
'$libdir/ltree', '_ltq_rregex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltq_rregex(lquery, ltree[])
  OWNER TO postgres;
-- Function: _ltree_compress(internal)

-- DROP FUNCTION _ltree_compress(internal);

CREATE OR REPLACE FUNCTION _ltree_compress(internal)
  RETURNS internal AS
'$libdir/ltree', '_ltree_compress'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_compress(internal)
  OWNER TO postgres;
-- Function: _ltree_consistent(internal, internal, smallint, oid, internal)

-- DROP FUNCTION _ltree_consistent(internal, internal, smallint, oid, internal);

CREATE OR REPLACE FUNCTION _ltree_consistent(internal, internal, smallint, oid, internal)
  RETURNS boolean AS
'$libdir/ltree', '_ltree_consistent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_consistent(internal, internal, smallint, oid, internal)
  OWNER TO postgres;
-- Function: _ltree_extract_isparent(ltree[], ltree)

-- DROP FUNCTION _ltree_extract_isparent(ltree[], ltree);

CREATE OR REPLACE FUNCTION _ltree_extract_isparent(ltree[], ltree)
  RETURNS ltree AS
'$libdir/ltree', '_ltree_extract_isparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_extract_isparent(ltree[], ltree)
  OWNER TO postgres;
-- Function: _ltree_extract_risparent(ltree[], ltree)

-- DROP FUNCTION _ltree_extract_risparent(ltree[], ltree);

CREATE OR REPLACE FUNCTION _ltree_extract_risparent(ltree[], ltree)
  RETURNS ltree AS
'$libdir/ltree', '_ltree_extract_risparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_extract_risparent(ltree[], ltree)
  OWNER TO postgres;
-- Function: _ltree_isparent(ltree[], ltree)

-- DROP FUNCTION _ltree_isparent(ltree[], ltree);

CREATE OR REPLACE FUNCTION _ltree_isparent(ltree[], ltree)
  RETURNS boolean AS
'$libdir/ltree', '_ltree_isparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_isparent(ltree[], ltree)
  OWNER TO postgres;
-- Function: _ltree_penalty(internal, internal, internal)

-- DROP FUNCTION _ltree_penalty(internal, internal, internal);

CREATE OR REPLACE FUNCTION _ltree_penalty(internal, internal, internal)
  RETURNS internal AS
'$libdir/ltree', '_ltree_penalty'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_penalty(internal, internal, internal)
  OWNER TO postgres;
-- Function: _ltree_picksplit(internal, internal)

-- DROP FUNCTION _ltree_picksplit(internal, internal);

CREATE OR REPLACE FUNCTION _ltree_picksplit(internal, internal)
  RETURNS internal AS
'$libdir/ltree', '_ltree_picksplit'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_picksplit(internal, internal)
  OWNER TO postgres;
-- Function: _ltree_r_isparent(ltree, ltree[])

-- DROP FUNCTION _ltree_r_isparent(ltree, ltree[]);

CREATE OR REPLACE FUNCTION _ltree_r_isparent(ltree, ltree[])
  RETURNS boolean AS
'$libdir/ltree', '_ltree_r_isparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_r_isparent(ltree, ltree[])
  OWNER TO postgres;
-- Function: _ltree_r_risparent(ltree, ltree[])

-- DROP FUNCTION _ltree_r_risparent(ltree, ltree[]);

CREATE OR REPLACE FUNCTION _ltree_r_risparent(ltree, ltree[])
  RETURNS boolean AS
'$libdir/ltree', '_ltree_r_risparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_r_risparent(ltree, ltree[])
  OWNER TO postgres;
-- Function: _ltree_risparent(ltree[], ltree)

-- DROP FUNCTION _ltree_risparent(ltree[], ltree);

CREATE OR REPLACE FUNCTION _ltree_risparent(ltree[], ltree)
  RETURNS boolean AS
'$libdir/ltree', '_ltree_risparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_risparent(ltree[], ltree)
  OWNER TO postgres;
-- Function: _ltree_same(internal, internal, internal)

-- DROP FUNCTION _ltree_same(internal, internal, internal);

CREATE OR REPLACE FUNCTION _ltree_same(internal, internal, internal)
  RETURNS internal AS
'$libdir/ltree', '_ltree_same'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_same(internal, internal, internal)
  OWNER TO postgres;
-- Function: _ltree_union(internal, internal)

-- DROP FUNCTION _ltree_union(internal, internal);

CREATE OR REPLACE FUNCTION _ltree_union(internal, internal)
  RETURNS integer AS
'$libdir/ltree', '_ltree_union'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltree_union(internal, internal)
  OWNER TO postgres;
-- Function: _ltxtq_exec(ltree[], ltxtquery)

-- DROP FUNCTION _ltxtq_exec(ltree[], ltxtquery);

CREATE OR REPLACE FUNCTION _ltxtq_exec(ltree[], ltxtquery)
  RETURNS boolean AS
'$libdir/ltree', '_ltxtq_exec'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltxtq_exec(ltree[], ltxtquery)
  OWNER TO postgres;
-- Function: _ltxtq_extract_exec(ltree[], ltxtquery)

-- DROP FUNCTION _ltxtq_extract_exec(ltree[], ltxtquery);

CREATE OR REPLACE FUNCTION _ltxtq_extract_exec(ltree[], ltxtquery)
  RETURNS ltree AS
'$libdir/ltree', '_ltxtq_extract_exec'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltxtq_extract_exec(ltree[], ltxtquery)
  OWNER TO postgres;
-- Function: _ltxtq_rexec(ltxtquery, ltree[])

-- DROP FUNCTION _ltxtq_rexec(ltxtquery, ltree[]);

CREATE OR REPLACE FUNCTION _ltxtq_rexec(ltxtquery, ltree[])
  RETURNS boolean AS
'$libdir/ltree', '_ltxtq_rexec'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION _ltxtq_rexec(ltxtquery, ltree[])
  OWNER TO postgres;
-- Function: changedatastructure(text, text)

-- DROP FUNCTION changedatastructure(text, text);

CREATE OR REPLACE FUNCTION changedatastructure(oldval text, newval text)
  RETURNS void AS
$BODY$

Update master_data set id = $2 where id = $1 and field in ('Other Street Address','Other City','Other State-Prov-Region','Other Zip-Postal Code','Other Country');
insert into master_data (id, field, value) values ($1, 'Other Address', $2);
Update master_data set field = substr(field,6) where id = $2 and field in ('Other Street Address','Other City','Other State-Prov-Region','Other Zip-Postal Code','Other Country');

$BODY$
  LANGUAGE sql VOLATILE
  COST 100;
ALTER FUNCTION changedatastructure(text, text)
  OWNER TO postgres;
-- Function: index(ltree, ltree)

-- DROP FUNCTION index(ltree, ltree);

CREATE OR REPLACE FUNCTION index(ltree, ltree)
  RETURNS integer AS
'$libdir/ltree', 'ltree_index'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION index(ltree, ltree)
  OWNER TO postgres;
-- Function: index(ltree, ltree, integer)

-- DROP FUNCTION index(ltree, ltree, integer);

CREATE OR REPLACE FUNCTION index(ltree, ltree, integer)
  RETURNS integer AS
'$libdir/ltree', 'ltree_index'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION index(ltree, ltree, integer)
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree, ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree)
  OWNER TO postgres;
-- Function: lca(ltree[])

-- DROP FUNCTION lca(ltree[]);

CREATE OR REPLACE FUNCTION lca(ltree[])
  RETURNS ltree AS
'$libdir/ltree', '_lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree[])
  OWNER TO postgres;
-- Function: lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree)

-- DROP FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree);

CREATE OR REPLACE FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'lca'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lca(ltree, ltree, ltree, ltree, ltree, ltree, ltree)
  OWNER TO postgres;
-- Function: lquery_in(cstring)

-- DROP FUNCTION lquery_in(cstring);

CREATE OR REPLACE FUNCTION lquery_in(cstring)
  RETURNS lquery AS
'$libdir/ltree', 'lquery_in'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION lquery_in(cstring)
  OWNER TO postgres;
-- Function: lquery_out(lquery)

-- DROP FUNCTION lquery_out(lquery);

CREATE OR REPLACE FUNCTION lquery_out(lquery)
  RETURNS cstring AS
'$libdir/ltree', 'lquery_out'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION lquery_out(lquery)
  OWNER TO postgres;
-- Function: lt_q_regex(ltree, lquery[])

-- DROP FUNCTION lt_q_regex(ltree, lquery[]);

CREATE OR REPLACE FUNCTION lt_q_regex(ltree, lquery[])
  RETURNS boolean AS
'$libdir/ltree', 'lt_q_regex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lt_q_regex(ltree, lquery[])
  OWNER TO postgres;
-- Function: lt_q_rregex(lquery[], ltree)

-- DROP FUNCTION lt_q_rregex(lquery[], ltree);

CREATE OR REPLACE FUNCTION lt_q_rregex(lquery[], ltree)
  RETURNS boolean AS
'$libdir/ltree', 'lt_q_rregex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION lt_q_rregex(lquery[], ltree)
  OWNER TO postgres;
-- Function: ltq_regex(ltree, lquery)

-- DROP FUNCTION ltq_regex(ltree, lquery);

CREATE OR REPLACE FUNCTION ltq_regex(ltree, lquery)
  RETURNS boolean AS
'$libdir/ltree', 'ltq_regex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltq_regex(ltree, lquery)
  OWNER TO postgres;
-- Function: ltq_rregex(lquery, ltree)

-- DROP FUNCTION ltq_rregex(lquery, ltree);

CREATE OR REPLACE FUNCTION ltq_rregex(lquery, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltq_rregex'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltq_rregex(lquery, ltree)
  OWNER TO postgres;
-- Function: ltree2text(ltree)

-- DROP FUNCTION ltree2text(ltree);

CREATE OR REPLACE FUNCTION ltree2text(ltree)
  RETURNS text AS
'$libdir/ltree', 'ltree2text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree2text(ltree)
  OWNER TO postgres;
-- Function: ltree_addltree(ltree, ltree)

-- DROP FUNCTION ltree_addltree(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_addltree(ltree, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'ltree_addltree'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_addltree(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_addtext(ltree, text)

-- DROP FUNCTION ltree_addtext(ltree, text);

CREATE OR REPLACE FUNCTION ltree_addtext(ltree, text)
  RETURNS ltree AS
'$libdir/ltree', 'ltree_addtext'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_addtext(ltree, text)
  OWNER TO postgres;
-- Function: ltree_cmp(ltree, ltree)

-- DROP FUNCTION ltree_cmp(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_cmp(ltree, ltree)
  RETURNS integer AS
'$libdir/ltree', 'ltree_cmp'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_cmp(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_compress(internal)

-- DROP FUNCTION ltree_compress(internal);

CREATE OR REPLACE FUNCTION ltree_compress(internal)
  RETURNS internal AS
'$libdir/ltree', 'ltree_compress'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_compress(internal)
  OWNER TO postgres;
-- Function: ltree_consistent(internal, internal, smallint, oid, internal)

-- DROP FUNCTION ltree_consistent(internal, internal, smallint, oid, internal);

CREATE OR REPLACE FUNCTION ltree_consistent(internal, internal, smallint, oid, internal)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_consistent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_consistent(internal, internal, smallint, oid, internal)
  OWNER TO postgres;
-- Function: ltree_decompress(internal)

-- DROP FUNCTION ltree_decompress(internal);

CREATE OR REPLACE FUNCTION ltree_decompress(internal)
  RETURNS internal AS
'$libdir/ltree', 'ltree_decompress'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_decompress(internal)
  OWNER TO postgres;
-- Function: ltree_eq(ltree, ltree)

-- DROP FUNCTION ltree_eq(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_eq(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_eq'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_eq(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_ge(ltree, ltree)

-- DROP FUNCTION ltree_ge(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_ge(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_ge'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_ge(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_gist_in(cstring)

-- DROP FUNCTION ltree_gist_in(cstring);

CREATE OR REPLACE FUNCTION ltree_gist_in(cstring)
  RETURNS ltree_gist AS
'$libdir/ltree', 'ltree_gist_in'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltree_gist_in(cstring)
  OWNER TO postgres;
-- Function: ltree_gist_out(ltree_gist)

-- DROP FUNCTION ltree_gist_out(ltree_gist);

CREATE OR REPLACE FUNCTION ltree_gist_out(ltree_gist)
  RETURNS cstring AS
'$libdir/ltree', 'ltree_gist_out'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltree_gist_out(ltree_gist)
  OWNER TO postgres;
-- Function: ltree_gt(ltree, ltree)

-- DROP FUNCTION ltree_gt(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_gt(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_gt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_gt(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_in(cstring)

-- DROP FUNCTION ltree_in(cstring);

CREATE OR REPLACE FUNCTION ltree_in(cstring)
  RETURNS ltree AS
'$libdir/ltree', 'ltree_in'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltree_in(cstring)
  OWNER TO postgres;
-- Function: ltree_isparent(ltree, ltree)

-- DROP FUNCTION ltree_isparent(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_isparent(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_isparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_isparent(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_le(ltree, ltree)

-- DROP FUNCTION ltree_le(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_le(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_le'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_le(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_lt(ltree, ltree)

-- DROP FUNCTION ltree_lt(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_lt(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_lt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_lt(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_ne(ltree, ltree)

-- DROP FUNCTION ltree_ne(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_ne(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_ne'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_ne(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_out(ltree)

-- DROP FUNCTION ltree_out(ltree);

CREATE OR REPLACE FUNCTION ltree_out(ltree)
  RETURNS cstring AS
'$libdir/ltree', 'ltree_out'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltree_out(ltree)
  OWNER TO postgres;
-- Function: ltree_penalty(internal, internal, internal)

-- DROP FUNCTION ltree_penalty(internal, internal, internal);

CREATE OR REPLACE FUNCTION ltree_penalty(internal, internal, internal)
  RETURNS internal AS
'$libdir/ltree', 'ltree_penalty'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_penalty(internal, internal, internal)
  OWNER TO postgres;
-- Function: ltree_picksplit(internal, internal)

-- DROP FUNCTION ltree_picksplit(internal, internal);

CREATE OR REPLACE FUNCTION ltree_picksplit(internal, internal)
  RETURNS internal AS
'$libdir/ltree', 'ltree_picksplit'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_picksplit(internal, internal)
  OWNER TO postgres;
-- Function: ltree_risparent(ltree, ltree)

-- DROP FUNCTION ltree_risparent(ltree, ltree);

CREATE OR REPLACE FUNCTION ltree_risparent(ltree, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltree_risparent'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_risparent(ltree, ltree)
  OWNER TO postgres;
-- Function: ltree_same(internal, internal, internal)

-- DROP FUNCTION ltree_same(internal, internal, internal);

CREATE OR REPLACE FUNCTION ltree_same(internal, internal, internal)
  RETURNS internal AS
'$libdir/ltree', 'ltree_same'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_same(internal, internal, internal)
  OWNER TO postgres;
-- Function: ltree_textadd(text, ltree)

-- DROP FUNCTION ltree_textadd(text, ltree);

CREATE OR REPLACE FUNCTION ltree_textadd(text, ltree)
  RETURNS ltree AS
'$libdir/ltree', 'ltree_textadd'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_textadd(text, ltree)
  OWNER TO postgres;
-- Function: ltree_union(internal, internal)

-- DROP FUNCTION ltree_union(internal, internal);

CREATE OR REPLACE FUNCTION ltree_union(internal, internal)
  RETURNS integer AS
'$libdir/ltree', 'ltree_union'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltree_union(internal, internal)
  OWNER TO postgres;
-- Function: ltreeparentsel(internal, oid, internal, integer)

-- DROP FUNCTION ltreeparentsel(internal, oid, internal, integer);

CREATE OR REPLACE FUNCTION ltreeparentsel(internal, oid, internal, integer)
  RETURNS double precision AS
'$libdir/ltree', 'ltreeparentsel'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltreeparentsel(internal, oid, internal, integer)
  OWNER TO postgres;
-- Function: ltxtq_exec(ltree, ltxtquery)

-- DROP FUNCTION ltxtq_exec(ltree, ltxtquery);

CREATE OR REPLACE FUNCTION ltxtq_exec(ltree, ltxtquery)
  RETURNS boolean AS
'$libdir/ltree', 'ltxtq_exec'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltxtq_exec(ltree, ltxtquery)
  OWNER TO postgres;
-- Function: ltxtq_in(cstring)

-- DROP FUNCTION ltxtq_in(cstring);

CREATE OR REPLACE FUNCTION ltxtq_in(cstring)
  RETURNS ltxtquery AS
'$libdir/ltree', 'ltxtq_in'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltxtq_in(cstring)
  OWNER TO postgres;
-- Function: ltxtq_out(ltxtquery)

-- DROP FUNCTION ltxtq_out(ltxtquery);

CREATE OR REPLACE FUNCTION ltxtq_out(ltxtquery)
  RETURNS cstring AS
'$libdir/ltree', 'ltxtq_out'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION ltxtq_out(ltxtquery)
  OWNER TO postgres;
-- Function: ltxtq_rexec(ltxtquery, ltree)

-- DROP FUNCTION ltxtq_rexec(ltxtquery, ltree);

CREATE OR REPLACE FUNCTION ltxtq_rexec(ltxtquery, ltree)
  RETURNS boolean AS
'$libdir/ltree', 'ltxtq_rexec'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION ltxtq_rexec(ltxtquery, ltree)
  OWNER TO postgres;
-- Function: nlevel(ltree)

-- DROP FUNCTION nlevel(ltree);

CREATE OR REPLACE FUNCTION nlevel(ltree)
  RETURNS integer AS
'$libdir/ltree', 'nlevel'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION nlevel(ltree)
  OWNER TO postgres;
-- Function: subltree(ltree, integer, integer)

-- DROP FUNCTION subltree(ltree, integer, integer);

CREATE OR REPLACE FUNCTION subltree(ltree, integer, integer)
  RETURNS ltree AS
'$libdir/ltree', 'subltree'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION subltree(ltree, integer, integer)
  OWNER TO postgres;
-- Function: subpath(ltree, integer)

-- DROP FUNCTION subpath(ltree, integer);

CREATE OR REPLACE FUNCTION subpath(ltree, integer)
  RETURNS ltree AS
'$libdir/ltree', 'subpath'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION subpath(ltree, integer)
  OWNER TO postgres;
-- Function: subpath(ltree, integer, integer)

-- DROP FUNCTION subpath(ltree, integer, integer);

CREATE OR REPLACE FUNCTION subpath(ltree, integer, integer)
  RETURNS ltree AS
'$libdir/ltree', 'subpath'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION subpath(ltree, integer, integer)
  OWNER TO postgres;
-- Function: text2ltree(text)

-- DROP FUNCTION text2ltree(text);

CREATE OR REPLACE FUNCTION text2ltree(text)
  RETURNS ltree AS
'$libdir/ltree', 'text2ltree'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION text2ltree(text)
  OWNER TO postgres;
-- Function: truncate_tables(character varying)

-- DROP FUNCTION truncate_tables(character varying);

CREATE OR REPLACE FUNCTION truncate_tables(username character varying)
  RETURNS void AS
$BODY$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables
        WHERE tableowner = username AND schemaname = 'public';
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION truncate_tables(character varying)
  OWNER TO postgres;
