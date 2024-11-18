from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

# Іменований простір
EX = Namespace("http://example.com/")

# Створення RDF-графу
rdf_graph = Graph()
rdf_graph.bind("ex", EX)

# Додавання основних класів
rdf_graph.add((EX.ElectronicComponent, RDF.type, RDFS.Class))
rdf_graph.add((EX.Transistor, RDF.type, RDFS.Class))
rdf_graph.add((EX.Capacitor, RDF.type, RDFS.Class))
rdf_graph.add((EX.Resistor, RDF.type, RDFS.Class))
rdf_graph.add((EX.Diode, RDF.type, RDFS.Class))

# Додавання підкласів
rdf_graph.add((EX.Transistor, RDFS.subClassOf, EX.ElectronicComponent))
rdf_graph.add((EX.Capacitor, RDFS.subClassOf, EX.ElectronicComponent))
rdf_graph.add((EX.Resistor, RDFS.subClassOf, EX.ElectronicComponent))
rdf_graph.add((EX.Diode, RDFS.subClassOf, EX.ElectronicComponent))

# Додавання індивідуальних об'єктів
# Транзистори
rdf_graph.add((EX.Transistor1, RDF.type, EX.Transistor))
rdf_graph.add((EX.Transistor1, EX.hasVoltage, Literal("5V")))
rdf_graph.add((EX.Transistor1, EX.hasType, Literal("NPN")))

rdf_graph.add((EX.Transistor2, RDF.type, EX.Transistor))
rdf_graph.add((EX.Transistor2, EX.hasVoltage, Literal("3.3V")))
rdf_graph.add((EX.Transistor2, EX.hasType, Literal("PNP")))

# Конденсатори
rdf_graph.add((EX.Capacitor1, RDF.type, EX.Capacitor))
rdf_graph.add((EX.Capacitor1, EX.hasCapacity, Literal("100uF")))
rdf_graph.add((EX.Capacitor1, EX.hasVoltage, Literal("16V")))

rdf_graph.add((EX.Capacitor2, RDF.type, EX.Capacitor))
rdf_graph.add((EX.Capacitor2, EX.hasCapacity, Literal("220uF")))
rdf_graph.add((EX.Capacitor2, EX.hasVoltage, Literal("25V")))

# Резистори
rdf_graph.add((EX.Resistor1, RDF.type, EX.Resistor))
rdf_graph.add((EX.Resistor1, EX.hasResistance, Literal("1kΩ")))
rdf_graph.add((EX.Resistor1, EX.hasPowerRating, Literal("0.25W")))

rdf_graph.add((EX.Resistor2, RDF.type, EX.Resistor))
rdf_graph.add((EX.Resistor2, EX.hasResistance, Literal("10kΩ")))
rdf_graph.add((EX.Resistor2, EX.hasPowerRating, Literal("0.5W")))

# Діоди
rdf_graph.add((EX.Diode1, RDF.type, EX.Diode))
rdf_graph.add((EX.Diode1, EX.hasVoltage, Literal("0.7V")))
rdf_graph.add((EX.Diode1, EX.hasType, Literal("Silicon")))

rdf_graph.add((EX.Diode2, RDF.type, EX.Diode))
rdf_graph.add((EX.Diode2, EX.hasVoltage, Literal("0.3V")))
rdf_graph.add((EX.Diode2, EX.hasType, Literal("Germanium")))

# Збереження у файл
rdf_file_path = "data/knowledge_base.rdf"
rdf_graph.serialize(destination=rdf_file_path, format="xml")

print(f"Розширений RDF файл збережено за адресою: {rdf_file_path}")
