from src.rmscene import read_blocks
from io import BytesIO
from pathlib import Path

scene_name = "scene1"
DATA_PATH = Path(__file__).parent / "scenes" / scene_name




def id_to_string(id):
    return str(id.part1) + "-" + str(id.part2)

def blocks_to_object(blocks):
    layers = []
    for block in blocks:
        if block.__class__.__name__ == "TreeNodeBlock":
            layer = {"group":id_to_string(block.group.node_id),"lines":[]}
            layers.append(layer)
    for block in blocks:
        if block.__class__.__name__ == "SceneLineItemBlock":
            for layer in layers:
                if id_to_string(block.parent_id) == layer["group"]:
                    if block.item.value:
                        line = {"points":points_to_array(block.item.value.points),"thickness_scale":block.item.value.thickness_scale,"color":block.item.value.color}
                        layer["lines"].append(line)
    return layers

def points_to_array(points):
    arr = []
    for point in points:
        arr.append({"x":point.x,"y":point.y,"speed":point.speed,"direction":point.direction,"width":point.width,"pressure":point.pressure})
    return arr

def save_to_json(data):
    import json
    with open(scene_name+'.json', 'w') as f:
        json.dump(data, f)



obj_list = []
for file_path in DATA_PATH.glob("*.rm"):
    with open(file_path, "rb") as f:
        data = f.read()
    
    input_buf = BytesIO(data)
    blocks = read_blocks(input_buf)
    blocklist = list(blocks)
    obj_list.append(blocks_to_object(blocklist))

save_to_json(obj_list)
print(obj_list)
