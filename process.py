# convert raw information (already converted into
# required schema by source team) into graph representation
# scholar as node, influence/influenced as edge
#   
# Raw Source Schema (every source team must match this schema):
#       Scholar Name: str
#       LifeSpan: (int, int)
#       Research Field: [str] 
#       Influenced by: [str] (list of Scholar ID)
#       Influences: [str] (list of Scholar ID)
#       MISC information: str
#
# Unified node schema:
#       Node ID: str (GUID/UUID)
#       Type: str ('Scholar', 'Field')
#
#   Field Node Schema:
#       Field: string
#
#   Scholar Node Schema:
#       Scholar Name: str
#       LifeSpan: (int, int)
#       Research Field: [str] 
#       Influenced by: [str] (list of Scholar ID)
#       Influences: [str] (list of Scholar ID)
#       MISC information: str
# 
# Graph Representation: 
#   [str] (A list of UUID/GUID repesenting Scholars)