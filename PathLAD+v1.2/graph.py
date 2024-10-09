from utils import *
from PathLADPlus import py_run_solver

# Replace '*.txt' with your actual file path
file_path = 'bench/qv_36.txt'
pattern_dirs = "pattern"
n = 7
m = 7
r = 2

induced = False
time = 60
only_first = True
soultion_number = 100

os.makedirs(pattern_dirs,exist_ok= True)
graphs = read_file_and_create_graph(file_path)
for i,graph in enumerate(graphs):
    export_graph(graph,os.path.join(pattern_dirs,f"graph_{i}.txt"))
    
grid_graph = generate_grid_with_Rb(n,m,r)
target_path = f"target_{n}_{m}.txt"
export_graph(grid_graph,target_path)

res = []
for file in os.listdir(pattern_dirs):
    if file.endswith(".txt"):
        pattern_path = os.path.join(pattern_dirs,file)
        res_file=py_run_solver(pattern_path, target_path, time, only_first, soultion_number, induced, 1)
        res.append(parse_result(res_file))
    else:
        continue
print(res)
    