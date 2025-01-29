# SPDX-FileCopyrightText: 2023 Marcel Parciak <marcel.parciak@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import io
import xml.etree.ElementTree as ET

from typing import Any, Dict, List


def is_table(element: ET.Element) -> bool:
    """Returns True if element is a table, False otherwise."""
    return ("style" in element.attrib) and ("shape=table;" in element.attrib["style"])


def get_tables(root_element: ET.Element) -> List[ET.Element]:
    """Returns a list of table elements."""
    return list(filter(is_table, root_element.findall("./mxCell")))


def get_attribute_containers(
        table_element: ET.Element, root_element: ET.Element
) -> List[ET.Element]:
    """Returns a list of container elements that contain attributes."""
    table_id = table_element.attrib["id"]
    return root_element.findall(f"./mxCell[@parent='{table_id}']")


def get_attribute_dict(
        attribute_container: ET.Element, root_element: ET.Element
) -> Dict[str, str]:
    """Transforms an attribute container into a descriptive dictionary."""
    attribute_id = attribute_container.attrib["id"]
    attribute_dict = {
        "id": attribute_id,
    }
    for attribute in root_element.findall(f"./mxCell[@parent='{attribute_id}']"):
        if float(attribute.find("./mxGeometry").attrib["width"]) < 100.0:
            attribute_dict["key"] = attribute.attrib.get("value", None)
        else:
            descriptor = attribute.get("value", None)
            if descriptor and " " in descriptor:
                attribute_dict["name"] = descriptor.split(" ")[0]
                attribute_dict["type"] = descriptor.split(" ")[1]
                attribute_dict["notnull"] = "NOT NULL" in descriptor
    return attribute_dict


def get_relationships(root_element: ET.Element) -> List[ET.Element]:
    """Returns a list of relationships."""
    return list(
        filter(
            lambda e: ("style" in e.attrib) and ("edge" in e.attrib["style"]),
            root_element.findall("./mxCell"),
        )
    )


def get_relationship_dict(
        relationship_element: ET.Element, root_element: ET.Element
) -> Dict[str, str]:
    """Transforms a relationship element into a descriptive dictionary."""
    source_attribute = None
    source_table_name = None
    target_attribute = None
    target_table_name = None

    source_id = relationship_element.attrib.get("source", None)
    if source_id:
        source_element = root_element.find(f"./mxCell[@id='{source_id}']")
        source_table_name = root_element.find(
            f"./mxCell[@id='{source_element.attrib['parent']}']"
        ).attrib["value"]
        source_attribute = get_attribute_dict(source_element, root_element)
    target_id = relationship_element.attrib.get("target", None)
    if target_id:
        target_element = root_element.find(f"./mxCell[@id='{target_id}']")
        target_table_name = root_element.find(
            f"./mxCell[@id='{target_element.attrib['parent']}']"
        ).attrib["value"]
        target_attribute = get_attribute_dict(target_element, root_element)
    relationship_dict = {
        "source_id": source_id,
        "source_name": source_attribute.get("name", None) if source_attribute else None,
        "source_table_name": source_table_name if source_table_name else None,
        "target_id": target_id,
        "target_name": target_attribute.get("name", None) if target_attribute else None,
        "target_table_name": target_table_name,
    }
    return relationship_dict


def parse_drawio(xml_file: str, sheet_name: str):
    """Parse a DrawIO file and return a dictionary representing the ER diagram."""
    tree = ET.parse(xml_file)
    root = tree.getroot().find(f"./diagram[@name='{sheet_name}']/mxGraphModel/root")
    er = {}
    tables = get_tables(root)
    for table in tables:
        attributes = list(
            map(
                lambda a: get_attribute_dict(a, root),
                get_attribute_containers(table, root),
            )
        )
        er[table.attrib["value"]] = {"attributes": attributes}
    er["constraints"] = list(
        map(lambda r: get_relationship_dict(r, root), get_relationships(root))
    )
    return er


def er_to_sql(er: Dict[str, Any]) -> str:
    """Transforms an ER diagram into a SQL CREATE script."""
    table_sqls = {}
    dependencies = []
    for table_name, table_er in er.items():
        sql = io.StringIO()
        if table_name == "constraints":
            continue
        sql.write(f"CREATE TABLE {table_name} (\n")
        first = True
        for attribute in table_er["attributes"]:
            if first:
                first = False
            else:
                sql.write(",\n")
            datatype = attribute.get("type", "")
            if datatype == "datetime":  # clean for PostgreSQL
                datatype = "timestamp"
            sql.write(f"    {attribute.get('name', "")} {datatype}")
            if attribute["key"] == "PK":
                sql.write(" PRIMARY KEY")
            if attribute.get("notnull", False):
                sql.write(" NOT NULL")
            if attribute["key"] == "FK":
                constraint = next(
                    filter(
                        lambda c: c["source_id"] == attribute["id"], er["constraints"]
                    )
                )
                sql.write(
                    f" REFERENCES {constraint['target_table_name']} ({constraint['target_name']})"
                )
                dependencies.append(
                    (table_name, "depends_on", constraint["target_table_name"])
                )
        sql.write("\n);")
        table_sqls[table_name] = sql.getvalue()
    tables = list(table_sqls.keys())
    for dependency in dependencies:
        if tables.index(dependency[0]) < tables.index(dependency[2]):
            tables.insert(
                tables.index(dependency[2]), tables.pop(tables.index(dependency[0]))
            )  # move behind table it depends on
    return "\n\n".join(map(lambda t: table_sqls[t], tables))


if __name__ == "__main__":
    choice = 1
    filename="data_model"
    if choice == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument(filename, help="Path to drawio file")
        parser.add_argument("V4 - Évolution fonctionnalités", help="Name of diagram sheet in drawio file")
        print(parser)
        args = parser.parse_args()
        print(args)
        er = parse_drawio(args.drawio_file, args.sheet_name)
        print(er_to_sql(er))

    # Exportation en SQL après export en XML
    elif choice == 1:
        er = parse_drawio(f"{filename}.drawio.xml", "V4 - Évolution fonctionnalités")
        print(er_to_sql(er))