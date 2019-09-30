# import Utils.Storage as Storage
import xmlschema

schema = xmlschema.XMLSchema('xml_schemas/sports_schema.xsd')
is_valid = schema.validate('<aiml><category></category></aiml>')
print(is_valid)
