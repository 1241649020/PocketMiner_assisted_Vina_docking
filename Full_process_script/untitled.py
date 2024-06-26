import torch
import esm
import os
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

model = esm.pretrained.esmfold_v1()
model = model.eval().cuda()

# Optionally, uncomment to set a chunk size for axial attention. This can help reduce memory.
# Lower sizes will have lower memory requirements at the cost of increased speed.
# model.set_chunk_size(128)

sequence = "MKSALTFSRRINPVFLAFFVVAFLSGIAGALQAPTLSLFLSTEVKVRPLWVGLFYTVNAIAGITVSFILAKRSDSRGDRRKLIMVCYLMAVGNCLLFAFNRDYLTLITAGVLLASVANTAMPQIFALAREYADSSAREVVMFSSIMRAQLSLAWVIGPPLSFMLALNYGFTLMFSIAAGIFVLSALVVWFILPSVPRAEPVVDAPVVVQGSLFADKNVLLLFIASMLMWTCNTMYIIDMPLYITASLGLPERLAGLLMGTAAGLEIPIMLLAGYSVRYFGKRKIMLFAVLAGVLFYTGLVLFKFKTALMLLQIFNAIFIGIVAGIGMLYFQDLMPGRAGAATTLFTNSISTGVILAGVLQGGLTETWGHDSVYVMAMVLSILALIICARVREA"
# Multimer prediction can be done with chains separated by ':'

with torch.no_grad():
    output = model.infer_pdb(sequence)

with open("result.pdb", "w") as f:
    f.write(output)
