import os
import lxml.etree as ET
from datetime import datetime
from mesh import Mesh
from typing import Tuple, Optional


class LandXML(Mesh):
    def __init__(
        self,
        file_name: Optional[str] = None,
        points: list[Tuple[int, float, float, float]] = [],
        faces: list[Tuple[int, int, int]] = [],
    ):
        super().__init__(file_name, points, faces)

    def _check_file_type(self):
        if not self.file_name.endswith(".xml"):
            raise TypeError("File is not a .xml file: {}".format(self.file_name))

    def _load(self):
        """
        Loads mesh data from a .xml file

        time 11.26 seconds
        """
        ns = {"landxml": "http://www.landxml.org/schema/LandXML-1.2"}

        tree = ET.parse(self.file_name)

        # Get all points
        for point in tree.findall(".//landxml:P", ns):
            point_data = point.text.split()
            self.points.append(
                (
                    int(point.attrib["id"]),
                    float(point_data[0]),
                    float(point_data[1]),
                    float(point_data[2]),
                )
            )

        # Get all faces
        for face in tree.findall(".//landxml:F", ns):
            face_data = face.text.split()
            self.faces.append(
                (
                    int(face_data[0]),
                    int(face_data[1]),
                    int(face_data[2]),
                )
            )

    def _write(self, file_name: str, prec: int = 4):
        """
        Writes mesh data to a .xml file

        time 6.1 seconds
        """

        file_base_name = os.path.split(file_name)[1]
        point_format = f'<P id="{{}}">{{:.{prec}f}} {{:.{prec}f}} {{:.{prec}f}}</P>'
        face_format = "<F>{0:d} {1:d} {2:d}</F>"

        xml_content = [
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<LandXML xsi:schemaLocation="http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.2/LandXML-1.2.xsd" '
            'xmlns="http://www.landxml.org/schema/LandXML-1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" '
            f'date="{datetime.now().strftime("%Y-%m-%d")}" time="{datetime.now().strftime("%H:%M:%S")}">'
            '<Units><Metric areaUnit="squareMeter" linearUnit="meter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="HPA"/></Units>'
            f'<Project name="{file_base_name}"/>'
            '<Application name="Python LandXml2Ply convertor" version="1.0" manufacturer="Exact Control System a.s." manufacturerURL="http://www.exact.com"/>'
            '<Surfaces><Surface name="Surface"><Definition surfType="TIN"><Pnts>'
        ]

        xml_content.extend(point_format.format(*point) for point in self.points)
        xml_content.append("</Pnts><Faces>")
        xml_content.extend(face_format.format(*face) for face in self.faces)
        xml_content.append("</Faces></Definition></Surface></Surfaces></LandXML>")

        # better time performance if we write to file all at once
        with open(f"{file_name}.xml", "w") as f:
            f.writelines(xml_content)

    def _write_secondary(self, file_name: str, prec: int = 4):
        """

        :param file_name: _description_
        :param prec: _description_, defaults to 4
        """

        file_base_name = os.path.split(file_name)[1]
        point_format = f'<P id="{{}}">{{:.{prec}f}} {{:.{prec}f}} {{:.{prec}f}}</P>'
        face_format = "<F>{0:d} {1:d} {2:d}</F>"

        with open(f"{file_name}.xml", "w") as f:
            f.writelines(
                [
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<LandXML xsi:schemaLocation="http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.2/LandXML-1.2.xsd" '
                    'xmlns="http://www.landxml.org/schema/LandXML-1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" '
                    f'date="{datetime.now().strftime("%Y-%m-%d")}" time="{datetime.now().strftime("%H:%M:%S")}">'
                    '<Units><Metric areaUnit="squareMeter" linearUnit="meter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="HPA"/></Units>'
                    f'<Project name="{file_base_name}"/>'
                    '<Application name="Python LandXml2Ply convertor" version="1.0" manufacturer="Exact Control System a.s." manufacturerURL="http://www.exact.com"/>'
                    '<Surfaces><Surface name="Surface"><Definition surfType="TIN"><Pnts>'
                ]
            )

            # write points
            for point in self.points:
                f.write(point_format.format(*point))

            f.write("</Pnts><Faces>")

            # write faces
            for face in self.faces:
                f.write(face_format.format(*face))

            f.write("</Faces></Definition></Surface></Surfaces></LandXML>")
