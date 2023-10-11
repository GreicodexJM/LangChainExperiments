extract_json_schema_prompt=f"""
Extract the JSON schema from the data between three backticks.
```{json}```
"""
convert_json2xml_prompt=f"""Convert the following JSON between three backticks into an XML structure that mimics closely the intention and size of the original JSON.
```{json}```
"""
gen_xsdschema_prompt=f"""
Generate an XSD schema from the following xml data:
{xml}
"""
get_code_prompt=f"""
Generate the python code that would generate XML documents that follow the XSD schema provided from JSON documents that follow the JSON-Schema provided between three backticks.
{xsd}
```{jschema}```

Considerations:

- Generalize the code as reusable functions.
- Express the source to target copy rules as a declarative set of rules in an XML document.
- Include error handling in case the json or xml schemas fail to load.
- Include error handling in case the json or xml validations fail.
- Include error handling in case the source to target rules fail to execute.
- Include reading and parsing data from a file indicated in an input_filename variable.
- Include writing the output into corresponding file indicated in the output_filename variable.
- Include reading the rules file into a map_filename variable.

Follow the following procedures:

To generate XML documents that follow the XSD schema provided from JSON documents that follow the JSON-Schema provided, you can use a Python library like `jsonschema` and `xml.etree.ElementTree`. Here are the steps you can follow:

1. Load the JSON-Schema and XSD schema files into Python using the `json.load()` and `xml.etree.ElementTree.parse()` functions, respectively. Handle any errors that may occur during the loading process.

2. Validate the JSON data against the JSON-Schema using the `jsonschema.validate()` function. Handle any errors that may occur during the validation process.

3. Create an XML document using the `xml.etree.ElementTree.Element()` function and set the root element to the `invoices` element defined in the XSD schema.

4. Loop through the JSON data and create XML elements for each invoice and its corresponding lines, buyer, seller, and tax elements. Use the `xml.etree.ElementTree.SubElement()` function to create child elements for each invoice element.

5. Set the text values of the XML elements to the corresponding values in the JSON data.

6. Write the XML document to a file using the `xml.etree.ElementTree.ElementTree().write()` function. Handle any errors that may occur during the writing process.

7. Repeat the process for each JSON file that needs to be converted to XML.

To generalize the code as reusable functions, you can create separate functions for each step of the process and pass in the necessary parameters. For example, you can create a function to load the JSON-Schema and XSD schema files, a function to validate the JSON data, a function to create the XML document, and a function to write the XML document to a file.

To express the source to target copy rules as a declarative set of rules in an XML document, you can create an XML file that defines the mapping between the JSON data and the XML elements. You can then load this file into Python and use it to map the JSON data to the corresponding XML elements.

To include error handling in case the JSON or XML schemas fail to load, you can use a try-except block to catch any errors that may occur during the loading process.

To include error handling in case the JSON or XML validations fail, you can use a try-except block to catch any errors that may occur during the validation process.

To include error handling in case the source to target rules fail to execute, you can use a try-except block to catch any errors that may occur during the mapping process.

To read and parse data from a file indicated in an input_filename variable, you can use the `json.load()` function to load the JSON data from the file.

To write the output into corresponding file indicated in the output_filename variable, you can use the `xml.etree.ElementTree.ElementTree().write()` function to write the XML document to a file.

To read the rules file into a map_filename variable, you can use the `xml.etree.ElementTree.parse()` function to load the XML file into Python.


"""