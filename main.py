import time
from landxml import LandXML
from ply import Ply

if __name__ == "__main__":
    """
    Testing conversion from landxml to ply
    """

    start_load = time.time()
    input_file = "stenungsund_design.xml"
    print("Loading landxml")
    xml = LandXML(input_file)
    print(f"Time to load landxml: {time.time() - start_load}")

    start_convert = time.time()

    ply = Ply(points=xml.points, faces=xml.faces)

    print("Converting to ply")
    ply.write_data("stenungsund_design_converted.ply")
    print(f"Time to save to ply: {time.time() - start_convert}")
