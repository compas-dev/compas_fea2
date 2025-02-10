import h5py
from compas_fea2.model import Model, Part, Node

output_path = "/Users/francesco/code/fea2/compas_fea2/scripts/node.hdf5"
# output_path = "/Users/francesco/code/fea2/compas_fea2/scripts/node.json"

# Create and save the node
node = Node([0.0, 0.0, 0.0], mass=1.0, temperature=20.0)

mdl = Model(name="test_hdf5")
prt = mdl.add_new_part(name="part")

# prt.to_hdf5(output_path, group_name="parts", mode="w")

n = prt.add_node(node)
# prt.to_json(filepath=output_path)
prt.to_hdf5(output_path, group_name="parts", mode="w")
# # n.save_to_hdf5(output_path, group_name="nodes", erase_data=True)
# mdl.save_to_hdf5(output_path, group_name="models", erase_data=True)
# # n_new = Node.load_from_hdf5(output_path, "nodes", n.uid)

# # Load the node from the file
# new_mdl = Model.load_from_hdf5(output_path, "models", mdl.uid)
# print(new_mdl.uid)
# # print(n_new._registration)

# # print(f"Loaded Node: {loaded_node.xyz}, Mass: {loaded_node.mass}, Temperature: {loaded_node.temperature}")
