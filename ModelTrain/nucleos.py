import psutil

# Obtener el número de núcleos físicos y lógicos
num_nucleos_fisicos = psutil.cpu_count(logical=False)  # Núcleos físicos
num_nucleos_logicos = psutil.cpu_count(logical=True)   # Núcleos lógicos

print(f"Núcleos físicos: {num_nucleos_fisicos}")
print(f"Núcleos lógicos: {num_nucleos_logicos}")
