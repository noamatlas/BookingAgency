from sql_util import run_query_sql, convert_recordset_to_dict
VALID_COUNTRIES = run_query_sql("SELECT DISTINCT destination AS Countries FROM Vacations", "fetch")
# print(VALID_COUNTRIES)
countries = [row[0] for row in VALID_COUNTRIES]
print(countries)
# countries_dict = convert_recordset_to_dict(VALID_COUNTRIES, ['Countries'])
# print(countries_dict)
# countries_tup = tuple(countries_dict)
# print("-----------")
# print(countries_tup)
# countries_tup = tuple(VALID_COUNTRIES)
# print(countries_tup)