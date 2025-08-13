import shapefile
from shapely.geometry import Polygon, Point
from config import PGW_PATH
# Transform coordinates from UTM to pixel using the .pgw file
def load_world_file(pgw_path):
    with open(pgw_path) as f:
        A = float(f.readline())
        D = float(f.readline())
        B = float(f.readline())
        E = float(f.readline())
        C = float(f.readline())
        F = float(f.readline())
    return A, D, B, E, C, F
A, D, B, E, C, F = load_world_file(PGW_PATH)
def pixel_to_map(x_pix, y_pix):
    x_map = A * x_pix + B * y_pix + C
    y_map = D * x_pix + E * y_pix + F
    return x_map, y_map

def map_to_pixel(x_map, y_map):
    det = A * E - B * D
    x_pix = (E * (x_map - C) - B * (y_map - F)) / det
    y_pix = (-D * (x_map - C) + A * (y_map - F)) / det
    return x_pix, y_pix

class TerrainMap:
    def __init__(self, filepath):
        self.shapes = []
        self.symbols = []
        
        sf = shapefile.Reader(filepath, encoding="latin1")
        fields = [field[0] for field in sf.fields[1:]]

        print("Loaded terrain areas:")
        for i, record in enumerate(self.symbols[:5]):
            print(f"  {i}: {record.get('Name', 'Unknown')}")

        for record, shp in zip(sf.records(), sf.shapes()):
            record_dict = dict(zip(fields, record))
            if shp.shapeType == shapefile.POLYGON:
                transformed_points = [map_to_pixel(x, y) for x, y in shp.points]
                polygon = Polygon(transformed_points)
                self.shapes.append(polygon)
                self.symbols.append(record_dict)

    def get_speed_multiplier(self, map_x, map_y):
        x, y = map_to_pixel(map_x, map_y)
        point = Point(x, y)
        for i, polygon in enumerate(self.shapes):
            if polygon.contains(point):
                symbol_name = self.symbols[i].get("Name", "")
                return self.map_symbol_to_speed(symbol_name) or 1.0
        return 1.0
    
    def get_terrain_type(self, map_x, map_y):
        x, y = map_to_pixel(map_x, map_y)
        point = Point(x, y)
        closest_name = None
        closest_distance = float("inf")

        for i, polygon in enumerate(self.shapes):
            attributes = self.symbols[i]
            name = attributes.get("Name", "Unnamed")

            if polygon.contains(point):
                return name

            distance = polygon.distance(point)
            if distance < closest_distance:
                closest_distance = distance
                closest_name = name

        return closest_name or "Unknown"

    
    def map_symbol_to_speed(self, symbol):
        symbol = str(symbol).lower()
        
        if "upasserbart vann" in symbol or "vann" in symbol:
            return 0.5
        elif "myr" in symbol:
            return 0.5
        elif "vann" in symbol or "innsjø" in symbol:
            return 0.5 
        elif "åpent, lettløpt" in symbol:
            return 1.2
        elif "vegetasjon, god sikt" in symbol:
            return 1.0
        elif "vegetasjon" in symbol:
            return 0.7
        elif "bygning" in symbol or "forbudt" in symbol:
            return 0.5  # impassable
        elif "fast dekke" in symbol:
            return 1.3
        elif "berg i dagen" in symbol:
            return 1.0
        elif "Dominerende upasserbart vann 70%" in symbol:
            return 1.0
        return 1.0
