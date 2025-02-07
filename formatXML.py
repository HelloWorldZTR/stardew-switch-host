import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

def format_xml(input_file, output_file):
    # 解析XML文件
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 将树结构转换为字符串
    rough_string = ET.tostring(root, 'utf-8')

    # 使用minidom进行格式化
    reparsed = minidom.parseString(rough_string)
    formatted_string = reparsed.toprettyxml(indent="  ")

    # 写入格式化后的内容到输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(formatted_string)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python formatXML.py <input_file>")
        sys.exit(1)
    input_file = args[1]
    output_file = f"{input_file}_formated.xml"  # 输出格式化后的文件路径
    format_xml(input_file, output_file)

    print('File has been saved to ', output_file)
